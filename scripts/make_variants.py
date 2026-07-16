"""Regenerate the anchoring-ablation template variants from ANCHOR markers.

The templates delimit their anchoring blocks with `{# ANCHOR:BEGIN #}` / `{# ANCHOR:END #}`
comment lines; variants are the base templates with those blocks removed:
  anchor_none      — block removed from BOTH the generator and judge templates
  anchor_gen_only  — block removed from the JUDGE template only
  anchor_judge_only— block removed from the GENERATOR template only
Run after any base-template change; refreshes templates_variants/ and its manifest.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

PIPE = Path(__file__).resolve().parent.parent / "src" / "vgap" / "pipeline"
BASE = PIPE / "templates"
VAR = PIPE / "templates_variants"

GEN = "agents/code/python_generate_tests_simple.j2"
JUDGE = "judge/test_quality.j2"

BLOCK = re.compile(r"\{#\s*ANCHOR:BEGIN\s*#\}.*?\{#\s*ANCHOR:END\s*#\}\n?", re.DOTALL)


def strip_anchor(rel: str) -> str:
    text = (BASE / rel).read_text()
    assert BLOCK.search(text), f"no ANCHOR block in {rel}"
    return BLOCK.sub("", text)


def write(variant: str, rel: str, content: str) -> None:
    p = VAR / variant / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def main() -> None:
    gen_stripped = strip_anchor(GEN)
    judge_stripped = strip_anchor(JUDGE)

    write("anchor_none", GEN, gen_stripped)
    write("anchor_none", JUDGE, judge_stripped)
    write("anchor_gen_only", JUDGE, judge_stripped)
    write("anchor_judge_only", GEN, gen_stripped)

    manifest = []
    for p in sorted(VAR.rglob("*.j2")):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        manifest.append(f"{h}  ./{p.relative_to(VAR)}")
    (VAR / "MANIFEST.sha256").write_text("\n".join(manifest) + "\n")
    print(f"variants regenerated ({len(manifest)} files) + manifest")


if __name__ == "__main__":
    main()
