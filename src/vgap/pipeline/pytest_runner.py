"""pytest subprocess runner.

Runs the workspace suite with `sys.executable -m pytest` (pinned interpreter, so the recorded
interpreter/pytest version is the one that runs) under a 30 s timeout. A timeout scores as a
failed run (TestResult with all_passed=False and a TIMEOUT marker in the output); FAILED
lines are parsed into failed_tests."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestResult:
    all_passed: bool
    output: str
    failed_tests: list[str]
    exit_code: int


def run_tests(project_root: Path, test_file: Path | None = None) -> TestResult:
    cmd = [sys.executable, "-m", "pytest"]

    if test_file:
        cmd.append(str(test_file))
    else:
        cmd.append("tests/")

    cmd.extend(["-v", "--tb=short"])

    env = os.environ.copy()
    src_path = project_root / "src"
    if src_path.exists():
        existing_path = env.get("PYTHONPATH", "")
        if existing_path:
            env["PYTHONPATH"] = f"{src_path}:{existing_path}"
        else:
            env["PYTHONPATH"] = str(src_path)

    try:
        result = subprocess.run(
            cmd, cwd=project_root, capture_output=True, text=True, timeout=30, env=env
        )
    except subprocess.TimeoutExpired:
        # v2 (B-2 fixed): a hanging generated test scores as a failing run instead of
        # crashing the whole problem.
        return TestResult(
            all_passed=False,
            output="TIMEOUT: test run exceeded 30s",
            failed_tests=["<timeout>"],
            exit_code=-1,
        )

    all_passed = result.returncode == 0

    failed_tests = []
    if not all_passed:
        for line in result.stdout.split("\n"):
            if "FAILED" in line:
                parts = line.split("::")
                if len(parts) >= 3:
                    method = parts[2].split(" ")[0]
                    failed_tests.append(method)
                elif len(parts) >= 2:
                    test_name = parts[1].split(" ")[0]
                    failed_tests.append(test_name)

    return TestResult(
        all_passed=all_passed,
        output=result.stdout + result.stderr,
        failed_tests=failed_tests,
        exit_code=result.returncode,
    )
