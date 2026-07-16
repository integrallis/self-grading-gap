"""TDD RED-GREEN-VERIFY subgraph: nodes, routing, and graph wiring.

Load-bearing behaviors:
- Execution-gated GREEN: judge approval triggers a pytest run of the whole suite; a failure
  overrides the judge, injects failure-analysis feedback, increments
  execution_validation_failures, and retries.
- Escalation: attempt >= escalation_threshold OR execution_validation_failures >= 2 swaps in a
  fresh PythonAgent on coordinator.escalation_llm (generation only — judges keep their LLM;
  experiments disable escalation by pinning the escalation model to the generator).
- Feedback travels as text: VERIFY persists only the failure analysis into state, so a failed
  cycle's next GREEN attempt sees feedback inside its prompt, never judge-written code.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Literal

from langgraph.graph import END, START, StateGraph

from vgap.pipeline.python_agent import PythonAgent
from vgap.pipeline.state import TDDCycleState
from vgap.pipeline.pytest_runner import run_tests

logger = logging.getLogger(__name__)


async def red_phase_node(state: TDDCycleState, coordinator: Any) -> dict:
    task_id = state["task"].get("id", "UNKNOWN")
    attempt = state["red_attempts"] + 1

    log_entry = f"🔴 → RED Phase (attempt {attempt}) - Task {task_id}"
    logger.info(log_entry)
    phase_log = state.get("phase_log", []).copy()
    phase_log.append(log_entry)
    task = state["task"]
    workspace_path = Path(state["workspace_path"])
    project_name = state["project_name"]

    existing_test_files = coordinator._collect_existing_test_files(workspace_path)
    existing_impl_files = coordinator._collect_existing_impl_files(
        workspace_path, project_name
    )

    task_context = {
        "existing_test_files": existing_test_files,
        "existing_impl_files": existing_impl_files,
        "project_brief": state.get("project_brief", ""),
        "existing_implementation": state.get("existing_implementation", ""),
        "recent_commits": state.get("recent_commits", []),
        "project_name": project_name,
        "cartridge": state["cartridge"],
    }

    if attempt > 1 and state.get("judge_feedback"):
        task_context["judge_feedback"] = state["judge_feedback"]
        if state.get("test_code"):
            task_context["previous_test_attempt"] = state["test_code"]

    max_json_retries = 3
    test_code = None
    test_file_path = None

    for json_retry in range(max_json_retries):
        # RED routes through test_agent: with no separate test_llm configured it wraps
        # the same llm and template as the generator (identity); with test_llm set it is
        # the model-asymmetry knob.
        test_info = await coordinator.test_agent._generate_tests(task, task_context)

        try:
            test_code = test_info["content"]
            test_file_path = test_info["test_file_path"]

            log_entry = f"🔴   Generated {len(test_code)} chars → {test_file_path}"
            logger.info(log_entry)
            phase_log.append(log_entry)
            break

        except KeyError as e:
            if json_retry < max_json_retries - 1:
                logger.warning(
                    f"Dict structure invalid (attempt {json_retry + 1}/{max_json_retries}): {e}. "
                    f"Retrying..."
                )

                error_feedback = (
                    f"\n\n{'='*80}\n"
                    f"❌ DICT STRUCTURE ERROR - RETRY ATTEMPT {json_retry + 1}/{max_json_retries - 1}\n"
                    f"{'='*80}\n\n"
                    f"Your previous response was missing a required key:\n"
                    f"ERROR: {str(e)}\n\n"
                    f"Dict had keys: {list(test_info.keys())}\n\n"
                    f"Please regenerate VALID JSON, fixing the error mentioned above.\n"
                    f"Expected format:\n"
                    f"{{\n"
                    f'  "test_file_path": "tests/test_module.py",\n'
                    f'  "content": "# Python test code here"\n'
                    f"}}\n\n"
                    f"Pay special attention to:\n"
                    f"- Proper commas between all fields\n"
                    f"- Matching quotes (no unescaped quotes in strings)\n"
                    f"- Proper bracket/brace matching\n"
                    f"- Valid escape sequences in strings\n"
                    f"{'='*80}\n"
                )

                task_context["json_error_feedback"] = error_feedback
            else:
                logger.warning(
                    f"JSON parsing failed after {max_json_retries} attempts. "
                    f"Using fallback: treating entire response as test code."
                )
                # Fall back to whatever content the dict carries.
                test_code = test_info.get("content", "")
                test_file_path = f"tests/test_{task_id.lower().replace('-', '_')}.py"

    if coordinator.judge and attempt <= state.get("max_retries", 3):
        test_quality = await coordinator._judge_test_quality(
            test_code=test_code, task=task, task_context=task_context
        )
        judge_score = test_quality.score
        judge_feedback = test_quality.feedback

        log_entry = f"🔴   Judge score: {judge_score:.2f} (threshold: {state.get('judge_threshold', 0.7):.2f})"
        logger.info(log_entry)
        phase_log.append(log_entry)
    else:
        judge_score = 1.0
        judge_feedback = ""

    test_file_full_path = workspace_path / test_file_path
    test_file_full_path.parent.mkdir(parents=True, exist_ok=True)
    test_file_full_path.write_text(test_code, encoding="utf-8")

    log_entry = f"🔴   Wrote test file → {test_file_path}"
    logger.info(log_entry)
    phase_log.append(log_entry)

    log_exit = (
        f"🔴 ← RED Phase: Generated {len(test_code)} chars, judge={judge_score:.2f}"
    )
    logger.info(log_exit)
    phase_log.append(log_exit)

    return {
        **state,
        "test_code": test_code,
        "test_file_path": test_file_path,
        "red_judge_score": judge_score,
        "judge_feedback": judge_feedback,
        "red_attempts": attempt,
        "phase_log": phase_log,
    }


async def green_phase_node(state: TDDCycleState, coordinator: Any) -> dict:
    task_id = state["task"].get("id", "UNKNOWN")
    attempt = state["green_attempts"] + 1

    log_entry = f"🟢 → GREEN Phase (attempt {attempt}) - Task {task_id}"
    logger.info(log_entry)
    phase_log = state.get("phase_log", []).copy()
    phase_log.append(log_entry)

    task = state["task"]
    test_code = state["test_code"]
    workspace_path = Path(state["workspace_path"])
    project_name = state["project_name"]

    existing_impl_files = coordinator._collect_existing_impl_files(
        workspace_path, project_name
    )

    code_context = {
        "task": task,
        "test_code": test_code,
        "existing_impl_files": existing_impl_files,
        "project_brief": state.get("project_brief", ""),
        "existing_implementation": state.get("existing_implementation", ""),
        "recent_commits": state.get("recent_commits", []),
        "project_name": project_name,
        "cartridge": state.get("cartridge", {}),
    }

    if state.get("judge_feedback"):
        code_context["judge_feedback"] = state["judge_feedback"]
    if attempt > 1:
        if state.get("test_result"):
            test_result_dict = state["test_result"]
            if not test_result_dict.get("all_passed"):
                code_context["test_failures"] = test_result_dict.get("output", "")
        if state.get("impl_code"):
            code_context["previous_attempt"] = state["impl_code"]

    python_agent_to_use = coordinator.python_agent
    escalation_threshold = state.get("escalation_threshold", 3)
    execution_validation_failures = state.get("execution_validation_failures", 0)

    should_escalate = (attempt >= escalation_threshold) or (
        execution_validation_failures >= 2
    )

    if should_escalate:
        escalated_llm = coordinator.escalation_llm
        python_agent_to_use = PythonAgent(llm=escalated_llm)

        escalated_model = getattr(escalated_llm, "model", "unknown")
        log_entry = f"🟢   Using escalated model: {escalated_model}"
        logger.info(log_entry)
        phase_log.append(log_entry)

    max_json_retries = 3
    malformed_response = None
    impl_code = None
    impl_file_path = None

    for json_retry in range(max_json_retries):
        impl_response = await python_agent_to_use._generate_from_tests_with_context(
            code_context
        )

        try:
            impl_info = coordinator._parse_json_response(impl_response)
            impl_code = impl_info["content"]
            impl_file_path = impl_info["impl_file_path"]

            log_entry = f"🟢   Generated {len(impl_code)} chars → {impl_file_path}"
            logger.info(log_entry)
            phase_log.append(log_entry)
            break

        except (ValueError, KeyError) as e:
            malformed_response = impl_response

            if json_retry < max_json_retries - 1:
                logger.warning(
                    f"JSON parsing failed (attempt {json_retry + 1}/{max_json_retries}): {e}. "
                    f"Providing error feedback to LLM for retry..."
                )

                error_feedback = (
                    f"\n\n{'='*80}\n"
                    f"❌ JSON PARSING ERROR - RETRY ATTEMPT {json_retry + 1}/{max_json_retries - 1}\n"
                    f"{'='*80}\n\n"
                    f"Your previous response had a JSON parsing error:\n"
                    f"ERROR: {str(e)}\n\n"
                    f"Your malformed JSON response was:\n"
                    f"```json\n{malformed_response[:500]}\n```\n\n"
                    f"Please regenerate VALID JSON, fixing the error mentioned above.\n"
                    f"Expected format:\n"
                    f"{{\n"
                    f'  "impl_file_path": "src/package_name/module.py",\n'
                    f'  "content": "# Python code here"\n'
                    f"}}\n\n"
                    f"Pay special attention to:\n"
                    f"- Proper commas between all fields\n"
                    f"- Matching quotes (no unescaped quotes in strings)\n"
                    f"- Proper bracket/brace matching\n"
                    f"- Valid escape sequences in strings\n"
                    f"{'='*80}\n"
                )

                code_context["json_error_feedback"] = error_feedback
            else:
                logger.warning(
                    f"JSON parsing failed after {max_json_retries} attempts. "
                    f"Using fallback: treating entire response as implementation."
                )
                impl_code = impl_response
                package_name = state["project_name"].replace("-", "_")
                impl_file_path = f"src/{package_name}/main.py"

    if coordinator.judge and attempt <= state.get("max_retries", 3):
        code_quality = await coordinator._judge_code_quality(
            test_code=test_code,
            impl_code=impl_code,
            task=task,
            task_context=code_context,
        )
        judge_score = code_quality.score
        judge_feedback = code_quality.feedback

        log_entry = f"🟢   Judge score: {judge_score:.2f} (threshold: {state.get('judge_threshold', 0.7):.2f})"
        logger.info(log_entry)
        phase_log.append(log_entry)
    else:
        judge_score = 1.0
        judge_feedback = ""

    if judge_score >= state.get("judge_threshold", 0.7) and coordinator.judge:
        impl_file_full_path = workspace_path / impl_file_path
        impl_file_full_path.parent.mkdir(parents=True, exist_ok=True)
        impl_file_full_path.write_text(impl_code, encoding="utf-8")

        # The gate runs the whole suite, matching VERIFY (identical for
        # single-task HumanEval runs; consistent for multi-task use).
        test_result = run_tests(workspace_path)

        if not test_result.all_passed:
            log_entry = f"🟢   ⚠️  Execution validation FAILED: Tests fail despite judge={judge_score:.2f}"
            logger.warning(log_entry)
            phase_log.append(log_entry)

            failed_test_names = []
            for line in test_result.output.split("\n"):
                if "FAILED" in line and "::" in line:
                    test_name = (
                        line.split("::")[-1].split(" ")[0]
                        if "::" in line
                        else line.split(" ")[0]
                    )
                    failed_test_names.append(test_name)

            failed_tests_info = (
                "\n".join([f"  - {t}" for t in failed_test_names])
                if failed_test_names
                else "  (see output below)"
            )

            execution_feedback = None
            if coordinator.judge:
                try:
                    # Same failure-analysis template as VERIFY — one analysis path.
                    failure_analysis = await coordinator._judge_test_failures(
                        test_output=test_result.output[:4000],
                        test_code=test_code,
                        impl_code=impl_code,
                        task=state["task"],
                    )

                    execution_feedback = (
                        f"EXECUTION VALIDATION FAILED\n"
                        f"\n"
                        f"Judge gave score {judge_score:.2f}, but tests FAIL when actually run.\n"
                        f"\n"
                        f"Failed tests:\n"
                        f"{failed_tests_info}\n"
                        f"\n"
                        f"=== FAILURE ANALYSIS ===\n"
                        f"{failure_analysis.feedback}\n"
                    )

                except Exception as e:
                    error_type = type(e).__name__
                    error_msg = str(e) or repr(e)
                    logger.warning(
                        f"🟢   Judge analysis failed ({error_type}): {error_msg}, falling back to basic feedback"
                    )

            if not execution_feedback:
                execution_feedback = (
                    f"EXECUTION VALIDATION FAILED: Implementation fails tests!\n"
                    f"\n"
                    f"The judge gave a score of {judge_score:.2f}, but the implementation FAILS when tests are actually run.\n"
                    f"\n"
                    f"Failed tests:\n"
                    f"{failed_tests_info}\n"
                    f"\n"
                    f"Test output (first 1000 chars):\n"
                    f"{test_result.output[:1000]}\n"
                    f"\n"
                    f"YOUR TASK: Fix the implementation to actually pass ALL tests.\n"
                    f"Focus on the specific test failures shown above."
                )

            execution_validation_failures_new = (
                state.get("execution_validation_failures", 0) + 1
            )

            return {
                **state,
                "impl_code": impl_code,
                "impl_file_path": impl_file_path,
                "green_judge_score": judge_score,
                "green_attempts": state.get("green_attempts", 0) + 1,
                "judge_feedback": execution_feedback,
                "test_result": {
                    "all_passed": False,
                    "failed_tests": test_result.failed_tests,
                    "output": test_result.output,
                },
                "phase_log": phase_log,
                "execution_validation_failed": True,
                "execution_validation_failures": execution_validation_failures_new,
            }
        else:
            log_entry = "🟢   ✓ Execution validation PASSED: All tests pass"
            logger.info(log_entry)
            phase_log.append(log_entry)
    else:
        impl_file_full_path = workspace_path / impl_file_path
        impl_file_full_path.parent.mkdir(parents=True, exist_ok=True)
        impl_file_full_path.write_text(impl_code, encoding="utf-8")

    log_entry = f"🟢   Wrote impl file → {impl_file_path}"
    logger.info(log_entry)
    phase_log.append(log_entry)

    log_exit = (
        f"🟢 ← GREEN Phase: Generated {len(impl_code)} chars, judge={judge_score:.2f}"
    )
    logger.info(log_exit)
    phase_log.append(log_exit)

    return {
        **state,
        "impl_code": impl_code,
        "impl_file_path": impl_file_path,
        "green_judge_score": judge_score,
        "judge_feedback": judge_feedback,
        "green_attempts": attempt,
        "phase_log": phase_log,
        "execution_validation_failed": False,
    }


async def verify_phase_node(state: TDDCycleState, coordinator: Any) -> dict:
    task_id = state["task"].get("id", "UNKNOWN")
    attempt = state["verify_attempts"] + 1

    log_entry = f"✅ → VERIFY Phase (attempt {attempt}) - Task {task_id}"
    logger.info(log_entry)
    phase_log = state.get("phase_log", []).copy()
    phase_log.append(log_entry)

    workspace_path = Path(state["workspace_path"])

    test_result = run_tests(workspace_path)

    test_result_dict = {
        "all_passed": test_result.all_passed,
        "output": test_result.output,
        "failed_tests": test_result.failed_tests,
    }

    log_entry = f"✅   Tests {'PASSED' if test_result.all_passed else 'FAILED'}"
    if not test_result.all_passed:
        log_entry += f" - {len(test_result.failed_tests)} failures"
    logger.info(log_entry)
    phase_log.append(log_entry)

    judge_feedback = ""
    if not test_result.all_passed:
        if coordinator and coordinator.judge:
            failure_analysis = await coordinator._judge_test_failures(
                test_output=test_result.output,
                test_code=state["test_code"],
                impl_code=state["impl_code"],
                task=state["task"],
            )
            judge_feedback = failure_analysis.feedback

    log_exit = f"✅ ← VERIFY Phase: {'PASSED' if test_result.all_passed else 'FAILED'}"
    logger.info(log_exit)
    phase_log.append(log_exit)

    return {
        **state,
        "test_result": test_result_dict,
        "judge_feedback": judge_feedback,
        "verify_attempts": attempt,
        "phase_log": phase_log,
    }


def route_after_red(
    state: TDDCycleState,
) -> Literal["green", "retry_red", "failed"]:
    score = state.get("red_judge_score", 0.0)
    threshold = state.get("judge_threshold", 0.7)
    attempts = state.get("red_attempts", 0)
    max_retries = state.get("max_retries", 3)

    if score >= threshold:
        return "green"
    elif attempts < max_retries:
        return "retry_red"
    else:
        return "failed"


def route_after_green(
    state: TDDCycleState,
) -> Literal["verify", "retry_green", "failed"]:
    score = state.get("green_judge_score", 0.0)
    threshold = state.get("judge_threshold", 0.7)
    attempts = state.get("green_attempts", 0)
    max_retries = state.get("max_retries", 3)
    execution_validation_failed = state.get("execution_validation_failed", False)

    if execution_validation_failed:
        if attempts < max_retries:
            return "retry_green"
        else:
            return "failed"
    elif score >= threshold:
        return "verify"
    elif attempts < max_retries:
        return "retry_green"
    else:
        return "failed"


def route_after_verify(
    state: TDDCycleState,
) -> Literal["complete", "retry_green", "failed"]:
    test_result = state.get("test_result", {})
    all_passed = test_result.get("all_passed", False)
    attempts = state.get("verify_attempts", 0)
    max_retries = state.get("max_retries", 3)

    if all_passed:
        return "complete"
    elif attempts < max_retries:
        return "retry_green"
    else:
        return "failed"


def complete_node(state: TDDCycleState) -> dict:
    task_id = state["task"].get("id", "UNKNOWN")
    phase_log = state.get("phase_log", []).copy()
    phase_log.append(f"✅ Task {task_id} COMPLETE")

    return {
        **state,
        "tdd_phase": "COMPLETE",
        "success": True,
        "phase_log": phase_log,
    }


def failed_node(state: TDDCycleState) -> dict:
    task_id = state["task"].get("id", "UNKNOWN")
    phase_log = state.get("phase_log", []).copy()
    phase_log.append(f"❌ Task {task_id} FAILED")

    return {
        **state,
        "tdd_phase": "FAILED",
        "success": False,
        "failure_reason": "Max retries exceeded",
        "phase_log": phase_log,
    }


def create_tdd_cycle_subgraph(coordinator: Any) -> StateGraph:
    workflow = StateGraph(TDDCycleState)

    async def _red_phase_with_coordinator(state: TDDCycleState) -> dict:
        return await red_phase_node(state, coordinator)

    async def _green_phase_with_coordinator(state: TDDCycleState) -> dict:
        return await green_phase_node(state, coordinator)

    async def _verify_phase_with_coordinator(state: TDDCycleState) -> dict:
        return await verify_phase_node(state, coordinator)

    workflow.add_node("red", _red_phase_with_coordinator)
    workflow.add_node("green", _green_phase_with_coordinator)
    workflow.add_node("verify", _verify_phase_with_coordinator)
    workflow.add_node("complete", complete_node)
    workflow.add_node("failed", failed_node)

    workflow.add_edge(START, "red")

    workflow.add_conditional_edges(
        "red",
        route_after_red,
        {
            "green": "green",
            "retry_red": "red",
            "failed": "failed",
        },
    )

    workflow.add_conditional_edges(
        "green",
        route_after_green,
        {
            "verify": "verify",
            "retry_green": "green",
            "failed": "failed",
        },
    )

    workflow.add_conditional_edges(
        "verify",
        route_after_verify,
        {
            "complete": "complete",
            "retry_green": "green",
            "failed": "failed",
        },
    )

    workflow.add_edge("complete", END)
    workflow.add_edge("failed", END)

    return workflow.compile()
