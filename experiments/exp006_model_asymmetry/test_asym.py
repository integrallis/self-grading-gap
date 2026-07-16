"""Unit tests for exp006 helpers (no API, no data)."""

from run_asym import CELLS, FLOORS, PROBLEM_IDS, S, W, _majority, _mcnemar_exact


def test_frozen_cells():
    assert set(CELLS) == {"control_rerun", "strong_testgen", "strong_judge", "strong_both"}
    assert CELLS["control_rerun"] == {"test_model": None, "judge_model": W}
    assert CELLS["strong_testgen"]["test_model"] == S
    assert CELLS["strong_judge"]["judge_model"] == S
    assert CELLS["strong_both"] == {"test_model": S, "judge_model": S}
    assert len(PROBLEM_IDS) == 30


def test_frozen_floors():
    assert FLOORS == {"pass": 4, "fa": 2, "fr": 2, "verdict_error": 3}


def test_stats_helpers():
    assert not _majority([True, False])
    assert _mcnemar_exact(0, 0) == 1.0
    assert _mcnemar_exact(12, 0) < 0.01
