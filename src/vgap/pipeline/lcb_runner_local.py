"""LiveCodeBench TDD runner: the pipeline loop of humaneval_runner on frozen LCB problems.

Differences from humaneval_runner:
- Problems come from a frozen JSON (exp007 problems/lcb30.json) instead of EvalPlus — the
  vgap venv never needs lcb_runner or the HF script dataset.
- NO in-run oracle: LCB's hidden tests live in the harness venv and scoring is a separate
  stage (run_lcb.py --stage score). Result rows carry tdd_success and the stored
  impl_code/test_code; oracle fields are added by the score stage.
Workspace construction, coordinator/subgraph wiring, error handling, instrumentation, and
the summary shape are the same as humaneval_runner."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from langchain_litellm import ChatLiteLLM
from litellm.exceptions import ContentPolicyViolationError

from vgap.pipeline.bootstrap import PythonBootstrapper
from vgap.pipeline.coordinator import TDDCoordinatorAgent
from vgap.pipeline.instrumentation import set_call_tag
from vgap.pipeline.lcb_adapter import create_tdd_task_from_lcb
from vgap.pipeline.state import create_initial_tdd_cycle_state
from vgap.pipeline.subgraph import create_tdd_cycle_subgraph


def read_frozen_problems(problems_file: Path) -> Dict[str, Dict[str, Any]]:
    rows = json.loads(Path(problems_file).read_text())
    return {r["question_id"]: r for r in rows}


async def run_lcb_problem_with_tdd(
    problem: Dict[str, Any],
    generator_llm: ChatLiteLLM,
    judge_llm: ChatLiteLLM | None = None,
    escalation_llm: ChatLiteLLM | None = None,
    test_llm: ChatLiteLLM | None = None,
    max_retries: int = 3,
    judge_threshold: float = 0.7,
) -> Dict[str, Any]:
    task = create_tdd_task_from_lcb(problem)

    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir) / "solution"
        workspace.mkdir(parents=True)

        subprocess.run(["git", "init"], cwd=workspace, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"],
                       cwd=workspace, capture_output=True, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"],
                       cwd=workspace, capture_output=True, check=True)

        bootstrapper = PythonBootstrapper()
        files = bootstrapper.bootstrap(workspace, {
            "project_name": "solution",
            "package_name": "solution",
            "python_version": "3.11",
            "include_tdd_extras": True,
        })
        for file_path, content in files.items():
            full_path = workspace / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        subprocess.run(["git", "add", "."], cwd=workspace, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"],
                       cwd=workspace, capture_output=True, check=True)

        coordinator = TDDCoordinatorAgent(
            llm=generator_llm,
            judge_llm=judge_llm,
            escalation_llm=escalation_llm,
            test_llm=test_llm,
            max_retries=max_retries,
            judge_threshold=judge_threshold,
        )

        tdd_graph = create_tdd_cycle_subgraph(coordinator=coordinator)

        cartridge = {
            "programming_language": "Python",
            "application_type": "Library",
            "frameworks": [],
            "testing_frameworks": ["pytest"],
            "deployment_target": "local",
        }

        project_brief = f"""
LiveCodeBench Problem: {task["id"]}

Function: {task["lcb_metadata"]["fn_name"]}
Signature: {task["lcb_metadata"]["signature"]}

