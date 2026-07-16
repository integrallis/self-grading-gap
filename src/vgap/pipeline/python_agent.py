"""Python code/test generation agent: _generate_tests (RED) and
_generate_from_tests_with_context (GREEN).

Both methods render their template, invoke the LLM, log prompt and response, and extract
code from the first ```python fence (else the first ``` fence) — code is requested as
markdown, never as JSON-wrapped strings. _generate_tests returns a dict with
test_file_path (derived as tests/test_<task_id>.py) and content."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage

from vgap.pipeline.base_agent import BaseMaestroAgent
from vgap.pipeline.prompts import MaestroPromptManager, content_to_text


class PythonAgent(BaseMaestroAgent):
    def __init__(
        self,
        llm: BaseChatModel,
        name: str = "python_agent",
        prompt_template: str | None = None,
        test_prompt_template: str | None = None,
        **kwargs: Any,
    ):
        super().__init__(llm=llm, name=name, judge_llm=None, **kwargs)
        self.prompt_manager = MaestroPromptManager()
        self.prompt_template = prompt_template or "code/python_generate_from_tests"
        self.test_prompt_template = (
            test_prompt_template or "code/python_generate_tests_simple"
        )

    async def _generate_tests(
        self, task: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            prompt = self.prompt_manager.get_prompt(
                self.test_prompt_template,
                use_langchain=False,
                task=task,
                epic=context.get("epic"),
                story=context.get("story"),
                use_case=context.get("use_case"),
                existing_implementation=context.get("existing_implementation", ""),
                existing_test_files=context.get("existing_test_files", {}),
                test_results=context.get("test_results", ""),
                project_name=context.get("project_name", ""),
                project_brief=context.get("project_brief", ""),
                recent_commits=context.get("recent_commits", []),
                judge_feedback=context.get("judge_feedback", ""),
                previous_test_attempt=context.get("previous_test_attempt", ""),
                cartridge=context.get("cartridge", {}),
                json_error_feedback=context.get("json_error_feedback", ""),
            )
        except Exception as e:
            raise ValueError(f"Failed to load test generation prompt: {e}") from e

        if not prompt:
            raise ValueError(
                f"Test generation prompt returned None. Config keys: {list(self.prompt_manager.config.get('agents', {}).keys())}"
            )

        messages = [HumanMessage(content=prompt)]
        response = await self.llm.ainvoke(messages)
        code = content_to_text(response.content)

        self.prompt_manager.log_llm_response(response)

        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]

        return {
            "test_file_path": f"tests/test_{task.get('task_id', 'task').lower().replace('-', '_').replace('/', '_')}.py",
            "action": "create",
            "content": code.strip(),
            "reasoning": "Generated pytest tests for TDD RED phase",
        }

    async def _generate_from_tests_with_context(self, context: dict[str, Any]) -> str:
        prompt = self.prompt_manager.get_prompt(
            "code/python_generate_from_tests",
            use_langchain=False,
            task=context.get("task", {}),
            test_code=context.get("test_code", ""),
            existing_impl_files=context.get("existing_impl_files", {}),
            existing_implementation=context.get("existing_implementation", ""),
            project_name=context.get("project_name", ""),
            project_brief=context.get("project_brief", ""),
            recent_commits=context.get("recent_commits", []),
            judge_feedback=context.get("judge_feedback", ""),
            previous_attempt=context.get("previous_attempt", ""),
            rag_patterns=context.get("rag_patterns", ""),
            json_error_feedback=context.get("json_error_feedback", ""),
        )

        if not prompt:
            raise ValueError("Failed to load code generation prompt")

        messages = [{"role": "user", "content": prompt}]
        response = await self.llm.ainvoke(messages)

        self.prompt_manager.log_llm_response(response)

        return content_to_text(response.content)
