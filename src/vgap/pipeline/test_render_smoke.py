"""Render-contract smoke tests for the prompt templates: every template renders end-to-end
from a HumanEval-shaped task, embeds the right inputs, and states the exact output format
the parsers depend on (coordinator.py rating regexes, python_agent.py fence extraction)."""

import pytest

from vgap.pipeline.humaneval_adapter import create_tdd_task_from_humaneval
from vgap.pipeline.prompts import MaestroPromptManager

PROBLEM = {
    "task_id": "HumanEval/0",
    "entry_point": "has_close_elements",
    "prompt": (
        "from typing import List\n\n\n"
        "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n"
        '    """ Check if in given list of numbers, are any two numbers closer to each other than\n'
        "    given threshold.\n"
        "    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n"
        "    False\n"
        "    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n"
        "    True\n"
        '    """\n'
    ),
    "test": "def check(candidate): pass",
    "canonical_solution": "    return False\n",
}

TEST_CODE = "from solution import has_close_elements\n\ndef test_a():\n    assert has_close_elements([1.0, 2.0], 0.5) is False\n"
IMPL_CODE = "def has_close_elements(numbers, threshold):\n    return False\n"


@pytest.fixture()
def task():
    return create_tdd_task_from_humaneval(PROBLEM)


@pytest.fixture()
def manager():
    return MaestroPromptManager()


def gen_kwargs(task, **overrides):
    kw = dict(task=task, epic=None, story=None, use_case=None,
              existing_implementation="", existing_test_files={}, test_results="",
              project_name="solution", project_brief="", recent_commits=[],
              judge_feedback="", previous_test_attempt="", cartridge={},
              json_error_feedback="")
    kw.update(overrides)
    return kw


def test_adapter_hint_content(task):
    hints = task["implementation_hints"]
    assert "def has_close_elements(numbers: List[float], threshold: float) -> bool" in hints
    assert PROBLEM["prompt"] in hints
    assert "GENERAL TESTING BEST PRACTICES" not in task["description"]  # no checklist injection
    assert "Example: has_close_elements([1.0, 2.0, 3.0], 0.5) → False" in task["test_scenarios"]


def test_red_generator_renders_contract(task, manager):
    out = manager.get_prompt("code/python_generate_tests_simple",
                             use_langchain=False, **gen_kwargs(task))
    assert out is not None
    assert "MANDATORY: Canonical Examples from Specification" in out
    assert "from solution import" in out
    assert "```python" in out
    assert PROBLEM["prompt"] in out  # full spec reaches the generator
    assert "Reviewer feedback" not in out  # retry block absent on attempt 1


def test_red_generator_retry_blocks_render(task, manager):
    out = manager.get_prompt(
        "code/python_generate_tests_simple", use_langchain=False,
        **gen_kwargs(task, judge_feedback="FIX: use exact example values",
                     previous_test_attempt=TEST_CODE))
    assert "FIX: use exact example values" in out
    assert TEST_CODE.strip() in out


def test_red_judge_renders_contract(task, manager):
    out = manager.get_prompt("judge/test_quality", use_langchain=False,
                             test_code=TEST_CODE, task=task, story=None)
    assert out is not None
    assert "MANDATORY Canonical Example Coverage" in out
    assert TEST_CODE.strip() in out
    assert "Final score:" in out  # coordinator's score parser contract


def test_green_generator_renders_contract(task, manager):
    out = manager.get_prompt("code/python_generate_from_tests", use_langchain=False,
                             **gen_kwargs(task), test_code=TEST_CODE,
                             existing_impl_files={}, previous_attempt="")
    assert out is not None
    assert TEST_CODE.strip() in out
    assert '"impl_file_path"' in out and '"content"' in out  # JSON contract
    assert "```json" in out


def test_green_judge_renders_contract(task, manager):
    out = manager.get_prompt("judge/code_against_tests", use_langchain=False,
                             task=task, test_code=TEST_CODE, impl_code=IMPL_CODE)
    assert out is not None
    assert TEST_CODE.strip() in out
    assert IMPL_CODE.strip() in out
    assert "Rating:" in out  # coordinator's rating parser contract


def test_failure_analysis_renders_contract(task, manager):
    out = manager.get_prompt("judge/failure_analysis", use_langchain=False,
                             task=task, test_code=TEST_CODE, impl_code=IMPL_CODE,
                             test_output="FAILED tests/test_task.py::test_a - AssertionError")
    assert out is not None
    assert TEST_CODE.strip() in out
    assert IMPL_CODE.strip() in out
    assert "AssertionError" in out
    assert "FIX DIRECTIVES:" in out  # the feedback contract GREEN retries consume
    assert "corrected" not in out.lower()  # the analyst analyzes; the generator fixes
