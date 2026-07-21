"""exp011 — verifier-generalization runner (HumanEval subset-30). See PRE_REGISTRATION.md.

Reruns the exp006 asymmetry design with the strong verifier S chosen by --verifier.
Weak generator W = gpt-4o-mini is unchanged. Budget is capped across the WHOLE exp011
results tree (all verifiers x benchmarks), enforcing the pre-registered $150 total.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS_ROOT = HERE / "results"
REPO = HERE.parent.parent

W = "gpt-4o-mini"
VERIFIERS = {
    "claude": "claude-sonnet-4-5",          # proven best NL-requirement conformance
    "gemini": "vertex_ai/gemini-2.5-pro",   # proven best code judge (via Vertex)
}

# frozen HumanEval subset (identical to exp006; hardness-enriched, not benchmark rates)
INTERESTING13 = [32, 47, 74, 81, 86, 90, 101, 116, 129, 142, 145, 153, 162]
RANDOM17 = [6, 7, 8, 22, 23, 26, 28, 36, 57, 59, 61, 64, 72, 115, 138, 150, 155]
PROBLEM_IDS = [f"HumanEval/{n}" for n in sorted(INTERESTING13 + RANDOM17)]
N_RUNS = 5
BUDGET_CAP_USD = 350.0            # raised from pre-registered $150 to absorb re-run waste (see DEVIATIONS.md)
FLOORS = {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}
GEN_TEMP, JUDGE_TEMP, JUDGE_THRESHOLD, MAX_RETRIES = 0.7, 1.0, 0.70, 3

# set by _configure(verifier)
S = ""
VERIFIER = ""
RESULTS = RESULTS_ROOT
CELLS: dict[str, dict] = {}


def _configure(verifier: str) -> None:
    global S, RESULTS, CELLS, VERIFIER
    if verifier not in VERIFIERS:
        sys.exit(f"unknown verifier {verifier!r}; choose from {list(VERIFIERS)}")
    VERIFIER = verifier
    S = VERIFIERS[verifier]
    RESULTS = RESULTS_ROOT / f"he_{verifier}"
    CELLS = {
        "control":        {"test_model": None, "judge_model": W},
        "strong_testgen": {"test_model": S,    "judge_model": W},
        "strong_judge":   {"test_model": None, "judge_model": S},
        "strong_both":    {"test_model": S,    "judge_model": S},
    }


def _load_env() -> None:
    from dotenv import load_dotenv

    load_dotenv(REPO / ".env")
    if VERIFIER == "gemini":
        # Vertex AI: dedicated SA + project for gemini-2.5-pro, overriding the .env's
        # old-project service account. gemini-2.5-pro is served in us-central1.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(
            "~/.config/gcloud/vgap-vertex-sa.json")
        os.environ["VERTEXAI_PROJECT"] = "vgap-vertex-bsb-4417"
        os.environ["VERTEXAI_LOCATION"] = "us-central1"


def _git_sha() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def spent_usd() -> float:
    """Total spend across the WHOLE exp011 tree, so the $150 cap is global."""
    total = 0.0
    for f in RESULTS_ROOT.rglob("usage.jsonl"):
        for line in f.read_text().splitlines():
            try:
                total += json.loads(line).get("cost_usd") or 0.0
            except json.JSONDecodeError:
                continue
    return total


def stage_plan() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    plan = {"generated_at": datetime.now(timezone.utc).isoformat(),
            "vgap_git_sha": _git_sha(), "weak": W, "strong": S, "cells": CELLS,
            "n_runs": N_RUNS, "subset": PROBLEM_IDS, "floors": FLOORS,
            "budget_cap_usd": BUDGET_CAP_USD, "escalation": "off (pinned to generator)"}
    (RESULTS / "plan.json").write_text(json.dumps(plan, indent=2))
    assert len(PROBLEM_IDS) == 30
    print(f"plan[{RESULTS.name}]: strong={S} | {len(CELLS)} cells x {N_RUNS} runs x 30, "
          f"global cap ${BUDGET_CAP_USD}, instrument @ {plan['vgap_git_sha'][:9]}")


async def _one_pass(cell: str, run_idx: int, ids: list[str], out_dir: Path) -> dict:
    os.environ["VGAP_PROMPT_VARIANT"] = "both"
    from vgap.pipeline.humaneval_runner import run_humaneval_tdd_evaluation
    from vgap.pipeline.instrumentation import register_usage_logger

    cfg = CELLS[cell]
    out_dir.mkdir(parents=True, exist_ok=True)
    register_usage_logger(out_dir / "usage.jsonl")
    return await run_humaneval_tdd_evaluation(
        problem_ids=ids, config_name=f"{cell}-run{run_idx}", out_dir=out_dir,
        generator_model=W, judge_model=cfg["judge_model"],
        escalation_model=W,  # escalation OFF: swap is identity
        test_model=cfg["test_model"],
        test_temperature=(1.0 if cfg["test_model"] == S else None),  # S test-author pinned T=1.0
        max_retries=MAX_RETRIES, judge_threshold=JUDGE_THRESHOLD,
        generator_temperature=GEN_TEMP, judge_temperature=JUDGE_TEMP,
        prompt_log_base=out_dir / "prompts", run_tag=f"{cell}|run{run_idx}",
    )


def stage_smoke() -> None:
    if not (RESULTS / "plan.json").is_file():
        sys.exit("smoke refuses: plan.json missing (run --stage plan)")
    _load_env()
    import asyncio

    summary = asyncio.run(_one_pass("strong_judge", 0, ["HumanEval/2"], RESULTS / "smoke"))
    r = summary["results"][0]
    print(json.dumps({"passed": r["humaneval_passed"], "tdd_success": r["tdd_success"],
                      "wall_time_s": r["wall_time_s"]}))
    rows = [json.loads(l) for l in (RESULTS / "smoke" / "usage.jsonl").read_text().splitlines()]
    models = {row.get("model") for row in rows if "instrumentation_error" not in row}
    bare = S.split("/")[-1]
    assert any(bare in (m or "") for m in models), f"strong judge never called: {models}"
    print(f"model check OK (strong={S}; billed {sorted(m for m in models if m)})")


def _run_complete(run_dir: Path) -> bool:
    return any(run_dir.glob("humaneval_tdd_*p_*.json"))


def stage_run(cell: str) -> None:
    if cell not in CELLS:
        sys.exit(f"unknown cell {cell!r}; choose from {list(CELLS)}")
    smoke_ok = (RESULTS / "smoke").is_dir() and any((RESULTS / "smoke").glob("humaneval_tdd_*.json"))
    if not smoke_ok:
        sys.exit("run refuses: no completed smoke")
    _load_env()
    import asyncio

    for k in range(1, N_RUNS + 1):
        run_dir = RESULTS / cell / f"run{k}"
        if _run_complete(run_dir):
            continue
        spent = spent_usd()
        if spent > BUDGET_CAP_USD:
            sys.exit(f"BUDGET CAP: ${spent:.2f} > ${BUDGET_CAP_USD} (global exp011)")
        print(f"=== {RESULTS.name}/{cell}/run{k} (spent ${spent:.2f}) ===", flush=True)
        asyncio.run(_one_pass(cell, k, PROBLEM_IDS, run_dir))
    print(f"{RESULTS.name}/{cell}: complete")


def run_files() -> list[Path]:
    out = []
    for cell in CELLS:
        for run_dir in sorted((RESULTS / cell).glob("run*")):
            fs = sorted(run_dir.glob("humaneval_tdd_*p_*.json"))
            if fs:
                out.append(fs[-1])
    return out


def stage_score() -> None:
    from evalplus.data import get_human_eval_plus

    ids = sorted(get_human_eval_plus().keys(), key=lambda t: int(t.split("/")[1]))
    files = run_files()
    if not files:
        sys.exit("score refuses: no completed runs")
    for i, f in enumerate(files, 1):
        key = "__".join([f.parts[-3], f.parts[-2]])
        res = RESULTS / "scores" / f"samples_{key}_eval_results.json"
        if res.is_file():
            continue
        res.parent.mkdir(parents=True, exist_ok=True)
        data = json.loads(f.read_text())
        sols = {r["problem_id"]: r.get("impl_code") or "" for r in data["results"]}
        samples = RESULTS / "scores" / f"samples_{key}.jsonl"
        with samples.open("w") as sf:
            for tid in ids:
                sf.write(json.dumps({"task_id": tid, "solution": sols.get(tid, "")}) + "\n")
        proc = subprocess.run([sys.executable, "-m", "evalplus.evaluate", "--dataset",
                               "humaneval", "--samples", str(samples)],
                              capture_output=True, text=True)
        if proc.returncode != 0 or not res.is_file():
            sys.exit(f"evalplus failed on {key}")
        print(f"[{i}/{len(files)}] {key} scored", flush=True)


def _statuses(entry):
    e = entry[0] if isinstance(entry, list) else entry
    return e["base_status"], e.get("plus_status", "unknown")


def _majority(v: list[bool]) -> bool:
    return sum(v) * 2 > len(v)


def _mcnemar_exact(b: int, c: int) -> float:
    from scipy.stats import binomtest

    n = b + c
    return 1.0 if n == 0 else float(binomtest(min(b, c), n, 0.5).pvalue)


def cell_metrics(cell: str) -> dict | None:
    import re

    per_pass, per_fa = {}, {}
    passes, fa_b, fa_p, frs, ntests, ncanon = [], [], [], [], [], []
    cdir = RESULTS / cell
    if not cdir.is_dir():
        return None
    for run_dir in sorted(cdir.glob("run*")):
        fs = sorted(run_dir.glob("humaneval_tdd_*p_*.json"))
        if not fs:
            continue
        key = "__".join([fs[-1].parts[-3], fs[-1].parts[-2]])
        score_f = RESULTS / "scores" / f"samples_{key}_eval_results.json"
        if not score_f.is_file():
            sys.exit(f"analyze refuses: missing score for {key} (run --stage score)")
        in_run = {r["problem_id"]: r for r in json.loads(fs[-1].read_text())["results"]}
        ev = {t: _statuses(e) for t, e in json.loads(score_f.read_text())["eval"].items()
              if t in in_run}
        passes.append(sum(1 for b, _ in ev.values() if b == "pass"))
        fa_b.append(sum(1 for t, (b, _) in ev.items()
                        if in_run[t]["tdd_success"] and b != "pass"))
        fa_p.append(sum(1 for t, (_, pl) in ev.items()
                        if in_run[t]["tdd_success"] and pl != "pass"))
        frs.append(sum(1 for t, (b, _) in ev.items()
                       if not in_run[t]["tdd_success"] and b == "pass"))
        ntests.append(sum(len(re.findall(r"^\s*def test_", r.get("test_code") or "", re.M))
                          for r in in_run.values()))
        ncanon.append(sum(len(re.findall(r"def test_canonical_example",
                                         r.get("test_code") or ""))
                          for r in in_run.values()))
        for t, (b, pl) in ev.items():
            per_pass.setdefault(t, []).append(b == "pass")
            per_fa.setdefault(t, []).append(bool(in_run[t]["tdd_success"]) and pl != "pass")
    if not passes:
        return None
    mean = lambda v: round(sum(v) / len(v), 2)
    return {"pass": passes, "pass_mean": mean(passes),
            "fa_base": fa_b, "fa_base_mean": mean(fa_b),
            "fa_plus": fa_p, "fa_plus_mean": mean(fa_p),
            "fr": frs, "fr_mean": mean(frs),
            "verdict_error_mean": mean([a + b for a, b in zip(fa_p, frs)]),
            "tests_per_run_mean": mean(ntests), "canonical_per_run_mean": mean(ncanon),
            "per_pass": per_pass, "per_fa": per_fa}


def _mcnemar_maj(a: dict, b: dict, keyname: str) -> float:
    common = sorted(set(a[keyname]) & set(b[keyname]))
    x = sum(1 for p in common if _majority(a[keyname][p]) and not _majority(b[keyname][p]))
    y = sum(1 for p in common if not _majority(a[keyname][p]) and _majority(b[keyname][p]))
    return _mcnemar_exact(x, y)


def stage_analyze() -> None:
    report: dict = {"generated_at": datetime.now(timezone.utc).isoformat(),
                    "vgap_git_sha": _git_sha(), "strong": S, "cells": {}, "contrasts": {},
                    "total_spent_usd": round(spent_usd(), 2)}
    metrics = {c: cell_metrics(c) for c in CELLS}
    metrics = {k: v for k, v in metrics.items() if v}
    for c, m in metrics.items():
        report["cells"][c] = {k: v for k, v in m.items()
                              if k not in ("per_pass", "per_fa")}
    ctrl = metrics.get("control")
    L = [f"# exp011 ANALYSIS — {RESULTS.name} (generated; do not hand-edit)", "",
         f"strong verifier: {S}", f"instrument @ {report['vgap_git_sha'][:9]}; "
         f"spend (global exp011) ${report['total_spent_usd']}", ""]
    for c, m in metrics.items():
        L.append(f"## {c}")
        L.append(f"- oracle pass /30: {m['pass']} (mean {m['pass_mean']})")
        L.append(f"- false accepts base/plus: {m['fa_base_mean']} / {m['fa_plus_mean']} "
                 f"(runs {m['fa_plus']})")
        L.append(f"- false rejects: {m['fr_mean']} (runs {m['fr']}); "
                 f"verdict-error total: {m['verdict_error_mean']}")
        L.append(f"- tests/run: {m['tests_per_run_mean']} "
                 f"(canonical {m['canonical_per_run_mean']})")
        if ctrl and c != "control":
            d_fa = round(m["fa_plus_mean"] - ctrl["fa_plus_mean"], 2)
            d_fr = round(m["fr_mean"] - ctrl["fr_mean"], 2)
            d_ve = round(m["verdict_error_mean"] - ctrl["verdict_error_mean"], 2)
            d_pass = round(m["pass_mean"] - ctrl["pass_mean"], 2)
            p_fa = round(_mcnemar_maj(ctrl, m, "per_fa"), 4)
            p_pass = round(_mcnemar_maj(ctrl, m, "per_pass"), 4)
            ver = {
                "FA_plus": f"d{d_fa} p={p_fa} -> " + (
                    "SIGNAL" if p_fa < 0.05 and abs(d_fa) > FLOORS["fa"] else "within noise"),
                "FR": f"d{d_fr} -> " + (
                    "beyond floor" if abs(d_fr) > FLOORS["fr"] else "within noise"),
                "verdict_error": f"d{d_ve} -> " + (
                    "beyond floor" if abs(d_ve) > FLOORS["verdict_error"] else "within noise"),
                "pass": f"d{d_pass} p={p_pass} -> " + (
                    "SIGNAL" if p_pass < 0.05 and abs(d_pass) > FLOORS["pass"]
                    else "within noise"),
            }
            report["contrasts"][c] = ver
            L.append(f"- vs control: {json.dumps(ver)}")
        L.append("")
    L.append("Floors (pre-registered): " + json.dumps(FLOORS)
             + ". Subset hardness-enriched; not benchmark rates.")
    (RESULTS / "asym_summary.json").write_text(json.dumps(report, indent=2))
    (RESULTS / "ANALYSIS.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verifier", required=True, choices=list(VERIFIERS))
    ap.add_argument("--stage", required=True,
                    choices=["plan", "smoke", "run", "score", "analyze"])
    ap.add_argument("--cell", default=None)
    args = ap.parse_args()
    _configure(args.verifier)
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
