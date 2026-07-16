"""Judge support: the shared result type, the judge LLM handle, and score extraction.
Every judge call site (RED test-quality, GREEN code-vs-tests, failure analysis) renders its
own template and invokes the judge LLM directly through coordinator methods; this module
holds only what those sites share."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from langchain_core.language_models import BaseChatModel


@dataclass
class EvaluationResult:
    score: float
    passed: bool
    feedback: str
    details: dict[str, Any]
    confidence: float = 1.0


class JudgeEvaluator:
    def __init__(
        self,
        judge_llm: BaseChatModel,
        temperature: float = 0.0,
        threshold: float = 0.7,
    ):
        self.judge_llm = judge_llm
        self.temperature = temperature
        self.threshold = threshold

    def _extract_score(self, text: str) -> float:
        """Highest-priority pattern wins, taking the LAST occurrence in the response
        (verdicts come at the end); scale normalization treats values in (1,10] as 0-10 and
        (10,100] as 0-100 ("Score: 85" -> 0.85); anything larger is unparseable -> 0.0
        (fail-closed)."""
        patterns = [
            r"\*\*final\s+score\*\*[:\s]+([0-9]+\.?[0-9]*)\b",
            r"final\s+score[:\s]+([0-9]+\.?[0-9]*)\b",
            r"\*\*average\s+score\*\*[:\s]+([0-9]+\.?[0-9]*)\b",
            r"average\s+score[:\s]+([0-9]+\.?[0-9]*)\b",
            r"\*\*overall\s+score\*\*[:\s]+([0-9]+\.?[0-9]*)\b",
            r"overall\s+score[:\s]+([0-9]+\.?[0-9]*)\b",
            r"score[:\s]+([0-9]+\.?[0-9]*)\b",
            r"([0-9]+\.?[0-9]*)/1\.0",
            r"([0-9]+)/10",
            r"overall[:\s]+([0-9]+\.?[0-9]*)\b",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                score = float(matches[-1])
                if 1.0 < score <= 10.0:
                    score = score / 10.0
                elif 10.0 < score <= 100.0:
                    score = score / 100.0
                elif score > 100.0:
                    return 0.0
                return min(1.0, max(0.0, score))

        return 0.0
