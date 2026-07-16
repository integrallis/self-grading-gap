"""Prompt manager: renders the Jinja templates under templates/.

Jinja flags: trim_blocks, lstrip_blocks, autoescape off; per-agent config overlay from
config.yaml. An unknown agent or missing template resolves to None; a template that fails to
RENDER raises RuntimeError (a broken template must never silently become an empty prompt).
With MAESTRO_PROMPT_LOG_DIR set, every rendered prompt and its LLM response are logged with a
per-instance counter. VGAP_PROMPT_VARIANT selects an anchoring-ablation overlay directory and
refuses unknown names rather than running a mislabeled condition."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, Template, TemplateError
from langchain_core.prompts import PromptTemplate

TEMPLATES_DIR = Path(__file__).parent / "templates"


def content_to_text(content: Any) -> str:
    """Normalize LLM message content to text: some providers return content as a list of
    blocks rather than a string. Identity for str content."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(str(block.get("text", "")))
            else:
                parts.append(str(getattr(block, "text", "")))
        return "".join(parts)
    return str(content)


class MaestroPromptManager:
    def __init__(self, prompt_dir: Path | list[Path] | None = None):
        """prompt_dir may be a list for anchoring-ablation overlays: earlier dirs shadow
        later ones (variant dir first, base templates second)."""
        if prompt_dir is None:
            variant = os.environ.get("VGAP_PROMPT_VARIANT", "both")
            if variant in ("", "both"):
                self.prompt_dirs = [TEMPLATES_DIR]
            else:
                vdir = Path(__file__).parent / "templates_variants" / variant
                if not vdir.is_dir():
                    raise ValueError(
                        f"VGAP_PROMPT_VARIANT={variant!r} has no directory {vdir} — "
                        f"refusing to run the wrong condition silently"
                    )
                self.prompt_dirs = [vdir, TEMPLATES_DIR]
        elif isinstance(prompt_dir, (list, tuple)):
            self.prompt_dirs = [Path(p) for p in prompt_dir]
        else:
            self.prompt_dirs = [Path(prompt_dir)]
        self.prompt_dir = self.prompt_dirs[0]

        self.jinja_env = Environment(
            loader=FileSystemLoader(self.prompt_dirs),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=False,
        )

        self.config = self._load_config()

        self._template_cache: dict[str, Template] = {}
        self._langchain_cache: dict[str, PromptTemplate] = {}

        self._log_dir = os.environ.get("MAESTRO_PROMPT_LOG_DIR")
        self._prompt_counter = 0
        self._last_prompt_file: Path | None = None

    def _log_rendered_prompt(
        self,
        template_path: str,
        rendered_prompt: str,
        variables: dict[str, Any],
    ) -> None:
        if not self._log_dir:
            return

        log_dir = Path(self._log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)

        self._prompt_counter += 1
        template_name = Path(template_path).stem
        timestamp = int(time.time() * 1000)
        filename = f"{self._prompt_counter:02d}_{template_name}_{timestamp}.txt"
        log_file = log_dir / filename

        log_content = "=" * 80 + "\n"
        log_content += f"TEMPLATE: {template_path}\n"
        log_content += f"TIMESTAMP: {timestamp}\n"
        log_content += "VARIABLES:\n"
        for key, value in variables.items():
            value_str = str(value)
            if len(value_str) > 200:
                value_str = value_str[:200] + "...[truncated]"
            log_content += f"  {key}: {value_str}\n"
        log_content += "=" * 80 + "\n\n"
        log_content += rendered_prompt

        with open(log_file, "w") as f:
            f.write(log_content)

        self._last_prompt_file = log_file

    def log_llm_response(
        self,
        response: Any,
        template_path: str | None = None,
    ) -> None:
        if not self._log_dir:
            return

        log_dir = Path(self._log_dir)

        if hasattr(response, "content"):
            response_content = content_to_text(response.content)
        else:
            response_content = str(response)

        if self._last_prompt_file:
            response_file = self._last_prompt_file.parent / (
                self._last_prompt_file.stem + "_RESPONSE.txt"
            )
        else:
            timestamp = int(time.time() * 1000)
            response_file = (
                log_dir / f"{self._prompt_counter:02d}_response_{timestamp}.txt"
            )

        response_log = "=" * 80 + "\n"
        response_log += "LLM RESPONSE\n"
        response_log += "=" * 80 + "\n\n"
        response_log += response_content

        with open(response_file, "w") as f:
            f.write(response_log)

    def _load_config(self) -> dict[str, Any]:
        config_path = next(
            (d / "config.yaml" for d in self.prompt_dirs if (d / "config.yaml").exists()),
            self.prompt_dir / "config.yaml",
        )

        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = yaml.safe_load(f)
                    if "default" not in config:
                        config["default"] = {}
                    if "agents" not in config:
                        config["agents"] = {}
                    return config
            except Exception as e:
                logging.warning(
                    f"Failed to load prompts config from {config_path}: {e}"
                )

        return {
            "default": {
                "fence_open": "```",
                "fence_close": "```",
                "style": "standard",
            },
            "agents": {},
        }

    def get_prompt(
        self, agent_name: str, use_langchain: bool = True, **kwargs: Any
    ) -> str | PromptTemplate | None:
        agent_config = self.config.get("agents", {}).get(agent_name)

        if not agent_config:
            return None

        template_path = agent_config.get("template")

        if not template_path:
            return None

        if not any((d / template_path).exists() for d in self.prompt_dirs):
            return None

        try:
            if use_langchain:
                return self._get_langchain_prompt(agent_name, template_path, **kwargs)
            else:
                return self._get_jinja_prompt(template_path, agent_config, **kwargs)
        except (TemplateError, FileNotFoundError):
            return None

    def _get_langchain_prompt(
        self, agent_name: str, template_path: str, **kwargs: Any
    ) -> PromptTemplate | None:
        try:
            if agent_name not in self._langchain_cache:
                agent_config = self.config.get("agents", {}).get(agent_name, {})
                config_to_use = self._get_config_for_agent(agent_config)
                jinja_template = self.jinja_env.get_template(template_path)

                render_context: dict[str, Any] = {"config": config_to_use}
                for key in kwargs.keys():
                    render_context[key] = f"{{{key}}}"

                pre_rendered = jinja_template.render(**render_context)
                input_vars = list(kwargs.keys()) if kwargs else []

                self._langchain_cache[agent_name] = PromptTemplate(
                    template=pre_rendered,
                    input_variables=input_vars,
                    template_format="f-string",
                )

            return self._langchain_cache[agent_name]

        except Exception:
            return None

    def _get_jinja_prompt(
        self, template_path: str, agent_config: dict[str, Any], **kwargs: Any
    ) -> str | None:
        try:
            if template_path not in self._template_cache:
                self._template_cache[template_path] = self.jinja_env.get_template(
                    template_path
                )

            template = self._template_cache[template_path]
            config_to_use = self._get_config_for_agent(agent_config)
            rendered = template.render(config=config_to_use, **kwargs)

            self._log_rendered_prompt(
                template_path=template_path,
                rendered_prompt=rendered,
                variables={"config": config_to_use, **kwargs},
            )

            return rendered

        except Exception as e:
            # A render failure is an instrument error, not an empty prompt.
            raise RuntimeError(f"template render failed for {template_path}: {e}") from e

    def _get_config_for_agent(self, agent_config: dict[str, Any]) -> dict[str, Any]:
        config = self.config.get("default", {}).copy()

        experiment_name = agent_config.get("experiment")
        if experiment_name and "experiments" in self.config:
            experiment = self.config["experiments"].get(experiment_name, {})
            config.update(experiment)

        return config

