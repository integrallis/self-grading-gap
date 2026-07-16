"""Anchoring-ablation variant tests: overlay loading works and each variant excises exactly
its side's anchoring enforcement. Base-dir render contracts are covered by
test_render_smoke; variants are regenerated from ANCHOR markers by scripts/make_variants.py."""

from pathlib import Path

import pytest

from vgap.pipeline.prompts import TEMPLATES_DIR, MaestroPromptManager

VARIANTS = Path(__file__).parent / "templates_variants"

GEN_MARKER = "MANDATORY: Canonical Examples from Specification"
JUDGE_MARKER = "MANDATORY Canonical Example Coverage"

TASK = {
    "id": "HumanEval/0", "task_id": "HumanEval/0", "title": "t", "description": "d",
    "test_scenarios": ["s"], "implementation_hints": "h", "acceptance_criteria": ["a"],
    "humaneval_metadata": {"full_prompt": "def f(x):\n    \"\"\">>> f(1)\n    2\"\"\"\n",
                            "entry_point": "f", "task_id": "HumanEval/0",
                            "function_signature": "def f(x):"},
}

GEN_KWARGS = dict(task=TASK, epic=None, story=None, use_case=None,
                  existing_implementation="", existing_test_files={}, test_results="",
                  project_name="solution", project_brief="", recent_commits=[],
                  judge_feedback="", previous_test_attempt="", cartridge={},
                  json_error_feedback="")


def render(manager: MaestroPromptManager, agent: str, **kwargs) -> str:
    out = manager.get_prompt(agent, use_langchain=False, **kwargs)
    assert out is not None
    return out


@pytest.mark.parametrize("variant,gen_present,judge_present", [
    (None, True, True),
    ("anchor_none", False, False),
    ("anchor_gen_only", True, False),
    ("anchor_judge_only", False, True),
])
def test_variant_anchoring_sides(variant, gen_present, judge_present):
    dirs = [VARIANTS / variant, TEMPLATES_DIR] if variant else None
    m = MaestroPromptManager(prompt_dir=dirs)
    gen = render(m, "code/python_generate_tests_simple", **GEN_KWARGS)
    judge = render(m, "judge/test_quality", test_code="def test_a(): pass",
                   task=TASK, story=None)
    assert (GEN_MARKER in gen) == gen_present
    assert (JUDGE_MARKER in judge) == judge_present


def test_env_variant_selection(monkeypatch):
    monkeypatch.setenv("VGAP_PROMPT_VARIANT", "anchor_none")
    m = MaestroPromptManager()
    gen = render(m, "code/python_generate_tests_simple", **GEN_KWARGS)
    assert GEN_MARKER not in gen


def test_env_variant_typo_fails_loud(monkeypatch):
    monkeypatch.setenv("VGAP_PROMPT_VARIANT", "anchor_nope")
    with pytest.raises(ValueError, match="refusing"):
        MaestroPromptManager()


def test_overlay_only_shadows_changed_files():
    m = MaestroPromptManager(prompt_dir=[VARIANTS / "anchor_gen_only", TEMPLATES_DIR])
    base = MaestroPromptManager()
    ours = render(m, "code/python_generate_tests_simple", **GEN_KWARGS)
    theirs = render(base, "code/python_generate_tests_simple", **GEN_KWARGS)
    assert ours == theirs  # generator file untouched in this variant


def test_test_agent_identity_when_no_test_llm():
    """With no separate test_llm, RED's test_agent is behaviorally identical to the
    generator agent — same llm object, same test prompt template."""
    from vgap.pipeline.coordinator import TDDCoordinatorAgent

    class FakeLLM:
        model = "fake"

    c = TDDCoordinatorAgent(llm=FakeLLM())
    assert c.test_agent.llm is c.python_agent.llm
    assert c.test_agent.test_prompt_template == c.python_agent.test_prompt_template
