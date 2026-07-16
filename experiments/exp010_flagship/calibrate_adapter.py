"""Automated adapter-fidelity calibration — bounds the adapter's contribution to H-D1.

Concern: the oracle reaches the candidate through a generated adapter; a mis-mapping adapter
could fail oracle tests even for a correct candidate, inflating false accepts. Transparency
proves the adapter transmits candidate behavior, not that it maps every symbol correctly.

Method (no human in the loop): take each package's REFERENCE solution — which passes its
oracle at 1.0 natively — and mechanically rename its public top-level API to opaque tokens
(a behavior-preserving AST transform: rename def/class statements and their references,
nothing else). The result is a KNOWN-CORRECT candidate with a foreign API — exactly the
adapter's real job. Two checks per package:
  1. auto-adapter (built from the known rename map, provably correct) must grade 1.0 — this
     certifies the mangle is behavior-preserving AND the task is solvable at 1.0; packages
     that fail this are excluded (renamer artifact, not adapter signal).
  2. a model authors an adapter BLIND (mangled source + import surface only) and is graded.
Since behavior == reference, any shortfall on (2) is pure adapter-authoring error. The mean
shortfall is the adapter-attributable false-accept rate to subtract from the raw H-D1.
"""

from __future__ import annotations

import ast
import asyncio
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DATASET = Path(os.environ.get("DATASET_DIR", REPO.parent / "rgrbench"))
sys.path.insert(0, str(DATASET))
sys.path.insert(0, str(HERE.parent / "exp009_dataset_pilot"))
OUT = HERE / "calibration"
S = "gpt-5.6-terra"


class _Renamer(ast.NodeTransformer):
    def __init__(self, mapping: dict[str, str]):
        self.m = mapping

    def visit_Name(self, node):
        if node.id in self.m:
            node.id = self.m[node.id]
        return node

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        if node.name in self.m:
            node.name = self.m[node.name]
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.name in self.m:
            node.name = self.m[node.name]
        return node


def public_top_level(src: str) -> list[str]:
    tree = ast.parse(src)
    return [n.name for n in tree.body
            if isinstance(n, (ast.ClassDef, ast.FunctionDef))
            and not n.name.startswith("_")]


def mangle_package(ref_dir: Path, dest: Path) -> dict[str, str]:
    """Rename public top-level symbols across the package to opaque tokens."""
    impls = {f: f.read_text() for f in ref_dir.glob("*.py") if f.name != "__init__.py"}
    names: list[str] = []
    for src in impls.values():
        names.extend(public_top_level(src))
    mapping = {n: f"Z{i}Q" for i, n in enumerate(sorted(set(names)))}
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "__init__.py").write_text("from candidate.impl import *\n")
    merged = "\n\n".join(impls.values())
    tree = _Renamer(mapping).visit(ast.parse(merged))
    ast.fix_missing_locations(tree)
    (dest / "impl.py").write_text(ast.unparse(tree))
    return mapping


def _surface_imports(surface: str) -> dict[str, list[str]]:
    """{oracle module path: [imported names]} from the surface's `from X import ...` lines."""
    out: dict[str, list[str]] = {}
    for m in re.finditer(r"from ([\w.]+) import ([\w, ]+)", surface):
        out.setdefault(m.group(1), []).extend(
            n.strip() for n in m.group(2).split(",") if n.strip())
    return out


def auto_adapter(mapping: dict[str, str], surface: str, dest: Path) -> None:
    """Provably-correct adapter from the known rename map: for each module the oracle imports
    from, emit that module aliasing each imported name to its mangled definition (or a
    pass-through when the name was not renamed). Pure imports/aliases — statically clean."""
    dest.mkdir(parents=True, exist_ok=True)
    for module, names in _surface_imports(surface).items():
        f = dest / (module.replace(".", os.sep) + ".py")
        f.parent.mkdir(parents=True, exist_ok=True)
        for part in f.relative_to(dest).parents:
            if part.name and not (dest / part / "__init__.py").exists():
                (dest / part / "__init__.py").write_text("")
        lines = []
        for name in names:
            src = mapping.get(name, name)
            lines.append(f"from candidate.impl import {src} as {name}")
        f.write_text("\n".join(lines) + "\n")


