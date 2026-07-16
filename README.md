# Who Grades the Grader? The Verification Gap in Self-Testing Code Agents

Reproducer repository for the paper ([`paper/main.pdf`](paper/main.pdf)). The paper studies a
structural failure of test-first coding agents — pipelines that author their own tests cannot
notice the errors those tests inherit — and measures it on a reviewed, instrumented TDD
pipeline across two benchmarks, including a contamination-controlled one. The central
experiments put a frontier model into the pipeline's verification seats (test author, judge,
both) and find an asymmetry: the strong judge eliminates false rejects and lifts oracle pass
rates through its feedback, while false accepts — self-authored tests and code agreeing
against the specification — stay flat in every cell. Strengthening the grader buys
completeness, not soundness.

Every number in the paper traces to a committed, script-generated result file; every
experiment was pre-registered (hypotheses, decision rules, budget cap) before its first API
call; nulls are reported as results. `CLAUDE.md` is the protocol that enforces this.

## Layout

```
paper/                        the paper (main.tex, refs.bib, figures, PDF)
src/vgap/pipeline/            the pipeline under study: engine, judges, prompt templates
                              (ANCHOR-marked anchoring blocks), anchoring template variants,
                              REVIEW.md defect register, cost instrumentation
experiments/
  pilots/                     benchmark feasibility pilots (LiveCodeBench, SWT-Bench,
                              TDD-Bench Verified, TEBench) behind the exp007 oracle choice
  exp006_model_asymmetry/     pre-registered 4-cell model-asymmetry experiment on the
                              HumanEval subset-30 (EvalPlus oracles)
  exp007_lcb_asymmetry/       pre-registered confirmatory replication on LiveCodeBench
                              (post-cutoff problem window, hidden-test oracle)
scripts/make_figures.py       regenerates every paper figure from committed result files
scripts/make_variants.py      regenerates the anchoring template variants from ANCHOR markers
docs/RUNBOOK.md               experimenter guide: keys, environments, running and scoring
PROVENANCE.md                 history, instrument versioning, and artifact provenance notes
```

## Reproduce (no API keys)

```bash
uv sync                                    # vgap venv (pipeline + analysis)
uv run pytest src -q                       # instrument tests
uv run python scripts/make_figures.py      # figures from committed results
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage analyze
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage analyze
```

The analyze stages re-derive every table in the paper from committed per-run results and
scores.

## Run the experiments

See [`docs/RUNBOOK.md`](docs/RUNBOOK.md): required API keys, environments (including the
LiveCodeBench harness checkout that exp007's score stage shells out to), budget caps,
measured costs, and the staged runners (every stage refuses to run before its prerequisite
exists). Each experiment's README is its pre-registration.

The pipeline is a reviewed recreation of a 2025 system with its defects fixed and its
prompts rewritten; `src/vgap/pipeline/REVIEW.md` is the defect register, and PROVENANCE.md
records the artifact's provenance.

## Paper

```bash
cd paper && latexmk -pdf main.tex
```
