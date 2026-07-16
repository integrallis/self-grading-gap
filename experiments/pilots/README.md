# Benchmark pilots (exploratory — NOT pre-registered)

Feasibility pilots for successor benchmarks to EvalPlus/HumanEval+, motivated by the
mid-2026 landscape review: HumanEval-era suites are presumed contaminated at review time,
and the paper needs an oracle whose problems post-date the weak model's training data.
Nothing here tests a hypothesis; these runs measure floors/ceilings, harness friction, and
cost so exp007 can be pre-registered on solid ground. All generation uses gpt-4o-mini (the
study's weak model W). Harness clones live outside the repo under
`../benchmarks/` (LiveCodeBench, swt-bench, TDD-Bench-Verified, TEBench); every score below
is computed by the benchmark's own harness code, not re-implemented checkers.

## 1. LiveCodeBench (code_generation_lite, release_v6) — COMPLETE

**Setup.** Harness venv (Python 3.11, `datasets` pinned to 2.21.0 — v6 ships as a script
dataset that `datasets>=3` refuses to load; this is the only friction encountered). Slice:
release_v6 filtered to contest_date >= 2025-01-01 (182 problems; >1 year past
gpt-4o-mini's training cutoff), stratified 2 problems per (difficulty × platform) cell = 12
problems (Jan 2025 contests). Prompts rendered with the harness's generic template;
generation at LCB leaderboard settings (T=0.2, top_p=0.95) but n=3 samples instead of the
leaderboard's n=10 (recorded deviation). Scoring via `codegen_metrics` — the same function
`lcb_runner.runner.custom_evaluator` calls — against full public+private test sets.

**Result** (`lcb/results/lcb_pilot_summary.json`):

| slice | pass@1 | problems |
|---|---|---|
| overall | 0.250 | 12 |
| easy | 0.750 | 4 |
| medium | 0.000 | 4 |
| hard | 0.000 | 4 |
| leetcode | 0.167 | 6 |
| atcoder | 0.333 | 6 |

Per-problem outcomes were all-or-nothing (each problem 0/3 or 3/3 samples passed); no
extraction failures (0 empty extractions across 36 samples).

**Cost/time.** 36 completions, 16,590 in / 6,961 out tokens, ≈$0.007, 40 s wall.

**Verdict.** Viable as exp007's oracle, with one hard constraint: gpt-4o-mini is non-floor
ONLY on the easy tier of post-cutoff problems. An exp007 problem set must be drawn mostly
from the easy tier (weak model in the measurable 25–75% band), with medium problems
included only if the design wants headroom for strong-model cells. LeetCode problems carry
starter code (functional style) and adapt naturally to the TDD pipeline's task shape;
AtCoder problems are stdin/stdout and would need a different RED-phase harness — restricting
to LeetCode-style functional problems is the low-friction path. Building the
TDD-pipeline-on-LCB adapter is exp007 instrument work, deliberately out of pilot scope.

## 2. SWT-Bench Lite (test generation, fail-to-pass oracle) — COMPLETE

**Setup.** Harness installed clean. The benchmark publishes ready-made prompt datasets with
BM25-retrieved 27k-token context (`nmuendler/SWT-Bench_Lite_bm25_27k_zsp`), so no scaffold
is needed for a zero-shot pilot. Generation: first 5 instances by instance_id (all astropy —
single-repo slice, noted), T=0.0, raw output passed to the harness which extracts the
ZeroShotPlus custom-diff format itself (`--patch_types custom fuzzy`). 5 generations:
~129k in / ~1.3k out tokens, ≈$0.02, 7 s. Gold-patch validation passed first
(sympy__sympy-20590: 1/1 resolved).

**Result** (`swt/results/`, harness reports under the benchmark clone's
`run_instance_swt_logs/mini-zsp-pilot/`): gpt-4o-mini emitted syntactically plausible
custom-diff test patches for 5/5 instances, but only 1/5 applied to the repository
(astropy__astropy-6938), and that one did not flip fail-to-pass. **Applicability 1/5,
success 0/5.** The paper's GPT-4 ZeroShotPlus baseline reports ~87% applicability / ~16%
success on the full Lite set — the weak model is at floor here, failing mostly at emitting
edits that anchor correctly in 27k-token real-repo context (n=5, single repo: treat as a
floor signal, not an estimate).

**Verdict.** SWT-Bench cannot serve as a weak-generator setting: with no applicable tests
there are no accepts for a judge to grade. It remains attractive for the asymmetric cells —
a strong test author (the exp006 S role) produces gradeable tests here, and the fail-to-pass
oracle then measures the judge directly. Any exp007b on SWT-Bench should pair W-judge/S-judge
against S-authored tests rather than attempt W generation.

## 3. TDD-Bench Verified (449 instances, SWE-bench Verified-derived) — ASSESSED

**Setup.** Harness installed clean; dataset builds from HF via `dataset_preparation.py`.
Gold-patch validation passed (astropy__astropy-14995: 1/1 resolved, TDD score 1.0), so the
harness runs end to end on this machine.

**Assessment.** Predictions must be well-formed git diffs (vanilla patches; no
custom-format extraction), and the benchmark ships no prompt/context dataset — the paper's
own generation system (Otter: localization + generation + self-repair) is a separate
scaffold. A faithful gpt-4o-mini generation pilot therefore requires building a retrieval
scaffold first. Construct overlap with SWT-Bench is near-total (fail-to-pass test
generation on SWE-bench instances); SWT-Bench covers the same question with a packaged
zero-shot format. Verdict: keep as a robustness/secondary option; SWT-Bench is the primary
repo-level test-generation candidate.

## 4. TEBench (test evolution, 314 instances) — ASSESSED, NOT PILOTED

All instances are Java (Defects4J ecosystem, Maven builds, JaCoCo coverage). The construct
(agent-authored test updates scored against developer ground truth, three-version
V-1/V-0.5/V0 structure) is close to the paper's concerns, but piloting requires a Java
agent scaffold and the study's instrument is Python/pytest end to end. Verdict: cite as
related work; not a candidate oracle for this paper.

## Cross-cutting conclusions

- **Post-cutoff LCB easy tier is the direct EvalPlus replacement**: same task shape as the
  pipeline (NL spec → function), hidden tests, contamination-controlled window, measurable
  weak-model band (pass@1 0.75 easy vs 0.00 medium/hard), negligible cost. exp007's primary
  oracle candidate; needs a TDD-pipeline adapter for LeetCode-style functional problems.
- **Weak-model repo-level generation is at floor everywhere**: gpt-4o-mini 0/5 fail-to-pass
  (1/5 applicability) on SWT-Bench Lite; gpt-4o 4.9% on SWE-bench Pro. Repo-scale settings
  only enter the study through the asymmetric design — strong model authors the tests, the
  benchmark's oracle grades the judge (candidate exp007b on SWT-Bench).
- **TDD-Bench Verified** duplicates SWT-Bench's construct without a packaged prompt set —
  secondary. **TEBench** is Java-only — related work.
- Total pilot spend: ≈$0.03 across 41 gpt-4o-mini completions. Docker disk from harness
  validation/eval images: ~15 GB (removable; instructions in each harness repo).
