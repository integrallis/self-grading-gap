"""exp009 — staged pilot runner. See README.md (pre-registered).

Stages: plan | run | analyze. The dataset checkout provides the oracle suites,
requirements documents, and the evaluation harness (path via DATASET_DIR env or the
default sibling checkout)."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
REPO = HERE.parent.parent
DATASET = Path(os.environ.get(
    "DATASET_DIR", REPO.parent / "rgrbench"))
sys.path.insert(0, str(DATASET))

W = "gpt-4o-mini"
ADAPTER_MODEL = "gpt-5.6-terra"  # adapters are protocol plumbing, not the system under test
PER_TIER = 8
BUDGET_CAP_USD = 10.0


def _load_env():
    from dotenv import load_dotenv
    load_dotenv(REPO / ".env")


def _git_sha(repo: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def picked_packages() -> list[dict]:
    card = json.loads((DATASET / "dataset.json").read_text())
    picked = []
    for tier in ("beginner", "intermediate", "advanced"):
        rows = [r for r in card["records"] if r["tier"] == tier]
        picked.extend(sorted(rows, key=lambda r: r["package"])[:PER_TIER])
    return picked


def oracle_file_for(pkg: str) -> Path:
    direct = DATASET / "tests" / f"test_{pkg}.py"
    if direct.is_file():
        return direct
    for f in (DATASET / "tests").glob("test_*.py"):
        if re.search(rf"\bfrom {pkg}[.\s]|\bimport {pkg}\b", f.read_text()):
            return f
    raise FileNotFoundError(pkg)


def import_surface(oracle: Path) -> str:
    """Imports plus mechanically extracted call shapes — never test bodies."""
    tree = ast.parse(oracle.read_text())
    lines, shapes = set(), set()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names = ", ".join(a.name for a in node.names)
            lines.add(f"from {node.module} import {names}")
            imported.update(a.asname or a.name for a in node.names)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            argn = len(node.args) + len(node.keywords)
            f = node.func
            if isinstance(f, ast.Name) and f.id in imported:
                shapes.add(f"{f.id}(...) called with {argn} argument(s)")
            elif isinstance(f, ast.Attribute):
                shapes.add(f".{f.attr}(...) called with {argn} argument(s)")
    return ("\n".join(sorted(lines)) + "\n\nObserved call shapes:\n"
            + "\n".join(sorted(shapes)))


def _extract_code(text: str) -> str:
    m = re.search(r"```python\s*\n(.*?)```", text, re.DOTALL)
    return m.group(1) if m else text


def spent_usd() -> float:
    total = 0.0
    for f in RESULTS.rglob("usage.jsonl"):
        for line in f.read_text().splitlines():
            try:
                total += json.loads(line).get("cost_usd") or 0.0
            except json.JSONDecodeError:
                pass
    return total


def stage_plan():
    RESULTS.mkdir(exist_ok=True)
    pkgs = picked_packages()
    assert len(pkgs) == 3 * PER_TIER
    plan = {"generated_at": datetime.now(timezone.utc).isoformat(),
            "vgap_git_sha": _git_sha(REPO), "dataset_git_sha": _git_sha(DATASET),
            "model": W, "adapter_model": ADAPTER_MODEL,
            "packages": [p["package"] for p in pkgs],
            "budget_cap_usd": BUDGET_CAP_USD}
    (RESULTS / "plan.json").write_text(json.dumps(plan, indent=2))
    print(f"plan: {len(pkgs)} packages, dataset @ {plan['dataset_git_sha'][:9]}")


async def _one(pkg_row: dict, llm, adapter_llm) -> dict:
    from langchain_core.messages import HumanMessage

    from harness.evaluate import evaluate
    from vgap.pipeline.instrumentation import set_call_tag
    from vgap.pipeline.prompts import content_to_text

    pkg = pkg_row["package"]
    set_call_tag(f"exp009|{pkg}")
    out = RESULTS / pkg
    out.mkdir(parents=True, exist_ok=True)
    reqs = (DATASET / "requirements" / f"{pkg}.md").read_text()
    oracle = oracle_file_for(pkg)

    gen = await llm.ainvoke([HumanMessage(content=(
        "Implement the following requirements as a single Python module. Place all code "
        "in one file that will live at candidate/impl.py inside a package named "
        "`candidate`. Use clear public class/function names of your choosing. Standard "
        "library only. Return one ```python fence and nothing else.\n\n" + reqs))])
    cand_src = _extract_code(content_to_text(gen.content))
    cand_dir = out / "candidate"
    cand_dir.mkdir(exist_ok=True)
    (cand_dir / "__init__.py").write_text("from candidate.impl import *\n")
    (cand_dir / "impl.py").write_text(cand_src)

    surface = import_surface(oracle)
    adapt = await adapter_llm.ainvoke([HumanMessage(content=(
        "Write ADAPTER module(s) that expose an existing implementation under the exact "
        "import names below. Adapters may ONLY map APIs: import from `candidate.impl`, "
        "alias, wrap, rename, forward arguments. STRICTLY FORBIDDEN: if/for/while/try, "
        "any arithmetic or comparison operators, comprehensions, subscripts, and numeric "
        "constants — an automated checker rejects them. For each required module, emit a "
        "fence headed by a comment line `# file: <module path>.py`.\n\n"
        "Required import surface (from the grading tests):\n" + surface +
        "\n\nExisting implementation (candidate/impl.py):\n```python\n" + cand_src +
        "\n```"))])
    from harness.adapter_check import check_adapter_source

    def write_adapter(text: str, dest_dir: Path) -> list[str]:
        violations = []
        for block in re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL):
            m = re.match(r"\s*#\s*file:\s*(\S+?)\.py", block)
            rel = m.group(1) if m else pkg
            dest = dest_dir / f"{rel}.py"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(block)
            violations.extend(check_adapter_source(block, f"{rel}.py").violations)
        return violations

    adapter_dir = out / "adapter"
    adapter_dir.mkdir(exist_ok=True)
    text = content_to_text(adapt.content)
    violations = write_adapter(text, adapter_dir)
    if violations:  # one repair round: form feedback only, no grading information
        retry = await adapter_llm.ainvoke([HumanMessage(content=(
            "Your adapter violated the structural constraints below. Rewrite it. "
            "Remember: ONLY imports, aliasing, delegating classes/functions — no control "
            "flow, operators, subscripts, comprehensions, or numeric constants.\n\n"
            "Violations:\n" + "\n".join(violations) +
            "\n\nRequired import surface:\n" + surface +
            "\n\nCandidate (candidate/impl.py):\n```python\n" + cand_src + "\n```"))])
        for f in adapter_dir.rglob("*.py"):
            f.unlink()
        write_adapter(content_to_text(retry.content), adapter_dir)

    r = evaluate(pkg, cand_dir, adapter_dir, oracle)
    row = {"package": pkg, "tier": pkg_row["tier"], "provenance": pkg_row["provenance"],
           **{k: v for k, v in r.__dict__.items() if k != "per_test"},
           "per_test": r.per_test}
    (out / "result.json").write_text(json.dumps(row, indent=2))
    print(f"  {pkg:26s} valid={r.valid} pass={r.pass_fraction:.2f} "
          f"transp={r.transparency} reason={r.invalid_reason or '-'}", flush=True)
    return row


def stage_run():
    if not (RESULTS / "plan.json").is_file():
        sys.exit("run refuses: no plan.json")
    _load_env()
    import asyncio

    from langchain_litellm import ChatLiteLLM

    from vgap.pipeline.instrumentation import register_usage_logger
    register_usage_logger(RESULTS / "usage.jsonl")
    llm = ChatLiteLLM(model=W, temperature=0.7, max_tokens=4096)
    # gpt-5.x models accept only their default temperature (provider constraint)
    adapter_llm = ChatLiteLLM(model=ADAPTER_MODEL, temperature=1.0, max_tokens=4096)

    async def main():
        rows = []
        for p in picked_packages():
            if (RESULTS / p["package"] / "result.json").is_file():
                continue
            if spent_usd() > BUDGET_CAP_USD:
                sys.exit(f"BUDGET CAP: ${spent_usd():.2f}")
            rows.append(await _one(p, llm, adapter_llm))
        return rows

    asyncio.run(main())
    print("run complete")


def stage_analyze():
    rows = [json.loads((RESULTS / p["package"] / "result.json").read_text())
            for p in picked_packages()
            if (RESULTS / p["package"] / "result.json").is_file()]
    by_tier, by_prov = {}, {}
    taxonomy = {"static-reject": 0, "import-failure": 0, "low-transparency": 0}
    for r in rows:
        by_tier.setdefault(r["tier"], []).append(r)
        by_prov.setdefault(r["provenance"], []).append(r)
        if not r["valid"]:
            reason = r["invalid_reason"] or ""
            if "static" in reason:
                taxonomy["static-reject"] += 1
            elif "no tests" in reason:
                taxonomy["import-failure"] += 1
            elif "transparency" in reason:
                taxonomy["low-transparency"] += 1
    L = ["# exp009 ANALYSIS (generated; do not hand-edit)", "",
         f"packages evaluated: {len(rows)}; spend ${spent_usd():.2f}",
         f"valid evaluations: {sum(1 for r in rows if r['valid'])}/{len(rows)} "
         f"(H-C2 threshold 70%)", f"invalid taxonomy: {taxonomy}", ""]
    for name, groups in (("tier", by_tier), ("provenance", by_prov)):
        L.append(f"## by {name}")
        for g, rs in sorted(groups.items()):
            valid = [r for r in rs if r["valid"]]
            mean = (sum(r["pass_fraction"] for r in valid) / len(valid)) if valid else None
            L.append(f"- {g}: n={len(rs)}, valid={len(valid)}, "
                     f"mean pass fraction={mean if mean is None else round(mean, 3)}")
        L.append("")
    (RESULTS / "ANALYSIS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["plan", "run", "analyze"])
    a = ap.parse_args()
    {"plan": stage_plan, "run": stage_run, "analyze": stage_analyze}[a.stage]()
