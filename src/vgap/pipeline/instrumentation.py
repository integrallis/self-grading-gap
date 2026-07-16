"""Per-call LLM usage and cost logging.

Registers a litellm CustomLogger that appends one JSONL row per completed LLM call:
timestamp, model, token counts, litellm-computed cost (null when litellm lacks pricing for a
model — those rows are priced later from recorded token counts; never guessed), latency, and
the active call tag (problem id / phase) set by the runner via `set_call_tag`.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import litellm
from litellm.integrations.custom_logger import CustomLogger

_lock = threading.Lock()
_tag: dict[str, str] = {"current": ""}


def set_call_tag(tag: str) -> None:
    """Label subsequent LLM calls (e.g. 'HumanEval/86|run3'). Coarse by design: the pipeline
    is sequential per process, so a process-global tag is accurate."""
    _tag["current"] = tag


class UsageLogger(CustomLogger):
    def __init__(self, out_path: Path):
        super().__init__()
        self.out_path = out_path

    def _write(self, kwargs, response_obj, start_time, end_time) -> None:
        try:
            usage = getattr(response_obj, "usage", None) or {}
            if hasattr(usage, "model_dump"):
                usage = usage.model_dump()
            try:
                cost = litellm.completion_cost(completion_response=response_obj)
            except Exception:
                cost = None
            row = {
                "ts": time.time(),
                "tag": _tag["current"],
                "model": kwargs.get("model"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "cost_usd": cost,
                "latency_s": round((end_time - start_time).total_seconds(), 3)
                if hasattr(end_time - start_time, "total_seconds") else None,
            }
            with _lock, self.out_path.open("a") as f:
                f.write(json.dumps(row) + "\n")
        except Exception as e:  # instrumentation must never kill a run — but never silently
            with _lock, self.out_path.open("a") as f:
                f.write(json.dumps({"ts": time.time(), "instrumentation_error": str(e)}) + "\n")

    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._write(kwargs, response_obj, start_time, end_time)

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        self._write(kwargs, response_obj, start_time, end_time)


_active_logger: UsageLogger | None = None


def register_usage_logger(out_path: Path) -> UsageLogger:
    """Idempotent per process: repeated registration RETARGETS the existing
    logger instead of stacking callbacks — litellm keeps dispatching to the first registered
    callback, so stacked loggers silently wrote every run's rows into the first run's file.
    Rows carry the call tag, so attribution in mixed files is recoverable by tag."""
    global _active_logger
    if _active_logger is not None:
        _active_logger.out_path = out_path
        return _active_logger
    _active_logger = UsageLogger(out_path)
    litellm.callbacks = list(getattr(litellm, "callbacks", []) or []) + [_active_logger]
    return _active_logger


def summarize_usage(usage_jsonl: Path) -> dict:
    """Aggregate a usage log: totals overall and per model; count unpriced calls."""
    totals = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0, "cost_usd": 0.0,
              "unpriced_calls": 0, "errors": 0}
    per_model: dict[str, dict] = {}
    for line in usage_jsonl.read_text().splitlines():
        row = json.loads(line)
        if "instrumentation_error" in row:
            totals["errors"] += 1
            continue
        m = per_model.setdefault(row.get("model") or "unknown",
                                 {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0,
                                  "cost_usd": 0.0, "unpriced_calls": 0})
        for agg in (totals, m):
            agg["calls"] += 1
            agg["prompt_tokens"] += row.get("prompt_tokens") or 0
            agg["completion_tokens"] += row.get("completion_tokens") or 0
            if row.get("cost_usd") is None:
                agg["unpriced_calls"] += 1
            else:
                agg["cost_usd"] += row["cost_usd"]
    return {"totals": totals, "per_model": per_model}
