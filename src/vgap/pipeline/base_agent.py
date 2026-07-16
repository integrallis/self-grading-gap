"""Minimal base agent: holds the LLM and, when a judge LLM is provided, a
JudgeEvaluator(judge_llm, temperature=0.0); otherwise judge=None and judge gates are skipped.
Subgraph nodes call agent methods from closures; agents are not graph nodes."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel

from vgap.pipeline.judge import JudgeEvaluator


class BaseMaestroAgent:
    def __init__(
        self,
        llm: BaseChatModel,
        name: str,
        judge_llm: BaseChatModel | None = None,
        uncertainty_threshold: float = 0.7,
        **kwargs: Any,
    ):
        self.llm = llm
        self.name = name
        self.uncertainty_threshold = uncertainty_threshold

        if judge_llm:
            self.judge: JudgeEvaluator | None = JudgeEvaluator(judge_llm, temperature=0.0)
        else:
            self.judge = None