Task: {task["description"]}
"""

        state = create_initial_tdd_cycle_state(
            task=task,
            workspace_path=str(workspace),
            project_name="solution",
            cartridge=cartridge,
            project_brief=project_brief,
            existing_implementation="",
            max_retries=max_retries,
            judge_threshold=judge_threshold,
            git_enabled=False,
            bootstrapped=True,
        )
        state["generator_llm"] = generator_llm

        result = await tdd_graph.ainvoke(state)

        return {
            "problem_id": task["id"],
            "question_id": problem["question_id"],
            "difficulty": problem["difficulty"],
            "tdd_success": bool(result.get("success")),
            "impl_code": result.get("impl_code", ""),
            "test_code": result.get("test_code", ""),
            "error": None if result.get("success") else result.get("failure_reason",
                                                                   "Unknown TDD failure"),
            "red_attempts": result.get("red_attempts", 0),
            "green_attempts": result.get("green_attempts", 0),
            "red_judge_score": result.get("red_judge_score", 0.0),
            "green_judge_score": result.get("green_judge_score", 0.0),
            "phase_log": result.get("phase_log", []),
        }


def _git_sha(repo: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


async def run_lcb_tdd_evaluation(
    problems_file: Path,
    question_ids: List[str],
    config_name: str,
    out_dir: Path,
    generator_model: str = "gpt-4o-mini",
    judge_model: str = "gpt-5",
    escalation_model: str = "gpt-5",
    test_model: str | None = None,
    test_temperature: float | None = None,
    max_retries: int = 3,
    judge_threshold: float = 0.70,
    generator_temperature: float = 0.7,
    judge_temperature: float = 1.0,
    prompt_log_base: Path | None = None,
    run_tag: str = "",
) -> Dict[str, Any]:
    problems = read_frozen_problems(problems_file)
    generator_llm = ChatLiteLLM(model=generator_model, temperature=generator_temperature)
    judge_llm = ChatLiteLLM(model=judge_model, temperature=judge_temperature)
    escalation_llm = ChatLiteLLM(model=escalation_model, temperature=1.0)
    test_llm = (ChatLiteLLM(model=test_model,
                            temperature=(test_temperature if test_temperature is not None
                                         else generator_temperature))
                if test_model else None)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, qid in enumerate(question_ids, 1):
        print(f"[{i}/{len(question_ids)}] LCB/{qid} ...", flush=True)
        set_call_tag(f"LCB/{qid}|{run_tag}")
        if prompt_log_base is not None:
            problem_log_dir = Path(prompt_log_base) / f"LCB-{qid}"
            problem_log_dir.mkdir(parents=True, exist_ok=True)
            os.environ["MAESTRO_PROMPT_LOG_DIR"] = str(problem_log_dir)

        t0 = time.monotonic()
        try:
            result = await run_lcb_problem_with_tdd(
                problem=problems[qid],
                generator_llm=generator_llm,
                judge_llm=judge_llm,
                escalation_llm=escalation_llm,
                test_llm=test_llm,
                max_retries=max_retries,
                judge_threshold=judge_threshold,
            )
        except ContentPolicyViolationError:
            result = {"problem_id": f"LCB/{qid}", "question_id": qid,
                      "difficulty": problems[qid]["difficulty"], "tdd_success": False,
                      "impl_code": "", "test_code": "",
                      "error": "Content Policy Violation",
                      "red_attempts": 0, "green_attempts": 0, "phase_log": []}
        except Exception as e:
            result = {"problem_id": f"LCB/{qid}", "question_id": qid,
                      "difficulty": problems[qid]["difficulty"], "tdd_success": False,
                      "impl_code": "", "test_code": "",
                      "error": f"API Error: {str(e)}",
                      "red_attempts": 0, "green_attempts": 0, "phase_log": []}

        result["wall_time_s"] = round(time.monotonic() - t0, 1)
        results.append(result)
        print(f"    -> tdd_success={result['tdd_success']} ({result['wall_time_s']}s)",
              flush=True)

    total = len(results)
    tdd_success = sum(1 for r in results if r["tdd_success"])

    summary = {
        "configuration": {
            "name": config_name,
            "generator": generator_model,
            "generator_temperature": generator_temperature,
            "judge": judge_model,
            "judge_temperature": judge_temperature,
            "escalation": escalation_model,
            "test_model": test_model,
            "test_temperature": test_temperature,
            "max_retries": max_retries,
            "judge_threshold": judge_threshold,
            "run_tag": run_tag,
        },
        "provenance": {
            "vgap_git_sha": _git_sha(Path(__file__).resolve().parents[3]),
            "python": sys.version.split()[0],
            "problems_file": str(problems_file),
        },
        "summary": {
            "total_problems": total,
            "tdd_succeeded": tdd_success,
            "tdd_success_rate": tdd_success / total if total > 0 else 0.0,
        },
        "results": results,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    }

    result_file = out_dir / (
        f"lcb_tdd_{config_name}_{len(question_ids)}p_{summary['timestamp']}.json"
    )
    result_file.write_text(json.dumps(summary, indent=2))

    print(f"\nTDD Success: {tdd_success}/{total} "
          f"({summary['summary']['tdd_success_rate']:.1%}) — oracle scoring is a separate stage")
    print(f"Results saved to: {result_file}")

    return summary
