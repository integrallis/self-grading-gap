"""Unit tests for usage logging aggregation (no LLM calls)."""

import json

from vgap.pipeline.instrumentation import set_call_tag, summarize_usage


def test_summarize_usage(tmp_path):
    p = tmp_path / "usage.jsonl"
    rows = [
        {"ts": 1, "tag": "HumanEval/0|run1", "model": "gpt-4o-mini",
         "prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150,
         "cost_usd": 0.001, "latency_s": 1.0},
        {"ts": 2, "tag": "HumanEval/0|run1", "model": "gpt-4o-mini",
         "prompt_tokens": 200, "completion_tokens": 100, "total_tokens": 300,
         "cost_usd": 0.002, "latency_s": 2.0},
        {"ts": 3, "tag": "HumanEval/1|run1", "model": "brand-new-model",
         "prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15,
         "cost_usd": None, "latency_s": 0.5},
        {"ts": 4, "instrumentation_error": "boom"},
    ]
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    s = summarize_usage(p)
    assert s["totals"]["calls"] == 3
    assert s["totals"]["prompt_tokens"] == 310
    assert s["totals"]["completion_tokens"] == 155
    assert round(s["totals"]["cost_usd"], 6) == 0.003
    assert s["totals"]["unpriced_calls"] == 1  # unknown model priced later, never guessed
    assert s["totals"]["errors"] == 1
    assert s["per_model"]["gpt-4o-mini"]["calls"] == 2
    assert s["per_model"]["brand-new-model"]["unpriced_calls"] == 1


def test_set_call_tag_is_process_global():
    set_call_tag("HumanEval/42|run2")
    from vgap.pipeline.instrumentation import _tag
    assert _tag["current"] == "HumanEval/42|run2"