def stratified(n_per_tier: int = 6) -> list[dict]:
    card = json.loads((DATASET / "dataset.json").read_text())
    picked = []
    for tier in ("beginner", "intermediate", "advanced"):
        rows = [r for r in card["records"] if r["tier"] == tier]
        picked.extend(sorted(rows, key=lambda r: r["package"])[:n_per_tier])
    return picked


async def main():
    from langchain_core.messages import HumanMessage
    from langchain_litellm import ChatLiteLLM

    from dotenv import load_dotenv
    load_dotenv(REPO / ".env")
    from harness.adapter_check import check_adapter_source
    from harness.evaluate import evaluate
    from run_pilot import import_surface, oracle_file_for
    from vgap.pipeline.instrumentation import register_usage_logger
    from vgap.pipeline.prompts import content_to_text

    OUT.mkdir(exist_ok=True)
    register_usage_logger(OUT / "usage.jsonl")
    llm = ChatLiteLLM(model=S, temperature=1.0, max_tokens=4096)

    rows = []
    for prow in stratified():
        pkg = prow["package"]
        ref = DATASET / "src" / pkg
        oracle = oracle_file_for(pkg)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            cand = ws / "candidate"
            try:
                mapping = mangle_package(ref, cand)
            except SyntaxError:
                rows.append({"package": pkg, "excluded": "mangle-syntax"})
                continue

            # check 1: auto-adapter must certify behavior-preservation at 1.0
            auto = ws / "auto"
            auto_adapter(mapping, import_surface(oracle), auto)
            r_auto = evaluate(pkg, cand, auto, oracle)
            if not (r_auto.tests_total and r_auto.pass_fraction == 1.0):
                rows.append({"package": pkg, "excluded": "mangle-not-preserving",
                             "auto_pass": r_auto.pass_fraction,
                             "auto_reason": r_auto.invalid_reason})
                continue

            # check 2: model authors adapter blind, graded
            cand_src = (cand / "impl.py").read_text()
            surface = import_surface(oracle)
            prompt = ("Write ADAPTER module(s) exposing an existing implementation under the "
                      "exact import names below. ONLY imports/aliasing/delegation from "
                      "`candidate.impl`; FORBIDDEN: if/for/while/try, operators, "
                      "comprehensions, subscripts, numeric constants. Emit each module in a "
                      "fence headed by `# file: <name>.py`.\n\nImport surface:\n" + surface +
                      "\n\nImplementation:\n```python\n" + cand_src + "\n```")
            adir = ws / "terra"
            adir.mkdir()
            resp = await llm.ainvoke([HumanMessage(content=prompt)])
            for block in re.findall(r"```python\s*\n(.*?)```", content_to_text(resp.content),
                                    re.DOTALL):
                m = re.match(r"\s*#\s*file:\s*(\S+?)\.py", block)
                f = adir / f"{m.group(1) if m else pkg}.py"
                f.parent.mkdir(parents=True, exist_ok=True)
                for part in f.relative_to(adir).parents:
                    if part.name and not (adir / part / "__init__.py").exists():
                        (adir / part / "__init__.py").write_text("")
                f.write_text(block)
            r = evaluate(pkg, cand, adir, oracle)
            rows.append({"package": pkg, "tier": prow["tier"], "excluded": None,
                         "adapter_ok": r.adapter_ok, "valid": r.valid,
                         "pass_fraction": r.pass_fraction,
                         "adapter_error": round(1.0 - (r.pass_fraction or 0.0), 3),
                         "reason": r.invalid_reason})
        print(f"  {pkg:24s} {rows[-1]}", flush=True)

    (OUT / "calibration.json").write_text(json.dumps(rows, indent=2))
    usable = [r for r in rows if not r.get("excluded")]
    if usable:
        mean_err = sum(r["adapter_error"] for r in usable) / len(usable)
        clean = sum(1 for r in usable if r["adapter_error"] == 0.0)
        print(f"\ncalibration: {len(usable)} usable packages "
              f"({len(rows) - len(usable)} excluded)")
        print(f"perfect-adapter packages: {clean}/{len(usable)}")
        print(f"mean adapter-attributable failure rate: {mean_err:.3f}")


if __name__ == "__main__":
    asyncio.run(main())
