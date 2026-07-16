"""Workspace bootstrapper: writes the minimal `solution` package skeleton the TDD cycle
runs in — tests/conftest.py (sys.path insertion), pyproject.toml ([tool.pytest.ini_options]
testpaths + pythonpath), src/<package>/__init__.py version stub, tests/__init__.py,
.python-version, .pre-commit-config.yaml, and static placeholder .gitignore /
docker-compose.yml (execution-inert; nothing touches the network). Git init is the runner's
job."""

from __future__ import annotations

from pathlib import Path


class PythonBootstrapper:
    def bootstrap(self, project_path: Path, config: dict) -> dict[str, str]:
        files: dict[str, str] = {}

        files[".gitignore"] = (
            "# Python\n__pycache__/\n*.py[cod]\n*.egg-info/\n.eggs/\nbuild/\ndist/\n"
            ".venv/\nvenv/\n.pytest_cache/\n.mypy_cache/\n.coverage\nhtmlcov/\n"
            ".idea/\n.vscode/\n"
        )
        files["docker-compose.yml"] = (
            "# Placeholder (execution-inert)\nservices: {}\n"
        )
        files["README.md"] = f"# {config.get('project_name', 'project')}\n\nA Python project\n"

        files["pyproject.toml"] = self._generate_pyproject_toml(config)

        python_version = config.get("python_version", "3.11")
        files[".python-version"] = f"{python_version}\n"

        files[".pre-commit-config.yaml"] = self._generate_precommit_config()

        package_name = config.get(
            "package_name", config.get("project_name", "app").lower().replace("-", "_")
        )

        if not any("src/" in path for path in files.keys()):
            files[f"src/{package_name}/__init__.py"] = (
                f'"""The {package_name} package."""\n\n__version__ = "0.1.0"\n'
            )

        if not any("tests/" in path for path in files.keys()):
            files["tests/__init__.py"] = ""
            files["tests/conftest.py"] = (
                f'''"""Pytest configuration."""\n\nimport sys\nfrom pathlib import Path\n\n# Add src to path\nsrc_path = Path(__file__).parent.parent / "src"\nif src_path.exists():\n    sys.path.insert(0, str(src_path))\n\n\n# ==============================================================================\n# Test Isolation: Reset Global State Between Tests\n# ==============================================================================\n# If your implementation uses module-level state (global variables, lists, dicts),\n# you MUST reset it between tests to prevent state leakage.\n#\n# Example: If you have global state like:\n#   _counter = 0\n#   _items = []\n#\n# Create a reset function in your implementation:\n#   def reset_state():\n#       global _counter, _items\n#       _counter = 0\n#       _items = []\n#\n# Then uncomment and adapt the fixture below:\n# ------------------------------------------------------------------------------\n# import pytest\n# from {package_name} import reset_state  # Replace with your actual reset function\n#\n# @pytest.fixture(autouse=True)\n# def reset_global_state():\n#     """\"Reset global state before and after each test.\"\"\"\n#     reset_state()\n#     yield\n#     reset_state()\n# ==============================================================================\n'''
            )

        return files

    def _generate_pyproject_toml(self, config: dict) -> str:
        project_name = config.get("project_name", "project")
        package_name = config.get(
            "package_name", project_name.lower().replace("-", "_")
        )
        python_version = config.get("python_version", "3.11")

        dev_deps = [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "ruff>=0.1",
            "mypy>=1.0",
        ]

        if config.get("include_tdd_extras", False):
            dev_deps.extend(
                ["pytest-mock>=3.0", "pytest-asyncio>=0.21", "hypothesis>=6.0"]
            )

        dev_deps_str = ",\n    ".join(f'"{dep}"' for dep in dev_deps)

        return f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "A Python project"
readme = "README.md"
requires-python = ">={python_version}"
dependencies = ["pydantic>=2.0"]

[project.scripts]
{package_name} = "{package_name}.__main__:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    {dev_deps_str}
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.black]
line-length = 88
target-version = ["py{python_version.replace('.', '')}"]

[tool.ruff]
line-length = 88
target-version = "py{python_version.replace('.', '')}"
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "{python_version}"
warn_return_any = true
warn_unused_configs = true
"""

    def _generate_precommit_config(self) -> str:
        return """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
"""
