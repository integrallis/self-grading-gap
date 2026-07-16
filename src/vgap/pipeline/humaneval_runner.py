"""HumanEval TDD runner.

Each problem runs the full TDD cycle in a fresh temporary workspace (git-initialized,
bootstrapped `solution` package), then the produced implementation is checked in-run against
the problem's official test via `check(entry_point)` in a subprocess with a 120 s timeout —
so a pathological solution cannot hang the run. Problems come from EvalPlus's mirror of
original HumanEval. Every problem-run is instrumented: per-call usage tags, wall time, and a
per-run machine-readable summary with provenance fields (models, temperatures, thresholds,
git SHA); per-problem prompt logs via MAESTRO_PROMPT_LOG_DIR."""

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
from vgap.pipeline.humaneval_adapter import create_tdd_task_from_humaneval
from vgap.pipeline.instrumentation import set_call_tag
from vgap.pipeline.state import create_initial_tdd_cycle_state
from vgap.pipeline.subgraph import create_tdd_cycle_subgraph

_PROBLEMS_CACHE: Dict[str, Dict[str, Any]] | None = None


def read_problems() -> Dict[str, Dict[str, Any]]:
    """Original HumanEval problems via EvalPlus's mirror."""
    global _PROBLEMS_CACHE
    if _PROBLEMS_CACHE is None:
        from evalplus.data import get_human_eval_plus

        plus = get_human_eval_plus()
        # get_human_eval_plus returns {task_id: problem} with the ORIGINAL prompt/entry_point/
        # canonical_solution and the original "test" preserved per problem.
        _PROBLEMS_CACHE = plus
    return _PROBLEMS_CACHE


def evaluate_single_humaneval(problem_id: str, impl_code: str, timeout_s: int = 120) -> bool:
    """In-run oracle: impl + official test + check(entry_point), in a subprocess."""
    if not impl_code.strip():
        return False
    problems = read_problems()
    problem = problems[problem_id]

    test_code = (
        impl_code + "\n\n" + problem["test"] + f"\n\ncheck({problem['entry_point']})"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(test_code)
        script = f.name
    try:
        proc = subprocess.run(
            [sys.executable, script], capture_output=True, text=True, timeout=timeout_s
        )
        if proc.returncode != 0:
            print(f"HumanEval test failed: {proc.stderr.strip()[-300:]}")
        return proc.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"HumanEval test timed out after {timeout_s}s")
        return False
    finally:
        os.unlink(script)


async def run_humaneval_problem_with_tdd(
    problem_id: str,
    generator_llm: ChatLiteLLM,
    judge_llm: ChatLiteLLM | None = None,
    escalation_llm: ChatLiteLLM | None = None,
    test_llm: ChatLiteLLM | None = None,
    max_retries: int = 3,
    judge_threshold: float = 0.7,
) -> Dict[str, Any]:
    problems = read_problems()
    problem = problems[problem_id]

    task = create_tdd_task_from_humaneval(problem)

    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir) / "solution"
        workspace.mkdir(parents=True)

        subprocess.run(["git", "init"], cwd=workspace, capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=workspace, capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=workspace, capture_output=True, check=True,
        )

        bootstrapper = PythonBootstrapper()
        bootstrap_config = {
            "project_name": "solution",
            "package_name": "solution",
            "python_version": "3.11",
            "include_tdd_extras": True,
        }
        files = bootstrapper.bootstrap(workspace, bootstrap_config)
        for file_path, content in files.items():
            full_path = workspace / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)

        subprocess.run(["git", "add", "."], cwd=workspace, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=workspace, capture_output=True, check=True,
        )

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
HumanEval Problem: {problem_id}

Function: {task['humaneval_metadata']['entry_point']}
Signature: {task['humaneval_metadata']['function_signature']}

