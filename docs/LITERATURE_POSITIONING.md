# Literature positioning and next experiments — revised 2026-09-13

This replaces the 2026-07-15 planning memo. The earlier claims of a shared field constant,
“never soundness,” nullification of other studies, and unique use of mutation-based evaluation
are superseded. They were hypotheses or overinterpretations, not established findings.
Source verification and publication guidance are in [PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md);
statistical corrections are in [STATISTICAL_REVIEW.md](STATISTICAL_REVIEW.md).

The current contribution is measurement of an executed self-testing pipeline's acceptance,
independent oracle outcomes, and model-role interventions. The evidence shows residual
oracle-relative errors across the tested configurations. Failure to meet the original joint
improvement rule does not demonstrate invariance, a universal failure of stronger verification,
or a fixed false-accept rate. Comparisons across benchmark suites are contextual rather than
estimates of one shared population parameter.

## Relationship to earlier work

| Research line | Relation to this study |
|---|---|
| [The oracle problem in software testing](https://coinse.github.io/publications/pdfs/Barr2015qd.pdf) | Establishes the underlying challenge of obtaining a correctness criterion. This study measures particular agent-generated tests and review policies. |
| [Imperfect-verifier inference scaling](https://arxiv.org/abs/2411.17501) | Explains limits of resampling with false positives. The present role interventions differ from resampling under a fixed verifier. Observational retry groups do not isolate retry effects. |
| [Ahmed et al., test overfitting](https://arxiv.org/html/2511.16858v3) | Closest empirical predecessor: generated tests accept patches that fail golden tests, with refinement evaluated separately. Our comparisons add test-author and judge assignments within a different pipeline. |
| [EvalPlus](https://arxiv.org/abs/2305.01210) and [SWE-ABS](https://arxiv.org/abs/2603.00520) | Demonstrate that benchmark results depend on oracle adequacy. Stronger suites do not by themselves resolve specification ambiguity or establish a semantic error bound. |
| [CodeT](https://arxiv.org/abs/2207.10397) and [ConVerTest](https://arxiv.org/abs/2602.10522) | Use agreement to select code or tests and evaluate its utility. Our pipeline does not reproduce these methods, so it does not refute their improvements. Residual conditional error is a useful additional endpoint. |
| [TiCoder](https://arxiv.org/abs/2404.10100), [TENET](https://arxiv.org/abs/2509.24148), and [TDFlow](https://arxiv.org/abs/2510.23761) | Human clarification, developer-supplied tests, and autonomous test generation are different input regimes. Distinguish them when comparing outcomes. |
| [CodeJudgeBench](https://arxiv.org/html/2507.10535v2) | Documents strong but imperfect judges and sensitivity to task and presentation. Its rankings do not validate a later model version or the current GREEN rubric, which focuses on passing supplied tests. |
| [Sam-Bodden, context ablation](https://arxiv.org/abs/2607.09691) | Complementary methodology: hold one component fixed, vary another, and evaluate behavior independently. It studies context representation rather than self-test reliability. |

## Experiments that would address remaining holes

These are proposed designs, not pre-registrations or completed experiments. Dataset selections,
thresholds, inclusion rules, decision criteria, and budgets must be frozen before new collection.

1. **Adjudicate oracle disagreements.** Sample accepted candidates independently of model/condition
   labels; have reviewers compare behavior against the supplied requirements and the oracle.
   Separate implementation defects, ambiguous requirements, oracle mismatches, and adapter errors.
   Define a candidate-level endpoint rather than subtracting a test-failure fraction from a
   binary false-accept rate.
2. **Test a specification-aware final reviewer.** Freeze candidate implementations, compare the
   existing test-centered GREEN review with direct full-specification review, and score both
   without altering candidates. Report precision, acceptance, and paired uncertainty.
3. **Separate feedback from verdicts.** Randomize feedback availability while holding reviewer
   verdicts or review budgets comparable. This can test whether reviewer feedback causes the
   observed generation gains.
4. **Randomize retry policy.** Compare retry budgets or record oracle outcomes before and after
   refinement on the same candidates. This addresses the selection bias in first-attempt versus
   retried-success groups.
5. **Broaden generators and repeat at application scale.** Use multiple generator families and
   repeat verifier/threshold comparisons with complete logging and retained failed attempts.
   Define comparable operating policies prospectively, rather than selecting a threshold after
   seeing acceptance outcomes.
6. **Reproduce neighboring methods.** A CodeT, ConVerTest, or supplied-test intervention on a
   common set of tasks could test transportability of their gains. Weaknesses in the original
   benchmark motivate this work; they do not predict that a reported effect must disappear.

Release positioning should invite these independent checks. A later instrument paper can center
on corpus design, oracle adjudication, and reproducibility if those become separately validated
contributions. The current evidence does not require announcing a multi-paper thesis or an
unmeasured benchmark superiority claim.
