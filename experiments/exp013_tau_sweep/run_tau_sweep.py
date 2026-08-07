"""exp010 — flagship runner. See README.md (pre-registered).

Stages: plan | run --cell <control|strong_judge> | analyze. The RGR pipeline builds each
package from its requirements document; the produced src/solution package is persisted and
graded by the dataset's oracle through the v3.1 harness with a terra-authored adapter."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
REPO = HERE.parent.parent
DATASET = Path(os.environ.get("DATASET_DIR", REPO.parent / "rgrbench"))
sys.path.insert(0, str(DATASET))
sys.path.insert(0, str(HERE.parent / "exp009_dataset_pilot"))

W = "gpt-4o-mini"
S = "gpt-5.6-terra"
CELLS = {"control": W, "strong_judge": S}  # value = judge model (all judge roles)
N_RUNS = int(os.environ.get("EXP013_NRUNS", "1"))
TAU = float(os.environ.get("EXP013_TAU", "0.70"))  # RED/GREEN judge threshold (swept)
BUDGET_CAP_USD = float(os.environ.get("EXP013_BUDGET", "60"))


def _load_env():
    from dotenv import load_dotenv
    load_dotenv(REPO / ".env")


def _sha(repo: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def packages() -> list[dict]:
    card = json.loads((DATASET / "dataset.json").read_text())
    return sorted(card["records"], key=lambda r: r["package"])


def spent_usd() -> float:
    total = 0.0
    for f in RESULTS.rglob("usage*.jsonl"):
        for line in f.read_text().splitlines():
            try:
                total += json.loads(line).get("cost_usd") or 0.0
            except json.JSONDecodeError:
                pass
    return total


def make_task(pkg: str) -> dict:
    reqs = (DATASET / "requirements" / f"{pkg}.md").read_text()
    # strip the traceability block: it names oracle test functions
    reqs = re.sub(r"## Traceability.*", "", reqs, flags=re.DOTALL).strip()
    return {
        "id": pkg, "use_case_id": pkg, "story_id": pkg, "epic_id": "DATASET",
        "title": reqs.splitlines()[0].lstrip("# ").strip(),
        "description": reqs,
        "specification": reqs,
        "test_scenarios": [],
        "implementation_hints": (
            "Implement the requirements as general algorithms inside the `solution` "
            "package (src/solution/). Choose clear public names; do not hardcode "
            "specific inputs. Standard library only."),
        "acceptance_criteria": ["All acceptance criteria in the requirements hold"],
        "dependencies": [],
    }


async def run_pipeline(pkg: str, judge_model: str, out: Path) -> dict:
    from langchain_litellm import ChatLiteLLM

    from vgap.pipeline.bootstrap import PythonBootstrapper
    from vgap.pipeline.coordinator import TDDCoordinatorAgent
    from vgap.pipeline.state import create_initial_tdd_cycle_state
    from vgap.pipeline.subgraph import create_tdd_cycle_subgraph

    generator_llm = ChatLiteLLM(model=W, temperature=0.7)
    judge_llm = ChatLiteLLM(model=judge_model, temperature=1.0)
    task = make_task(pkg)

    with tempfile.TemporaryDirectory() as tmpdir:
        ws = Path(tmpdir) / "solution"
        ws.mkdir(parents=True)
        for cmd in (["git", "init"], ["git", "config", "user.name", "T"],
                    ["git", "config", "user.email", "t@e.c"]):
            subprocess.run(cmd, cwd=ws, capture_output=True, check=True)
        files = PythonBootstrapper().bootstrap(ws, {
            "project_name": "solution", "package_name": "solution",
            "python_version": "3.11", "include_tdd_extras": True})
        for fp, content in files.items():
            p = ws / fp
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        subprocess.run(["git", "add", "."], cwd=ws, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=ws,
                       capture_output=True, check=True)

        coordinator = TDDCoordinatorAgent(
            llm=generator_llm, judge_llm=judge_llm, escalation_llm=generator_llm,
            max_retries=3, judge_threshold=TAU)
        graph = create_tdd_cycle_subgraph(coordinator=coordinator)
        state = create_initial_tdd_cycle_state(
            task=task, workspace_path=str(ws), project_name="solution",
            cartridge={"programming_language": "Python", "application_type": "Library",
                       "frameworks": [], "testing_frameworks": ["pytest"],
                       "deployment_target": "local"},
            project_brief=f"Package: {pkg}\n\n{task['title']}",
            existing_implementation="", max_retries=3, judge_threshold=TAU,
            git_enabled=False, bootstrapped=True)
        state["generator_llm"] = generator_llm
        result = await graph.ainvoke(state)

        # persist the produced implementation as the harness candidate package
        cand = out / "candidate"
        if cand.exists():
            shutil.rmtree(cand)
        src_pkg = ws / "src" / "solution"
        shutil.copytree(src_pkg, cand)
        (out / "self_tests.py").write_text(result.get("test_code") or "")
        return {"self_verdict": bool(result.get("success")),
                "red_attempts": result.get("red_attempts", 0),
                "green_attempts": result.get("green_attempts", 0),
                "self_test_count": len(re.findall(r"^def test_",
                                                  result.get("test_code") or "", re.M))}


async def grade(pkg: str, out: Path, adapter_llm) -> dict:
    from langchain_core.messages import HumanMessage

    from harness.adapter_check import check_adapter_source
    from harness.evaluate import evaluate
    from run_pilot import import_surface, oracle_file_for
    from vgap.pipeline.prompts import content_to_text

    oracle = oracle_file_for(pkg)
    surface = import_surface(oracle)
    cand = out / "candidate"
    cand_src = "\n\n".join(f"# candidate/{f.name}\n{f.read_text()}"
                           for f in sorted(cand.glob("*.py")))

    def write_adapter(text: str, dest: Path) -> list[str]:
        violations = []
        for block in re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL):
            m = re.match(r"\s*#\s*file:\s*(\S+?)\.py", block)
            rel = m.group(1) if m else pkg
            d = dest / f"{rel}.py"
            d.parent.mkdir(parents=True, exist_ok=True)
            d.write_text(block)
            violations.extend(check_adapter_source(block, f"{rel}.py").violations)
        return violations

    prompt = ("Write ADAPTER module(s) exposing an existing implementation under the "
              "exact import names below. Adapters may ONLY map APIs: import from the "
              "`candidate` package modules shown, alias, wrap, rename, forward arguments. "
              "STRICTLY FORBIDDEN: if/for/while/try, arithmetic or comparison operators, "
              "comprehensions, subscripts, numeric constants. For each required module "
              "emit a fence headed by `# file: <module path>.py`.\n\n"
              f"Required import surface:\n{surface}\n\nCandidate package:\n```python\n"
              f"{cand_src}\n```")
    adapter_dir = out / "adapter"
    if adapter_dir.exists():
        shutil.rmtree(adapter_dir)
    adapter_dir.mkdir()
    resp = await adapter_llm.ainvoke([HumanMessage(content=prompt)])
    violations = write_adapter(content_to_text(resp.content), adapter_dir)
    if violations:
        retry = await adapter_llm.ainvoke([HumanMessage(content=(
            "Your adapter violated structural constraints. Rewrite (mapping only).\n\n"
            "Violations:\n" + "\n".join(violations) + "\n\n" + prompt))])
        for f in adapter_dir.rglob("*.py"):
            f.unlink()
        write_adapter(content_to_text(retry.content), adapter_dir)

    r = evaluate(pkg, cand, adapter_dir, oracle)
    return {k: v for k, v in r.__dict__.items()}


def stage_plan():
    RESULTS.mkdir(exist_ok=True)
    plan = {"generated_at": datetime.now(timezone.utc).isoformat(),
            "vgap_git_sha": _sha(REPO), "dataset_git_sha": _sha(DATASET),
            "weak": W, "strong": S, "cells": CELLS, "n_runs": N_RUNS,
            "packages": [p["package"] for p in packages()],
            "budget_cap_usd": BUDGET_CAP_USD}
    (RESULTS / "plan.json").write_text(json.dumps(plan, indent=2))
    print(f"plan: {len(plan['packages'])} pkgs x {len(CELLS)} cells x {N_RUNS} runs; "
          f"dataset @ {plan['dataset_git_sha'][:9]}")


def stage_run(cell: str, only: str | None = None):
    if cell not in CELLS:
        sys.exit(f"unknown cell {cell!r}")
    _load_env()
    from langchain_litellm import ChatLiteLLM

    from vgap.pipeline.instrumentation import register_usage_logger, set_call_tag
    register_usage_logger(RESULTS / f"usage-tau{TAU:.2f}-{cell}.jsonl")
    adapter_llm = ChatLiteLLM(model=S, temperature=1.0, max_tokens=4096)

    async def main():
        pkgs = packages()
        if only:
            pkgs = [p for p in pkgs if p["package"] == only]
        for prow in pkgs:
            pkg = prow["package"]
            for n in range(1, N_RUNS + 1):
                out = RESULTS / f"tau{TAU:.2f}" / cell / pkg / f"run{n}"
                if (out / "result.json").is_file():
                    continue
                if spent_usd() > BUDGET_CAP_USD:
                    sys.exit(f"BUDGET CAP: ${spent_usd():.2f}")
                out.mkdir(parents=True, exist_ok=True)
                set_call_tag(f"exp013|tau{TAU:.2f}|{cell}|{pkg}|run{n}")
                try:
                    pipe = await run_pipeline(pkg, CELLS[cell], out)
                    ev = await grade(pkg, out, adapter_llm)
                except Exception as e:
                    pipe = {"self_verdict": False, "error": f"{type(e).__name__}: {e}"}
                    ev = {"valid": False, "invalid_reason": "run error"}
                row = {"package": pkg, "cell": cell, "run": n,
                       "tier": prow["tier"], "provenance": prow["provenance"], **pipe,
                       "oracle": {k: ev.get(k) for k in
                                  ("valid", "invalid_reason", "pass_fraction",
                                   "tests_total", "tests_passed", "transparency",
                                   "transparency_note", "adapter_ok")}}
                (out / "result.json").write_text(json.dumps(row, indent=2))
                o = row["oracle"]
                print(f"  {cell}/{pkg}/run{n}: self={row['self_verdict']} "
                      f"valid={o['valid']} pass={o.get('pass_fraction')}", flush=True)

    asyncio.run(main())
    print(f"{cell}: complete")


def wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    from math import sqrt
    z, p = 1.96, k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def stage_analyze():
    rows = [json.loads(f.read_text()) for f in RESULTS.rglob("result.json")]
    L = ["# exp010 ANALYSIS (generated; do not hand-edit)", "",
         f"runs: {len(rows)}; spend ${spent_usd():.2f}", ""]
    for cell in CELLS:
        rs = [r for r in rows if r["cell"] == cell]
        valid = [r for r in rs if r["oracle"]["valid"]]
        claims = [r for r in valid if r["self_verdict"]]
        fa = [r for r in claims if (r["oracle"]["pass_fraction"] or 0) < 1.0]
        fr = [r for r in valid if not r["self_verdict"]
              and (r["oracle"]["pass_fraction"] or 0) == 1.0]
        L.append(f"## {cell}: runs={len(rs)} valid={len(valid)} claims={len(claims)}")
        if claims:
            p = len(fa) / len(claims)
            lo, hi = wilson(len(fa), len(claims))
            L.append(f"- H-D1 conditional FA of claims: {p:.3f} "
                     f"[{lo:.3f}, {hi:.3f}] (n={len(claims)})")
        L.append(f"- false rejects: {len(fr)}; mean oracle pass fraction (valid): "
                 f"{sum((r['oracle']['pass_fraction'] or 0) for r in valid) / max(1, len(valid)):.3f}")
        multi = [r for r in claims if r.get("green_attempts", 0) > 1]
        single = [r for r in claims if r.get("green_attempts", 0) <= 1]
        for name, grp in (("first-attempt", single), ("multi-attempt", multi)):
            g_fa = [r for r in grp if (r["oracle"]["pass_fraction"] or 0) < 1.0]
            if grp:
                L.append(f"- H-D2 {name} claims FA: {len(g_fa)}/{len(grp)} "
                         f"= {len(g_fa) / len(grp):.3f}")
        for tier in ("beginner", "intermediate", "advanced"):
            t_claims = [r for r in claims if r["tier"] == tier]
            t_fa = [r for r in t_claims if (r["oracle"]["pass_fraction"] or 0) < 1.0]
            if t_claims:
                L.append(f"- H-D4 {tier} FA: {len(t_fa)}/{len(t_claims)} "
                         f"= {len(t_fa) / len(t_claims):.3f}")
        L.append("")
    (RESULTS / "ANALYSIS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True, choices=["plan", "run", "analyze"])
    ap.add_argument("--cell")
    ap.add_argument("--only")
    a = ap.parse_args()
    if a.stage == "plan":
        stage_plan()
    elif a.stage == "run":
        stage_run(a.cell, a.only)
    else:
        stage_analyze()
