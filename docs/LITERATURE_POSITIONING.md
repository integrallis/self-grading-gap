# Literature positioning, replication program, and thesis trajectory (2026-07-15)

Sources: primary-source-verified survey of 2021-2026 code-gen verification / TDD-LLM
literature (~35 works) + extraction of the 2025 capstone's literature review. Full agent
reports in session records; this file is the load-bearing synthesis.

## 1. The refute/strengthen ledger (prior claims vs our evidence)

STRENGTHENED BY US (convergent, independent designs):
- Ahmed et al. 2025/26 (SWE-bench test overfitting): 21.8-33% of self-test-passing patches
  fail held-out golden tests; refinement WORSENS it (21.8->25.5). Our exp006/007
  conditional false-accept rates: 18% (HumanEval+) and 29% (LCB hidden). THE SAME ~1-in-4
  CONSTANT from an entirely different instrument. Closest published design to ours; ours
  adds prospective oracle error bars + adapter audit + N=5 repetition discipline.
- TDFlow 2026: 94.3% with human tests vs 68.0% self-tests — a 26-pt verification gap
  measured with a weak instrument (no held-out oracle; manual hack audit found 7/800).
- Olausson et al. (self-repair not a silver bullet; feedback is the bottleneck; human
  feedback 1.58x): our frontier-judge feedback lifting true pass +5-6/30 confirms feedback
  quality is the lever; our addition — it never touches false accepts.
- Huang et al. (no intrinsic self-correction without oracle stop signals); Reflexion's own
  footnote (16.3% self-test FP on MBPP, gains vanish exactly there); Crupi et al. (~50%
  judge false-accept, kappa 0.10-0.21); CodeJudgeBench (test-judging is the hardest task):
  all consistent with soundness-invariance; none measured it inside a full TDD loop.
- ImpossibleBench / METR / OpenAI-Baker / Denison (reward hacking): validate our adapter
  design choices (read-only oracle, non-inspectable scoring, static+behavioral detection)
  as the mitigations their taxonomies demand.

CANDIDATE NULLIFICATIONS (their result is plausibly an oracle-weakness artifact):
- Chen et al. 2026 "agent-written tests don't change outcomes": outcome variable is
  SWE-bench Verified, which STING shows is 77% under-constrained. Our harness can detect
  correctness effects their oracle cannot see.
- SWT-Bench "generated-test filtering doubles precision to 47.8%": thesis predicts the
  gain shrinks against a strong oracle (generated tests share generator blind spots —
  CodeT's +18.8 stands on the same mechanism).
- Mathews & Nagappan (+9-30 pts from tests-in-prompt) and TiCoder (+45.97, admitted upper
  bound from a reference-implementation-simulated user): both contaminated function-level;
  our requirements-only prompting with held-out grading tests whether the benefit survives
  when the visible signal is not a subset of the grading oracle.

## 2. The dataset-anatomy thesis (prediction: confirmed by survey)

Prior "TDD" datasets are weak TDD representations, algorithmic-level only:
- tests-as-prompt-garnish: Mathews&Nagappan, WebApp1K (tests ARE prompt and oracle);
- single fail-to-pass reproduction tests: TDD-Bench Verified (23.6% F2P best), SWT-Bench —
  one test flipping on one patch is not a suite, let alone test-first design;
- self-authored circular oracles: TDDev, ARC (pipeline writes its own acceptance tests);
- no held-out oracle at all: TDFlow;
- algorithmic I/O toys: HumanEval (7.7 tests/problem, mutation score 87.69% per JSEP'25
  measurement; 12.2-18.9% training contamination per Riddell), LiveCodeBench (algorithmic).
Nobody mutation-scores the oracle they grade with; nobody classifies survivors; nobody
publishes oracle error bars. Ours: 18 tests/pkg behavior suites, stateful multi-concern
domains, 0.981 kill with 100% survivor classification, requirements above the test layer.
Planned artifact: cross-dataset oracle-strength table (run our mutation machinery over
samples of their oracles) — turns "weak TDD representation" from claim into their number.

## 3. Replication matrix (all authorized; code available or recreatable)

| # | Target claim | How | Feasibility | Est. cost |
|---|---|---|---|---|
| R1 | Ahmed 21.8-33% overfit; refinement worsens | our RGR loop on D, self-tests vs held-out oracle | recreatable protocol | flagship run |
| R2 | Mathews TGen +9-30 pts | requirements-only vs tests-shown prompting on D | trivial recreation | ~$5 |
| R3 | CodeT dual-agreement +18.8 | rank N candidates by generated-test agreement; measure FA vs classified mutants | trivial | ~$5 |
| R4 | Crupi ~50% judge false-accept | 2026 judges on mutant-derived wrong impls | easy; mutants already exist | ~$5 |
| R5 | SWT-Bench filtering precision | their released harness + our oracle side-by-side | harness validated locally already | ~$10 |
| R6 | Chen 2026 null | test-writing interventions in our loop, oracle-graded | recreatable | ~$15 |
| R7 | Reflexion FP-vs-complexity curve | self-test FP rate across 89 packages by tier | easy | ~$10 |
| R8 | Oracle-strength audit | mutation-score samples of HumanEval/TDD-Bench/SWT-Bench oracles | our machinery, their data | ~$0 API |
| R9 | ImpossibleBench probes | conflicting-spec probes through the adapter | red-team certification | ~$3 |

## 4. Thesis trajectory

Current thesis: verification strength inside the loop buys completeness, never soundness.
The framework extends it into a three-layer program:
(a) FIELD CONSTANT: the ~20-30% false-claimed-success rate now appears across four
    independent instruments (ours x2 benchmarks, Ahmed, SWE-ABS/STING). Our RGR-on-D run
    makes it the first prospectively-measured, error-barred version — from phenomenon to
    reference number.
(b) INSTRUMENT CRITIQUE: prior TDD conclusions rest on weak/self-authored/contaminated
    oracles (the anatomy table); several field results (Chen null, SWT filtering) are
    candidate artifacts of that weakness — testable by replication.
(c) CONSTRUCTIVE CLOSURE: the paper's conclusion currently ENDS at "internal verdicts need
    an external calibration channel." The framework IS that channel — oracle-first,
    error-barred, adversarially certified. "Who grades the grader?" gets an answer, not
    just a warning.
Publication shape recommendation: two papers. Paper A (verification gap): exp006/007 +
the RGR-on-D flagship (R1) + R4/R6 as external validations. Paper B (instrument):
dataset + harness + anatomy/oracle-strength tables + R8/R9 + exp009 protocol series as
the methods evaluation. The capstone arc (its own §4.3.2 named the dataset gap) is Paper
B's provenance narrative. R2/R3/R5/R7 strengthen either as appendices or Paper B studies.
