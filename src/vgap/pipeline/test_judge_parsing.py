"""Unit tests for judge verdict parsing and error-handling edge cases."""

from vgap.pipeline.judge import JudgeEvaluator


class FakeLLM:
    model = "fake"


def _judge():
    return JudgeEvaluator(FakeLLM())


def test_b4_score_85_is_085_not_10():
    assert _judge()._extract_score("Final Score: 85") == 0.85


def test_b4_scale_normalization():
    j = _judge()
    assert j._extract_score("score: 0.7") == 0.7
    assert j._extract_score("score: 8") == 0.8
    assert j._extract_score("score: 8/10") == 0.8
    assert j._extract_score("score: 100000") == 0.0  # unparseable scale -> fail-closed
    assert j._extract_score("no numbers here") == 0.0


def test_b4_last_match_wins():
    text = "Per-test analysis... score: 0.2 (partial)\n\nFinal verdict\nscore: 0.9"
    assert _judge()._extract_score(text) == 0.9


def test_b4_priority_pattern_beats_generic():
    text = "score: 0.2 somewhere early\n**Final score**: 0.8"
    assert _judge()._extract_score(text) == 0.8


def test_b2_timeout_is_failing_result(tmp_path, monkeypatch):
    import subprocess as sp

    from vgap.pipeline import pytest_runner

    def boom(*a, **k):
        raise sp.TimeoutExpired(cmd="pytest", timeout=30)

    monkeypatch.setattr(pytest_runner.subprocess, "run", boom)
    r = pytest_runner.run_tests(tmp_path)
    assert not r.all_passed and r.exit_code == -1 and "TIMEOUT" in r.output


def test_b1_render_failure_raises():
    import pytest

    from vgap.pipeline.prompts import MaestroPromptManager

    m = MaestroPromptManager()
    with pytest.raises(RuntimeError, match="render failed"):
        # undefined-attribute access inside the template on a non-dict task
        m.get_prompt("judge/test_quality", use_langchain=False,
                     test_code="x", task=object(), story=None)
