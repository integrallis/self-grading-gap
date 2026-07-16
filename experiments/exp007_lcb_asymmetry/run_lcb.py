"""exp007 — staged LCB model-asymmetry runner. See README.md (pre-registered).

Stage `score` shells out to the LiveCodeBench harness venv (LCB_VENV_PY env var or the
default sibling-checkout path) — the oracle never runs in the vgap venv."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
REPO = HERE.parent.parent
PROBLEMS_FILE = HERE / "problems" / "lcb30.json"
LCB_PY = Path(os.environ.get(
    "LCB_VENV_PY",
    REPO.parent / "benchmarks" / "LiveCodeBench" / ".venv" / "bin" / "python"))

W = "gpt-4o-mini"
S = "gpt-5.6-terra"

CELLS: dict[str, dict] = {
    "control":        {"test_model": None, "judge_model": W},
    "strong_testgen": {"test_model": S,    "judge_model": W},
    "strong_judge":   {"test_model": None, "judge_model": S},
    "strong_both":    {"test_model": S,    "judge_model": S},
}
N_RUNS = 5
BUDGET_CAP_USD = 80.0
FLOORS = {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}
GEN_TEMP, JUDGE_TEMP, JUDGE_THRESHOLD, MAX_RETRIES = 0.7, 1.0, 0.70, 3


def question_ids() -> list[str]:
    return [r["question_id"] for r in json.loads(PROBLEMS_FILE.read_text())]


def _load_env() -> None:
    from dotenv import load_dotenv

    load_dotenv(REPO / ".env")


def _git_sha() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def spent_usd() -> float:
    total = 0.0
    for f in RESULTS.rglob("usage.jsonl"):
        for line in f.read_text().splitlines():
            try:
                total += json.loads(line).get("cost_usd") or 0.0
            except json.JSONDecodeError:
                continue
    return total


def stage_plan() -> None:
    RESULTS.mkdir(exist_ok=True)
    ids = question_ids()
    assert len(ids) == 30
    plan = {"generated_at": datetime.now(timezone.utc).isoformat(),
            "vgap_git_sha": _git_sha(), "weak": W, "strong": S, "cells": CELLS,
            "n_runs": N_RUNS, "problems": ids, "floors": FLOORS,
            "budget_cap_usd": BUDGET_CAP_USD, "escalation": "off (pinned to generator)"}
    (RESULTS / "plan.json").write_text(json.dumps(plan, indent=2))
    print(f"plan: {len(CELLS)} cells x {N_RUNS} runs x {len(ids)} problems, "
          f"cap ${BUDGET_CAP_USD}, instrument @ {plan['vgap_git_sha'][:9]}")


async def _one_pass(cell: str, run_idx: int, ids: list[str], out_dir: Path) -> dict:
    os.environ["VGAP_PROMPT_VARIANT"] = "both"
    from vgap.pipeline.instrumentation import register_usage_logger
    from vgap.pipeline.lcb_runner_local import run_lcb_tdd_evaluation

    cfg = CELLS[cell]
    out_dir.mkdir(parents=True, exist_ok=True)
    register_usage_logger(out_dir / "usage.jsonl")
    return await run_lcb_tdd_evaluation(
        problems_file=PROBLEMS_FILE, question_ids=ids,
        config_name=f"{cell}-run{run_idx}", out_dir=out_dir,
        generator_model=W, judge_model=cfg["judge_model"],
        escalation_model=W,  # escalation OFF: swap is identity
        test_model=cfg["test_model"],
        # gpt-5.x models accept only their default temperature (provider constraint)
        test_temperature=(1.0 if cfg["test_model"] == S else None),
        max_retries=MAX_RETRIES, judge_threshold=JUDGE_THRESHOLD,
        generator_temperature=GEN_TEMP, judge_temperature=JUDGE_TEMP,
        prompt_log_base=out_dir / "prompts", run_tag=f"{cell}|run{run_idx}",
    )


def _score_one(run_file: Path, out_file: Path) -> None:
    proc = subprocess.run([str(LCB_PY), str(HERE / "score_lcb.py"),
                           str(run_file), str(out_file)],
                          capture_output=True, text=True)
    if proc.returncode != 0 or not out_file.is_file():
        sys.exit(f"scorer failed on {run_file.name}:\n{proc.stderr[-2000:]}")
    print(proc.stdout.strip(), flush=True)


def stage_smoke() -> None:
    if not (RESULTS / "plan.json").is_file():
        sys.exit("smoke refuses: plan.json missing")
    if not LCB_PY.is_file():
        sys.exit(f"smoke refuses: LCB venv python missing at {LCB_PY}")
    _load_env()
    import asyncio

    ids = question_ids()[:1]
    summary = asyncio.run(_one_pass("strong_judge", 0, ids, RESULTS / "smoke"))
    r = summary["results"][0]
    fs = sorted((RESULTS / "smoke").glob("lcb_tdd_*p_*.json"))
    _score_one(fs[-1], RESULTS / "smoke" / "smoke_score.json")
    oracle = json.loads((RESULTS / "smoke" / "smoke_score.json").read_text())["oracle"]
    print(json.dumps({"tdd_success": r["tdd_success"],
                      "oracle_pass": oracle[r["question_id"]]["oracle_pass"],
                      "wall_time_s": r["wall_time_s"]}))
    rows = [json.loads(l) for l in (RESULTS / "smoke" / "usage.jsonl").read_text().splitlines()]
    models = {row.get("model") for row in rows if "instrumentation_error" not in row}
    assert any(S in (m or "") for m in models), f"strong judge never called: {models}"
    print(f"model check ✓ ({sorted(m for m in models if m)})")


def _run_complete(run_dir: Path) -> bool:
    return any(run_dir.glob("lcb_tdd_*p_*.json"))


def stage_run(cell: str) -> None:
    if cell not in CELLS:
        sys.exit(f"unknown cell {cell!r}; choose from {list(CELLS)}")
    smoke_ok = (RESULTS / "smoke").is_dir() and any((RESULTS / "smoke").glob("lcb_tdd_*.json"))
    if not smoke_ok:
        sys.exit("run refuses: no completed smoke")
    _load_env()
    import asyncio

    ids = question_ids()
    for k in range(1, N_RUNS + 1):
        run_dir = RESULTS / cell / f"run{k}"
        if _run_complete(run_dir):
            continue
        spent = spent_usd()
        if spent > BUDGET_CAP_USD:
            sys.exit(f"BUDGET CAP: ${spent:.2f} > ${BUDGET_CAP_USD}")
        print(f"=== {cell}/run{k} (spent ${spent:.2f}) ===", flush=True)
        asyncio.run(_one_pass(cell, k, ids, run_dir))
    print(f"{cell}: complete")


def run_files() -> list[Path]:
    out = []
    for cell in CELLS:
        for run_dir in sorted((RESULTS / cell).glob("run*")):
            fs = sorted(run_dir.glob("lcb_tdd_*p_*.json"))
            if fs:
                out.append(fs[-1])
    return out


def stage_score() -> None:
    files = run_files()
    if not files:
        sys.exit("score refuses: no completed runs")
    (RESULTS / "scores").mkdir(exist_ok=True)
    for i, f in enumerate(files, 1):
        key = "__".join([f.parts[-3], f.parts[-2]])
        out = RESULTS / "scores" / f"{key}_oracle.json"
        if out.is_file():
            continue
        _score_one(f, out)
        print(f"[{i}/{len(files)}] {key} scored", flush=True)


def _majority(v: list[bool]) -> bool:
    return sum(v) * 2 > len(v)


def _mcnemar_exact(b: int, c: int) -> float:
    from scipy.stats import binomtest

    n = b + c
    return 1.0 if n == 0 else float(binomtest(min(b, c), n, 0.5).pvalue)


def cell_metrics(cell: str) -> dict | None:
    import re

    per_pass, per_fa = {}, {}
    passes, fas, frs, ntests, ncanon = [], [], [], [], []
    cdir = RESULTS / cell
    if not cdir.is_dir():
        return None
    for run_dir in sorted(cdir.glob("run*")):
        fs = sorted(run_dir.glob("lcb_tdd_*p_*.json"))
        if not fs:
            continue
        key = "__".join([fs[-1].parts[-3], fs[-1].parts[-2]])
        score_f = RESULTS / "scores" / f"{key}_oracle.json"
        if not score_f.is_file():
            sys.exit(f"analyze refuses: missing score for {key} (run --stage score)")
        in_run = {r["question_id"]: r for r in json.loads(fs[-1].read_text())["results"]}
        oracle = {q: v["oracle_pass"]
                  for q, v in json.loads(score_f.read_text())["oracle"].items()}
        passes.append(sum(1 for v in oracle.values() if v))
        fas.append(sum(1 for q, v in oracle.items()
                       if in_run[q]["tdd_success"] and not v))
        frs.append(sum(1 for q, v in oracle.items()
                       if not in_run[q]["tdd_success"] and v))
        ntests.append(sum(len(re.findall(r"^\s*def test_", r.get("test_code") or "", re.M))
                          for r in in_run.values()))
        ncanon.append(sum(len(re.findall(r"def test_canonical_example",
                                         r.get("test_code") or ""))
                          for r in in_run.values()))
        for q, v in oracle.items():
            per_pass.setdefault(q, []).append(v)
            per_fa.setdefault(q, []).append(bool(in_run[q]["tdd_success"]) and not v)
    if not passes:
        return None
    mean = lambda v: round(sum(v) / len(v), 2)
    return {"pass": passes, "pass_mean": mean(passes),
            "fa": fas, "fa_mean": mean(fas),
            "fr": frs, "fr_mean": mean(frs),
            "verdict_error_mean": mean([a + b for a, b in zip(fas, frs)]),
            "tests_per_run_mean": mean(ntests), "canonical_per_run_mean": mean(ncanon),
            "per_pass": per_pass, "per_fa": per_fa}


def _mcnemar_maj(a: dict, b: dict, keyname: str) -> float:
    common = sorted(set(a[keyname]) & set(b[keyname]))
    x = sum(1 for p in common if _majority(a[keyname][p]) and not _majority(b[keyname][p]))
    y = sum(1 for p in common if not _majority(a[keyname][p]) and _majority(b[keyname][p]))
    return _mcnemar_exact(x, y)


def stage_analyze() -> None:
    report: dict = {"generated_at": datetime.now(timezone.utc).isoformat(),
                    "vgap_git_sha": _git_sha(), "cells": {}, "contrasts": {},
                    "total_spent_usd": round(spent_usd(), 2)}
    metrics = {c: cell_metrics(c) for c in CELLS}
    metrics = {k: v for k, v in metrics.items() if v}
    for c, m in metrics.items():
        report["cells"][c] = {k: v for k, v in m.items()
                              if k not in ("per_pass", "per_fa")}
    ctrl = metrics.get("control")
    L = ["# exp007 ANALYSIS (generated; do not hand-edit)", "",
         f"instrument @ {report['vgap_git_sha'][:9]}; spend ${report['total_spent_usd']}", ""]
    for c, m in metrics.items():
        L.append(f"## {c}")
        L.append(f"- oracle pass /30: {m['pass']} (mean {m['pass_mean']})")
        L.append(f"- false accepts: {m['fa_mean']} (runs {m['fa']})")
        L.append(f"- false rejects: {m['fr_mean']} (runs {m['fr']}); "
                 f"verdict-error total: {m['verdict_error_mean']}")
        L.append(f"- tests/run: {m['tests_per_run_mean']} "
                 f"(canonical {m['canonical_per_run_mean']})")
        if ctrl and c != "control":
            d_fa = round(m["fa_mean"] - ctrl["fa_mean"], 2)
            d_fr = round(m["fr_mean"] - ctrl["fr_mean"], 2)
            d_ve = round(m["verdict_error_mean"] - ctrl["verdict_error_mean"], 2)
            d_pass = round(m["pass_mean"] - ctrl["pass_mean"], 2)
            p_fa = round(_mcnemar_maj(ctrl, m, "per_fa"), 4)
            p_pass = round(_mcnemar_maj(ctrl, m, "per_pass"), 4)
            ver = {
                "FA": f"Δ{d_fa} p={p_fa} → " + (
                    "SIGNAL" if p_fa < 0.05 and abs(d_fa) > FLOORS["fa"] else "within noise"),
                "FR": f"Δ{d_fr} → " + (
                    "beyond floor" if abs(d_fr) > FLOORS["fr"] else "within noise"),
                "verdict_error": f"Δ{d_ve} → " + (
                    "beyond floor" if abs(d_ve) > FLOORS["verdict_error"] else "within noise"),
                "pass": f"Δ{d_pass} p={p_pass} → " + (
                    "SIGNAL" if p_pass < 0.05 and abs(d_pass) > FLOORS["pass"]
                    else "within noise"),
            }
            report["contrasts"][c] = ver
            L.append(f"- vs control: {json.dumps(ver)}")
        L.append("")
    L.append("Floors (pre-registered): " + json.dumps(FLOORS)
             + ". lcb30 = 19 easy + 11 medium LeetCode, post-2025 window; not benchmark rates.")
    (RESULTS / "asym_summary.json").write_text(json.dumps(report, indent=2))
    (RESULTS / "ANALYSIS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=["plan", "smoke", "run", "score", "analyze"])
    ap.add_argument("--cell", default=None)
    args = ap.parse_args()
    if args.stage == "plan":
        stage_plan()
    elif args.stage == "smoke":
        stage_smoke()
    elif args.stage == "run":
        if not args.cell:
            sys.exit("--stage run requires --cell")
        stage_run(args.cell)
    elif args.stage == "score":
        stage_score()
    else:
        stage_analyze()


if __name__ == "__main__":
    main()