Task: {task['description']}
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

        if not result.get("success"):
            return {
                "problem_id": problem_id,
                "tdd_success": False,
                "humaneval_passed": False,
                "impl_code": result.get("impl_code", ""),
                "test_code": result.get("test_code", ""),
                "error": result.get("failure_reason", "Unknown TDD failure"),
                "red_attempts": result.get("red_attempts", 0),
                "green_attempts": result.get("green_attempts", 0),
                "red_judge_score": result.get("red_judge_score", 0.0),
                "green_judge_score": result.get("green_judge_score", 0.0),
                "phase_log": result.get("phase_log", []),
            }

        impl_code = result.get("impl_code", "")

        humaneval_passed = evaluate_single_humaneval(problem_id, impl_code)

        return {
            "problem_id": problem_id,
            "tdd_success": result.get("success", False),
            "humaneval_passed": humaneval_passed,
            "impl_code": impl_code,
            "test_code": result.get("test_code", ""),
            "red_attempts": result.get("red_attempts", 0),
            "green_attempts": result.get("green_attempts", 0),
            "red_judge_score": result.get("red_judge_score", 0.0),
            "green_judge_score": result.get("green_judge_score", 0.0),
            "phase_log": result.get("phase_log", []),
        }


def _git_sha(repo: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


async def run_humaneval_tdd_evaluation(
    problem_ids: List[str],
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
    for i, problem_id in enumerate(problem_ids, 1):
        print(f"[{i}/{len(problem_ids)}] {problem_id} ...", flush=True)
        set_call_tag(f"{problem_id}|{run_tag}")
        if prompt_log_base is not None:
            problem_log_dir = Path(prompt_log_base) / problem_id.replace("/", "-")
            problem_log_dir.mkdir(parents=True, exist_ok=True)
            os.environ["MAESTRO_PROMPT_LOG_DIR"] = str(problem_log_dir)

        t0 = time.monotonic()
        try:
            result = await run_humaneval_problem_with_tdd(
                problem_id=problem_id,
                generator_llm=generator_llm,
                judge_llm=judge_llm,
                escalation_llm=escalation_llm,
                test_llm=test_llm,
                max_retries=max_retries,
                judge_threshold=judge_threshold,
            )
        except ContentPolicyViolationError:
            result = {
                "problem_id": problem_id,
                "tdd_success": False,
                "humaneval_passed": False,
                "impl_code": "",
                "test_code": "",
                "error": "Content Policy Violation",
                "red_attempts": 0,
                "green_attempts": 0,
                "phase_log": [],
            }
        except Exception as e:
            result = {
                "problem_id": problem_id,
                "tdd_success": False,
                "humaneval_passed": False,
                "impl_code": "",
                "test_code": "",
                "error": f"API Error: {str(e)}",
                "red_attempts": 0,
                "green_attempts": 0,
                "phase_log": [],
            }

        result["wall_time_s"] = round(time.monotonic() - t0, 1)
        results.append(result)
        status = "PASS" if result["humaneval_passed"] else "FAIL"
        print(f"    -> {status} (tdd_success={result['tdd_success']}, "
              f"{result['wall_time_s']}s)", flush=True)

    total = len(results)
    passed = sum(1 for r in results if r["humaneval_passed"])
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
        },
        "summary": {
            "total_problems": total,
            "humaneval_passed": passed,
            "tdd_succeeded": tdd_success,
            "pass_rate": passed / total if total > 0 else 0.0,
            "tdd_success_rate": tdd_success / total if total > 0 else 0.0,
        },
        "results": results,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
    }

    result_file = out_dir / (
        f"humaneval_tdd_{config_name}_{len(problem_ids)}p_{summary['timestamp']}.json"
    )
    result_file.write_text(json.dumps(summary, indent=2))

    print(f"\nHumanEval Pass Rate: {passed}/{total} "
          f"({summary['summary']['pass_rate']:.1%}) | TDD Success: {tdd_success}/{total}")
    print(f"Results saved to: {result_file}")

    return summary
