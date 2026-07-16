"""TDD coordinator: the three judge methods and agent handles the subgraph orchestrates.

Every judge verdict derives from the parsed score against the configured judge_threshold.
Each judge call constructs a fresh MaestroPromptManager so per-problem prompt logs number
from zero. Failure analysis returns feedback text only — the generator, not the judge,
produces code."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_litellm import ChatLiteLLM

from vgap.pipeline import judge as judge_mod
from vgap.pipeline.base_agent import BaseMaestroAgent
from vgap.pipeline.prompts import MaestroPromptManager, content_to_text
from vgap.pipeline.python_agent import PythonAgent

logger = logging.getLogger(__name__)


class TDDCoordinatorAgent(BaseMaestroAgent):
    def __init__(
        self,
        llm: BaseChatModel,
        name: str = "tdd_coordinator",
        judge_llm: BaseChatModel | None = None,
        test_llm: BaseChatModel | None = None,
        escalation_llm: BaseChatModel | None = None,
        max_retries: int = 2,
        judge_threshold: float = 0.7,
        test_prompt_template: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(llm, name=name, judge_llm=judge_llm, **kwargs)
        self.judge_for_failure_analysis = judge_llm or llm
        self.test_llm = test_llm or llm
        self.escalation_llm = escalation_llm or ChatLiteLLM(
            model="gpt-5", temperature=1.0
        )
        self.python_agent = PythonAgent(llm=llm)
        self.test_agent = PythonAgent(
            llm=self.test_llm,
            test_prompt_template=test_prompt_template
            or "code/python_generate_tests_simple",
        )
        self.max_retries = max_retries
        self.judge_threshold = judge_threshold

    def _collect_existing_test_files(self, workspace: Path) -> dict[str, str]:
        test_dir = workspace / "tests"
        if not test_dir.exists():
            return {}

        test_files = {}
        for test_file in test_dir.glob("test_*.py"):
            rel_path = str(test_file.relative_to(workspace))
            test_files[rel_path] = test_file.read_text()
        return test_files

    def _collect_existing_impl_files(
        self, workspace: Path, project_name: str
    ) -> dict[str, str]:
        package_name = project_name.replace("-", "_")
        src_dir = workspace / "src" / package_name
        if not src_dir.exists():
            return {}

        impl_files = {}
        for impl_file in src_dir.glob("*.py"):
            rel_path = str(impl_file.relative_to(workspace))
            impl_files[rel_path] = impl_file.read_text()
        return impl_files

    def _parse_json_response(self, response: str) -> dict:
        json_match = re.search(r"```json\s*\n(.*?)\n```", response, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                raise ValueError(f"No JSON found in response: {response[:200]}...")

        return json.loads(json_str)

    async def _judge_test_quality(
        self, test_code: str, task: dict, task_context: dict
    ) -> Any:
        if not self.judge:
            return judge_mod.EvaluationResult(
                score=1.0, passed=True, feedback="No judge configured", details={}
            )

        prompt_manager = MaestroPromptManager()

        prompt = prompt_manager.get_prompt(
            "judge/test_quality",
            use_langchain=False,
            test_code=test_code,
            task=task,
            story=task_context.get("story"),
        )

        messages = [
            SystemMessage(
                content="You are an expert test quality evaluator for TDD workflows."
            ),
            HumanMessage(content=prompt),
        ]

        response = await self.judge.judge_llm.ainvoke(messages)

        if prompt_manager:
            prompt_manager.log_llm_response(response)

        score = self.judge._extract_score(content_to_text(response.content))
        # Verdict derives from the parsed score against the threshold.
        passed = score >= self.judge.threshold

        return judge_mod.EvaluationResult(
            score=score,
            passed=passed,
            feedback=content_to_text(response.content),
            details={"raw_response": content_to_text(response.content)},
        )

    async def _judge_code_quality(
        self, test_code: str, impl_code: str, task: dict, task_context: dict
    ) -> Any:
        if not self.judge:
            return judge_mod.EvaluationResult(
                score=1.0, passed=True, feedback="No judge configured", details={}
            )

        prompt_manager = MaestroPromptManager()

        prompt = prompt_manager.get_prompt(
            "judge/code_against_tests",
            use_langchain=False,
            test_code=test_code,
            impl_code=impl_code,
            task=task,
            recent_commits=task_context.get("recent_commits", []),
        )

        system_message = SystemMessage(
            content="""You are predicting whether tests will PASS or FAIL.

Your ONLY job is to:
1. Trace through code with test inputs
2. Predict PASS/FAIL for EACH test
3. Give a quality rating (0.0-1.0) based on predicted pass rate

You are NOT evaluating:
- Code quality, readability, or style
- Security, performance, or best practices
- Maintainability or design patterns

ONLY test outcomes matter. Ugly code that passes tests = HIGH rating (1.0). Beautiful code that fails tests = LOW rating (0.0)."""
        )

        response = await self.judge.judge_llm.ainvoke(
            [system_message, HumanMessage(content=prompt)]
        )

        if prompt_manager:
            prompt_manager.log_llm_response(response)

        # Last occurrence of the highest-priority pattern; (1,10]->/10,
        # (10,100]->/100, >100 unparseable -> 0.0 (fail-closed).
        rating = 0.0
        patterns = [
            r"\*\*rating\*\*[:\s]+([0-9.]+)",
            r"rating[:\s]+([0-9.]+)",
            r"\*\*score\*\*[:\s]+([0-9.]+)",
            r"score[:\s]+([0-9.]+)",
            r"overall[:\s]+([0-9.]+)",
        ]
        text_lower = content_to_text(response.content).lower()
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                raw_value = float(matches[-1])
                if raw_value > 100.0:
                    rating = 0.0
                elif raw_value > 10.0:
                    rating = raw_value / 100.0
                elif raw_value > 1.0:
                    rating = raw_value / 10.0
                else:
                    rating = raw_value
                rating = max(0.0, min(1.0, rating))
                break

        # Verdict derives from the parsed rating against the configured threshold.
        passed = rating >= self.judge_threshold

        return judge_mod.EvaluationResult(
            score=rating,
            passed=passed,
            feedback=content_to_text(response.content),
            details={"raw_response": content_to_text(response.content)},
        )

    async def _judge_test_failures(
        self, test_output: str, test_code: str, impl_code: str, task: dict
    ) -> Any:
        if not self.judge:
            return judge_mod.EvaluationResult(
                score=0.0, passed=False, feedback=test_output, details={}
            )

        prompt_manager = MaestroPromptManager()

        prompt = prompt_manager.get_prompt(
            "judge/failure_analysis",
            use_langchain=False,
            test_output=test_output,
            test_code=test_code,
            impl_code=impl_code,
            task=task,
        )
        if prompt is None:
            raise RuntimeError("failure_analysis template failed to render")

        response = await self.judge_for_failure_analysis.ainvoke(
            [HumanMessage(content=prompt)]
        )
        prompt_manager.log_llm_response(response)
        feedback = content_to_text(response.content)

        return judge_mod.EvaluationResult(
            score=0.0, passed=False, feedback=feedback,
            details={"raw_response": feedback},
        )
