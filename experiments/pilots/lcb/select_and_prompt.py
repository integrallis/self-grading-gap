"""LCB pilot stage 1 — select a stratified 12-problem slice and render official prompts.

Runs in the LiveCodeBench harness venv (needs lcb_runner). Selection is deterministic:
release_v6 filtered to contest_date >= 2025-01-01 (>1 year after gpt-4o-mini's training
cutoff and ~6 months after its release), sorted by (contest_date, question_id), first two
LeetCode + first two AtCoder per difficulty tier. Prompts are rendered with the harness's
own generic template (PromptConstants.SYSTEM_MESSAGE_GENERIC +
get_generic_question_template_answer) so generation matches leaderboard conditions.
"""

import json
from pathlib import Path

from lcb_runner.benchmarks.code_generation import load_code_generation_dataset
from lcb_runner.prompts.code_generation import (
    PromptConstants,
    get_generic_question_template_answer,
)

OUT = Path(__file__).parent / "results"
OUT.mkdir(exist_ok=True)

PER_CELL = 2  # problems per (difficulty, platform) cell


def main() -> None:
    ds = load_code_generation_dataset(release_version="release_v6", start_date="2025-01-01")
    ds.sort(key=lambda p: (p.contest_date, p.question_id))

    selected = []
    for difficulty in ("easy", "medium", "hard"):
        for platform in ("leetcode", "atcoder"):
            cell = [p for p in ds
                    if p.difficulty.value == difficulty and p.platform.value == platform]
            selected.extend(cell[:PER_CELL])

    rows = []
    for p in selected:
        rows.append({
            "question_id": p.question_id,
            "question_title": p.question_title,
            "difficulty": p.difficulty.value,
            "platform": p.platform.value,
            "contest_date": p.contest_date.isoformat(),
            "has_starter_code": bool(p.starter_code),
            "system": PromptConstants.SYSTEM_MESSAGE_GENERIC,
            "user": get_generic_question_template_answer(p),
        })

    path = OUT / "problems.json"
    path.write_text(json.dumps(rows, indent=2))
    print(f"selected {len(rows)} problems -> {path}")
    for r in rows:
        print(f"  {r['question_id']:>10}  {r['difficulty']:<6} {r['platform']:<8} {r['contest_date'][:10]}")


if __name__ == "__main__":
    main()
