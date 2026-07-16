"""exp007 oracle scorer. RUNS IN THE LIVECODEBENCH HARNESS VENV (not vgap).

Usage: <lcb-venv-python> score_lcb.py <run_result.json> <out_score.json>

Loads release_v6, maps each result row's question_id to its full public+private test
sample, and scores the stored impl_code with codegen_metrics — the same function the
official LCB evaluator calls. One generation per problem; a problem passes if every test
outcome is true. Rows with empty impl_code score fail without calling the checker.
"""

import json
import sys
from pathlib import Path

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset
from lcb_runner.evaluation.compute_code_generation_metrics import codegen_metrics


def main(run_file: str, out_file: str) -> None:
    data = json.loads(Path(run_file).read_text())
    rows = data["results"]

    ds = load_code_generation_dataset(release_version="release_v6", start_date="2025-01-01")
    problems = {p.question_id: p for p in ds}

    scored = {}
    samples, gens, idx_qids = [], [], []
    for r in rows:
        qid = r["question_id"]
        impl = (r.get("impl_code") or "").strip()
        if not impl:
            scored[qid] = {"oracle_pass": False, "reason": "empty impl"}
            continue
        samples.append(problems[qid].get_evaluation_sample())
        gens.append([impl])
        idx_qids.append(qid)

    if samples:
        _, results, _ = codegen_metrics(
            samples, gens, k_list=[1], num_process_evaluate=6, timeout=6,
        )
        for i, qid in enumerate(idx_qids):
            outcomes = results[i][0]
            scored[qid] = {"oracle_pass": all(x is True or x == 1 for x in outcomes)}

    Path(out_file).write_text(json.dumps({
        "run_file": run_file,
        "n": len(rows),
        "oracle": scored,
    }, indent=2))
    npass = sum(1 for v in scored.values() if v["oracle_pass"])
    print(f"{Path(run_file).name}: oracle pass {npass}/{len(rows)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
