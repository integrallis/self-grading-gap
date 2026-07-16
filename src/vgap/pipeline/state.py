"""TDD cycle state: TDDCycleState, the LangGraph state dict the RED-GREEN-VERIFY subgraph
threads through its nodes, and the CartridgeContext project-configuration block."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class CartridgeContext(TypedDict, total=False):
    programming_language: str
    application_type: str
    frameworks: list[str]
    testing_frameworks: list[str]
    deployment_target: str


class TDDCycleState(TypedDict, total=False):
    messages: Annotated[Sequence[BaseMessage], add_messages]

    task: dict
    workspace_path: str
    project_name: str
    cartridge: CartridgeContext

    generator_llm: Any

    project_brief: str
    existing_implementation: str
    recent_commits: list[dict]

    tdd_phase: Literal["RED", "GREEN", "VERIFY", "REFACTOR", "COMPLETE", "FAILED"]
    red_attempts: int
    green_attempts: int
    verify_attempts: int
    max_retries: int
    escalation_threshold: int

    test_code: str
    test_file_path: str
    impl_code: str
    impl_file_path: str

    test_result: dict

    red_judge_score: float
    green_judge_score: float
    judge_threshold: float
    judge_feedback: str

    context_level: Literal["minimal", "enhanced", "full"]

    git_enabled: bool
    last_commit_sha: str

    bootstrapped: bool

    success: bool
    failure_reason: str

    phase_log: list[str]


def _get_recent_commits(repo_path: str, max_count: int = 10) -> list[dict]:
    """Recent commits for LLM context; empty list on any failure (faithful to original).
    GitPython imported lazily: only reached when git_enabled=True, which the
    HumanEval runner never sets."""
    try:
        from git import Repo

        repo = Repo(repo_path)
        commits = []
        for commit in list(repo.iter_commits(max_count=max_count)):
            msg = (
                commit.message
                if isinstance(commit.message, str)
                else commit.message.decode("utf-8")
            )
            commits.append(
                {
                    "sha": str(commit.hexsha)[:8],
                    "author": str(commit.author),
                    "date": commit.committed_datetime.isoformat(),
                    "message": msg.split("\n")[0],
                }
            )
        return commits
    except Exception:
        return []


def create_initial_tdd_cycle_state(
    task: dict,
    workspace_path: str,
    project_name: str,
    cartridge: CartridgeContext,
    project_brief: str = "",
    existing_implementation: str = "",
    max_retries: int = 3,
    judge_threshold: float = 0.7,
    escalation_threshold: int = 3,
    git_enabled: bool = True,
    bootstrapped: bool = False,
) -> TDDCycleState:
    recent_commits = []
    if git_enabled and (Path(workspace_path) / ".git").exists():
        recent_commits = _get_recent_commits(workspace_path, max_count=10)

    return TDDCycleState(
        messages=[],
        task=task,
        workspace_path=workspace_path,
        project_name=project_name,
        cartridge=cartridge,
        project_brief=project_brief,
        existing_implementation=existing_implementation,
        recent_commits=recent_commits,
        tdd_phase="RED",
        red_attempts=0,
        green_attempts=0,
        verify_attempts=0,
        max_retries=max_retries,
        escalation_threshold=escalation_threshold,
        test_code="",
        test_file_path="",
        impl_code="",
        impl_file_path="",
        test_result={},
        red_judge_score=0.0,
        green_judge_score=0.0,
        judge_threshold=judge_threshold,
        judge_feedback="",
        context_level="minimal",
        git_enabled=git_enabled,
        last_commit_sha="",
        bootstrapped=bootstrapped,
        success=False,
        failure_reason="",
        phase_log=[],
    )
