"""LCB pilot stage 3 — score the generations with the harness's own machinery.

Runs in the LiveCodeBench harness venv. Extraction uses lcb_runner's extract_code (the
generic ``` fence branch); scoring uses codegen_metrics — the same function the official
custom_evaluator calls (lcb_runner/runner/scenario_router.py) — against each problem's
full public+private test set. Nothing here re-implements checking logic.
"""

import json
from pathlib import Path

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset
from lcb_runner.evaluation.compute_code_generation_metrics import codegen_metrics
from lcb_runner.utils.extraction_utils import extract_code

HERE = Path(__file__).parent
RESULTS = HERE / "results"


def main() -> None:
    raw = json.loads((RESULTS / "raw_outputs.json").read_text())
    rows = json.loads((RESULTS / "problems.json").read_text())
    by_qid = {r["question_id"]: r for r in rows}

    ds = load_code_generation_dataset(release_version="release_v6", start_date="2025-01-01")
    problems = {p.question_id: p for p in ds}

    samples, generations, meta = [], [], []
    for gen in raw["generations"]:
        qid = gen["question_id"]
        p = problems[qid]
        # extract_code's generic branch (last fenced block); lmstyle=None never matches
        # the two special-cased styles, so this is the leaderboard extraction path.
        codes = [extract_code(o, None) for o in gen["outputs"]]
        samples.append(p.get_evaluation_sample())
        generations.append(codes)
        meta.append({"question_id": qid, "difficulty": by_qid[qid]["difficulty"],
                     "platform": by_qid[qid]["platform"],
                     "empty_extractions": sum(1 for c in codes if not c)})

    metrics, results, _ = codegen_metrics(
        samples, generations, k_list=[1], num_process_evaluate=6, timeout=6,
    )

    per_problem = []
    for idx, m in enumerate(meta):
        # results[idx] holds one list of per-test outcomes per sample; a sample passes
        # if every test outcome is truthy (True/1), the harness's own convention.
        outcomes = results[idx]
        passed = sum(1 for sample_result in outcomes if all(x is True or x == 1 for x in sample_result))
        per_problem.append({**m, "samples_passed": passed, "n_samples": len(outcomes)})

    summary = {
        "model": raw["model"], "n_samples": raw["n_samples"],
        "pass@1": metrics["pass@1"],
        "by_difficulty": {},
        "by_platform": {},
        "per_problem": per_problem,
    }
    for key, field in (("by_difficulty", "difficulty"), ("by_platform", "platform")):
        for group in sorted({m[field] for m in per_problem}):
            g = [m for m in per_problem if m[field] == group]
            total = sum(m["n_samples"] for m in g)
            hits = sum(m["samples_passed"] for m in g)
            summary[key][group] = {"pass@1": round(hits / total, 3), "problems": len(g)}

    path = RESULTS / "lcb_pilot_summary.json"
    path.write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != "per_problem"}, indent=2))
    for m in per_problem:
        print(f"  {m['question_id']:>10}  {m['difficulty']:<6} {m['platform']:<8} "
              f"{m['samples_passed']}/{m['n_samples']} passed  (empty extractions: {m['empty_extractions']})")
    print(f"-> {path}")


if __name__ == "__main__":
    main()
