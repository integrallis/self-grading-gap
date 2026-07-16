"""LiveCodeBench (LeetCode functional) → TDD task adapter.

Mirrors the humaneval_adapter task shape so the pipeline's templates work unchanged.
The task is built from a frozen problem row (see exp007 problems/freeze_problems.py):
statement, starter code, function name, and PUBLIC examples only — the private oracle
tests never reach any prompt. The starter's `class Solution` wrapper is flattened to a
top-level function signature: LCB's checker resolves top-level functions by name when no
Solution class is present, so a plain module scores directly."""

from __future__ import annotations

import re
from typing import Any, Dict


def derive_signature(starter_code: str, fn_name: str) -> str:
    """Top-level signature from LeetCode starter code (drops the class wrapper and self)."""
    m = re.search(rf"def\s+{re.escape(fn_name)}\s*\((.*?)\)(\s*->\s*[^:]+)?:", starter_code, re.DOTALL)
    if not m:
        raise ValueError(f"starter code has no def {fn_name}(...)")
    params = m.group(1).strip()
    params = re.sub(r"^self\s*,?\s*", "", params)
    ret = (m.group(2) or "").strip()
    return f"def {fn_name}({params}){' ' + ret if ret else ''}"


def create_tdd_task_from_lcb(problem: Dict[str, Any]) -> Dict[str, Any]:
    fn_name = problem["fn_name"]
    signature = derive_signature(problem["starter_code"], fn_name)
    qid = f"LCB/{problem['question_id']}"

    description = f"""{problem["question_content"]}

The problem statement above is the complete specification: it defines the valid inputs, the
required behavior, and the expected outputs. Do not add requirements it does not state, and
do not test or handle inputs outside the stated constraints.

Implement a single top-level function with exactly this signature (no class wrapper):
- {signature}

Include any typing imports the signature needs (e.g. `from typing import List`).
"""

    implementation_hints = f"""Implement one top-level function with its exact signature:
- {signature}

Implement a general algorithm. Do not hardcode results for specific inputs or pattern-match
test cases; every line must serve the general solution. Do not add constraints, validation,
or edge-case behavior the specification does not state. The file must be self-contained
(include typing imports). Do not wrap the function in a class.

Full problem statement:

{problem["question_content"]}"""

    test_scenarios = [
        f"Example: input {ex['input']!r} -> output {ex['output']!r}"
        for ex in problem["public_examples"]
    ] or ["Implement function matching specification"]

    return {
        "id": qid,
        "use_case_id": qid,
        "story_id": qid,
        "epic_id": "LIVECODEBENCH",
        "title": f"Implement {fn_name}()",
        "description": description,
        "specification": problem["question_content"],
        "specification_with_examples": True,  # activates the canonical-example ANCHOR blocks
        "test_scenarios": test_scenarios,
        "implementation_hints": implementation_hints,
        "acceptance_criteria": [f"{fn_name}() works as specified", "All test cases pass"],
        "dependencies": [],

        "lcb_metadata": {
            "question_id": problem["question_id"],
            "question_title": problem["question_title"],
            "difficulty": problem["difficulty"],
            "fn_name": fn_name,
            "signature": signature,
        },
    }
