"""exp007 problem-set freeze. Runs in the LiveCodeBench harness venv.

Selection (deterministic, pre-registered): release_v6, LeetCode platform,
contest_date >= 2025-01-01, sorted by (contest_date, question_id); ALL easy problems in the
window (19) + the FIRST 11 medium problems = 30. LeetCode-only because the pipeline's task
shape is a callable function; AtCoder problems are stdin/stdout programs.

Dumps statement, starter code, function name, and PUBLIC examples only. Private test cases
are never written here — the oracle stays inside the LCB harness (score stage).
"""

import json
from pathlib import Path

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset

HERE = Path(__file__).parent
N_MEDIUM = 11


def main() -> None:
    ds = load_code_generation_dataset(release_version="release_v6", start_date="2025-01-01")
    lc = [p for p in ds if p.platform.value == "leetcode"]
    lc.sort(key=lambda p: (p.contest_date, p.question_id))
    easy = [p for p in lc if p.difficulty.value == "easy"]
    medium = [p for p in lc if p.difficulty.value == "medium"][:N_MEDIUM]
    picked = easy + medium

    rows = []
    for p in picked:
        rows.append({
            "question_id": p.question_id,
            "question_title": p.question_title,
            "difficulty": p.difficulty.value,
            "contest_date": p.contest_date.isoformat(),
            "fn_name": p.metadata["func_name"],
            "starter_code": p.starter_code,
            "question_content": p.question_content,
            "public_examples": [
                {"input": t.input, "output": t.output} for t in p.public_test_cases
            ],
            "n_private_tests": len(p.private_test_cases),  # count only; content stays in harness
        })

    out = HERE / "lcb30.json"
    out.write_text(json.dumps(rows, indent=2))
    print(f"froze {len(rows)} problems ({len(easy)} easy + {len(medium)} medium) -> {out}")
    for r in rows:
        print(f"  {r['question_id']:>6} {r['difficulty']:<7} {r['contest_date'][:10]} {r['fn_name']}")


if __name__ == "__main__":
    main()
