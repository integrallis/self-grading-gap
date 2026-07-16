# Research Plan

> **Scope note (2026-07-13).** The paper and this public repository are fully independent of
> the 2025 informal-experiment artifacts: all paper numbers come from fresh, instrumented runs
> (exp003, exp004a) with full-benchmark confirmation pre-registered as exp004b. The
> artifact-reconstruction studies that informed early direction (exp001/exp002) live in the
> team's private archive, not here.

Working title: **The Verification Gap in Self-Testing Code Agents**.
Target: FSE 2027 (submission deadline 2026-10-02, verified 2026-07-09); fallback TOSEM/EMSE
(rolling). ICSE 2027's deadline passed 2026-06-30.

## Claim under construction

In fully autonomous test-first pipelines (agent writes tests, then code, with LLM judges in the
loop), the dominant failure mode is *self-consistent misalignment*: tests and implementation
agree with each other and disagree with the specification. Internal signals (self-test pass, judge
scores) are structurally blind to it. Grounding self-authored tests in the specification's worked
examples closes most of the gap at negligible cost.

Evidence base inherited from the predecessor (maestro-langgraph, treated as hypotheses until
audited): baseline TDD pipeline 146/164 on HumanEval with self-reported success 162/164 (gap =
16 problems, 89% of failures); anchoring intervention 157/164, replicated at 157/164 after
removing 16 problem-specific prompt hints; judge–execution correlation r=0.52.

## Research questions

- **RQ1 (phenomenon):** How large is the verification gap — Pr(self-reported success) −
  Pr(ground-truth pass) — across models and benchmarks, and how does it split into test-suite
  weakness vs judge blindness?
- **RQ2 (mechanism):** What distinguishes gap problems? (test-suite mutation score / coverage,
  docstring-example coverage, spec ambiguity, judge score trajectories)
- **RQ3 (intervention):** Does canonical example anchoring reduce the gap? Which side carries the
  effect (generator-prompt mandate vs judge-enforcement), and does the effect survive oracles
  that exceed the docstring examples (HumanEval+, MBPP+, LiveCodeBench)?
- **RQ4 (confounds & cost):** How much of end-to-end success is attributable to frontier-model
  escalation (incl. judge-emitted corrected code), and what does each condition cost in tokens
  and dollars?

## Experiment ladder

| ID | Question | Scale | API? | Status |
|----|----------|-------|------|--------|
| exp001 artifact audit | Do the predecessor's committed artifacts reproduce its 157/164 claim? First harder-oracle (HumanEval+) data point on the same code. | 164 problems, no LLM calls | no | pre-registered in `experiments/exp001_artifact_audit/README.md` |
| exp002 self-test re-execution | Reconstruct self-reported success independently: run each problem's self-authored tests against its reconstructed implementation; recompute the gap from artifacts alone. | 164, local exec | no | planned |
| exp003 noise floor | Re-run the pipeline, one condition, N≥5 identical runs; per-problem flip rate, Wilson CIs. Nothing is compared until this exists. | 164 × 5 | yes (small) | planned; local or VPS |
| exp004 factorial | anchoring {off, generator-only, judge-only, both} × escalation {on, off} × ≥3 generator models; N≥5 seeds; paired McNemar vs condition baseline; full token/cost accounting. | large | yes | VPS |
| exp005 benchmark transfer | Best + control conditions on MBPP+ and LiveCodeBench (held-out: prompts frozen at exp004 SHA — no tuning on these). | large | yes | VPS |
| exp006 mechanism | Mutation score & coverage of self-authored test suites (anchored vs not); judge-score calibration curves; per-layer provenance of shipped code. | analysis-heavy | partial | planned |

Small local experiments validate direction before anything scales to the VPS; every VPS run is
pre-registered and budgeted first.

## Statistical plan

Per-problem outcomes are paired across conditions on the same problem set: exact McNemar for
condition pairs, Wilson intervals per condition, and the exp003 flip-rate as the noise floor any
claimed delta must clear. Aggregates reported as mean ± CI over runs, never single runs. Analysis
scripts derive every paper table/figure from committed raw result files (`reproduce.sh`).

## Known threats (carried from the 2026-07-09 assessment, addressed by design)

1. **Prose-only headline** → exp001/exp002 audit from artifacts; all new runs emit machine-readable
   summaries with provenance (CLAUDE.md invariants 1–3).
2. **N=1 nondeterminism** (the two 157/164 runs fail different problems) → exp003 before any delta claim.
3. **Escalation confound** (GPT-5 judge can inject corrected code) → exp004 escalation arm + shipped-code
   provenance tracking in exp006.
4. **Docstring examples overlap the oracle** → exp001 HumanEval+ scoring; exp005 held-out benchmarks.
5. **Eval-set tuning history** (prompts were iterated on HumanEval failures) → frozen prompts;
   MBPP+/LiveCodeBench as held-out; disclose tuning history in the paper.
6. **No cost data** → token/dollar accounting mandatory in every API runner (CLAUDE.md invariant 11).

## Framework choices (minimize bespoke code)

- Scoring: **EvalPlus** (HumanEval/+ and MBPP/+), official **LiveCodeBench** harness later.
- Mutation testing (exp006): evaluate `mutmut` vs `cosmic-ray` on a pilot before committing.
- Stats: scipy/statsmodels implementations of McNemar/Wilson — no hand-rolled p-values.
- Pipeline under study: **ported into `src/vgap/pipeline/`** (user decision 2026-07-09,
  superseding the earlier fork-and-patch plan): the minimal closure of the maestro TDD pipeline,
  recreated with line-by-line review. Prompt templates copied byte-identical and verified by
  render-equivalence against the predecessor's logged 2025 prompts. Defects found in review are
  logged in `src/vgap/pipeline/REVIEW.md`; behavior-changing fixes ship behind config flags
  defaulting to 2025 behavior so exp003 measures the system under study and exp004 can ablate
  legacy-vs-fixed. Cost/usage instrumentation and machine-readable summaries are native.
