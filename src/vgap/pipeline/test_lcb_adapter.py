"""Unit tests for the LCB adapter: signature derivation, task shape, anchor activation,
oracle isolation (no private tests anywhere in the task), and end-to-end template rendering."""

import json
from pathlib import Path

import pytest

from vgap.pipeline.lcb_adapter import create_tdd_task_from_lcb, derive_signature
from vgap.pipeline.prompts import MaestroPromptManager

PROBLEM = {
    "question_id": "3702",
    "question_title": "Maximum Length",
    "difficulty": "easy",
    "contest_date": "2025-01-04T00:00:00",
    "fn_name": "maxLength",
    "starter_code": "class Solution:\n    def maxLength(self, nums: List[int]) -> int:\n        ",
    "question_content": "Given an array nums... Example 1: Input: nums = [1,2,1,2,1,1,1] Output: 5",
    "public_examples": [{"input": "[1, 2, 1, 2, 1, 1, 1]", "output": "5"}],
    "n_private_tests": 40,
}


def test_derive_signature_strips_class_and_self():
    assert derive_signature(PROBLEM["starter_code"], "maxLength") == \
        "def maxLength(nums: List[int]) -> int"


def test_derive_signature_no_annotations():
    assert derive_signature("class Solution:\n    def f(self, a, b):\n", "f") == "def f(a, b)"


def test_derive_signature_missing_fn_raises():
    with pytest.raises(ValueError):
        derive_signature("class Solution:\n    def other(self):\n", "maxLength")


def test_task_shape_and_anchor_flag():
    task = create_tdd_task_from_lcb(PROBLEM)
    assert task["id"] == "LCB/3702"
    assert task["specification_with_examples"] is True
    assert "def maxLength(nums: List[int]) -> int" in task["description"]
    assert "class solution" not in task["implementation_hints"].split("Full problem statement")[0].lower()
    assert task["lcb_metadata"]["fn_name"] == "maxLength"


def test_no_private_oracle_content_in_task():
    task = create_tdd_task_from_lcb(PROBLEM)
    assert "n_private_tests" not in json.dumps(task)


def test_templates_render_with_lcb_task():
    task = create_tdd_task_from_lcb(PROBLEM)
    m = MaestroPromptManager()
    kw = dict(task=task, epic=None, story=None, use_case=None,
              existing_implementation="", existing_test_files={}, test_results="",
              project_name="solution", project_brief="", recent_commits=[],
              judge_feedback="", previous_test_attempt="", cartridge={},
              json_error_feedback="")
    gen = m.get_prompt("code/python_generate_tests_simple", use_langchain=False, **kw)
    assert gen is not None
    assert "MANDATORY: Canonical Examples from Specification" in gen  # anchor fires
    assert PROBLEM["question_content"] in gen
    judge = m.get_prompt("judge/test_quality", use_langchain=False,
                         test_code="def test_a(): pass", task=task, story=None)
    assert judge is not None
    assert "MANDATORY Canonical Example Coverage" in judge


def test_frozen_problem_set_is_30():
    f = Path(__file__).resolve().parents[3] / \
        "experiments/exp007_lcb_asymmetry/problems/lcb30.json"
    rows = json.loads(f.read_text())
    assert len(rows) == 30
    assert sum(1 for r in rows if r["difficulty"] == "easy") == 19
    assert sum(1 for r in rows if r["difficulty"] == "medium") == 11
    assert all(r["fn_name"] and r["starter_code"] and r["question_content"] for r in rows)
