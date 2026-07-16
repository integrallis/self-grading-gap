"""HumanEval → TDD task adapter.

Builds the task dict the pipeline templates consume: the description with signature
constraints, implementation hints carrying the full specification, worked examples as test
scenarios, and humaneval_metadata (whose presence activates the canonical-example anchoring
blocks in the RED templates). Dataset loading is the caller's job (EvalPlus's mirror of
original HumanEval)."""

from __future__ import annotations

import re
from typing import Any, Dict


def convert_humaneval_to_task_context(problem: Dict[str, Any]) -> Dict[str, Any]:
    prompt = problem["prompt"]
    entry_point = problem["entry_point"]
    task_id = problem["task_id"]

    lines = prompt.strip().split('\n')
    sig_line = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f'def {entry_point}('):
            sig_line = stripped
            break

    if not sig_line:
        raise ValueError(f"Could not find function signature for {entry_point} in {task_id}")

    description = "Implement the function according to specification"
    doctest_examples = []

    if f'def {entry_point}(' in prompt:
        target_func_start = prompt.split(f'def {entry_point}(', 1)[1]
        docstring_match = re.search(r'(?:"""(.+?)"""|\'\'\'(.+?)\'\'\')', target_func_start, re.DOTALL)
        if docstring_match:
            docstring = (docstring_match.group(1) or docstring_match.group(2)).strip()
        else:
            docstring = None
    else:
        docstring_match = re.search(r'(?:"""(.+?)"""|\'\'\'(.+?)\'\'\')', prompt, re.DOTALL)
        if docstring_match:
            docstring = (docstring_match.group(1) or docstring_match.group(2)).strip()
        else:
            docstring = None

    if docstring:

        if '>>>' in docstring:
            parts = docstring.split('>>>', 1)
            description = parts[0].strip()

            examples_text = parts[1]
            pattern = r'([^\n]+)\n\s*([^\n]+?)(?=\n\s*>>>|$)'
            for match in re.finditer(pattern, examples_text, re.MULTILINE):
                call = match.group(1).strip()
                result = match.group(2).strip()
                if call and result and not result.startswith('>>>'):
                    call = call.replace('>>>', '').strip()
                    doctest_examples.append(f"{call} → {result}")
        else:
            description = docstring.strip()

    return {
        "function_signature": sig_line,
        "full_prompt": prompt,
        "description": description,
        "doctest_examples": doctest_examples,
        "entry_point": entry_point,
        "task_id": task_id,
    }


def create_tdd_task_from_humaneval(problem: Dict[str, Any]) -> Dict[str, Any]:
    context = convert_humaneval_to_task_context(problem)

    signature_pattern = r'def\s+(\w+)\s*\([^)]*\)\s*(?:->[\s\w\[\],\.]+)?:'
    all_function_signatures = []
    for match in re.finditer(signature_pattern, context["full_prompt"]):
        sig = context["full_prompt"][match.start():match.end()].strip().rstrip(':')
        all_function_signatures.append(sig)
    all_function_names = [sig.split('(')[0].replace('def ', '').strip()
                          for sig in all_function_signatures]
    signatures_list = "\n".join(f"- {sig}" for sig in all_function_signatures)

    description_with_constraints = context["description"] + f"""

The docstring below is the complete specification: it defines the valid inputs, the required
behavior, and the expected outputs. Do not add requirements it does not state, and do not
test or handle inputs outside the domain it describes.

Function signatures (match exactly — names, parameter order, arity):
{signatures_list}
"""

    implementation_hints = f"""Implement every function below with its exact signature:
{signatures_list}

Implement a general algorithm. Do not hardcode results for specific inputs or pattern-match
test cases; every line must serve the general solution. Do not add constraints, validation,
or edge-case behavior the specification does not state.

Full specification:

{context["full_prompt"]}"""

    acceptance_criteria = [f"{fn}() works as specified" for fn in all_function_names]
    acceptance_criteria.append("All test cases pass")

    test_scenarios = []
    if context["doctest_examples"]:
        for ex in context["doctest_examples"]:
            test_scenarios.append(f"Example: {ex}")
    else:
        test_scenarios.append("Implement function matching specification")

    return {
        "id": context["task_id"],
        "use_case_id": context["task_id"],
        "story_id": context["task_id"],
        "epic_id": "HUMANEVAL",
        "title": f"Implement {context['entry_point']}()",
        "description": description_with_constraints,
        "specification": context["full_prompt"],
        "test_scenarios": test_scenarios,
        "implementation_hints": implementation_hints,
        "acceptance_criteria": acceptance_criteria,
        "dependencies": [],

        "humaneval_metadata": {
            "task_id": problem["task_id"],
            "entry_point": problem["entry_point"],
            "reference_test": problem["test"],
            "canonical_solution": problem.get("canonical_solution", ""),
            "function_signature": context["function_signature"],
            "full_prompt": context["full_prompt"],
        }
    }
