# Manuscript review and revision — 2026-09-13

**Submission update:** arXiv confirmed “Article submitted” for **8074393**, with
status **processing**. See the [submission receipt](../release/arxiv-submission.json)
and [final upload record](ARXIV_UPLOAD.md). The route advice below predates the
original record’s server failures and the completed fresh submission.

The revised [paper](../paper/main.pdf) is defensible as an **author preprint about measured
pipeline verdict reliability**. The previous universal conclusion—stronger verification
cannot improve soundness—was not supported. The review preserves original model outputs and
oracle scores, corrects the reporting, and makes the remaining limitations explicit.

## Changes made

- **Use a consistent HumanEval oracle.** The previous headline table mixed original-test
  oracle passes and false rejects with HumanEval+ false accepts. The revised table and plot
  use the complete HumanEval+ matrix. Both complete matrices remain available in the
  [generated audit](../experiments/review_audit/results/ANALYSIS.md).
- **Separate non-significance from equivalence.** Abstract, results, captions, discussion,
  and conclusion now report residual errors and inconclusive contrasts. They acknowledge
  favorable point estimates instead of calling them flat or unchanged.
- **Separate oracle disagreement from specification violations.** The numbers-to-words
  example requires an exception type in the oracle that the visible requirements omit.
  The corrected figure and appendix identify this mismatch; historical requirements
  and scores have not been silently corrected.
- **Remove unsupported causal explanations.** Retry count and difficulty are observational
  groupings. The judge intervention changes feedback, gates, and generated candidates
  together, so the data do not isolate coaching or a harmful retry effect.
- **Correct uncertainty and calibration claims.** The new analysis resamples entire
  problems/packages with their repeated runs, reports paired conditional-rate uncertainty,
  and bounds the effect of missing oracle verdicts. Mutation adequacy and zero failures
  on selected adapter fixtures are no longer called semantic oracle error bounds.
- **Explain acceptance and abandonment.** A negative self-verdict can arise before final
  execution or any implementation. The pseudocode now includes termination at an exhausted
  GREEN gate. Lower false rejects at application scale accompany lower correct output.
- **Correct the threshold follow-up.** The analyzer now separates thresholds instead of
  pooling them. The manuscript identifies the adaptive follow-up, unequal acceptance,
  RED/GREEN joint threshold change, and nonmonotonic intermediate estimates.
- **Disclose analysis and provenance limits.** The original analyzers omit some paired
  tests and a control-spread adjustment. The supplement supplies post hoc checks without
  presenting them as prospective confirmations. Reconstructed history and deleted/repeated
  cross-provider attempts are explicitly disclosed.
- **Improve positioning and reproduction.** Added the oracle-problem and imperfect-verifier
  literature, corrected citation details, connected the context ablation, regenerated the
  data plots, and expanded the offline reproduction command to cover the later studies.
- **Restore the detailed illustrations.** The manuscript uses the original loop PNG and
  a corrected copy of the detailed requirements, generated-test, code, and oracle diagram.
  Their layout is preserved; the example's labels now distinguish an omitted exception
  type from a demonstrated model error. Both illustrations use the paper's normal
  portrait layout. See [figure sources](../paper/figures/README.md).
- **Audit the bibliography and current research.** Verified all 21 original entries and
  reviewed 26 additional primary sources through September 13, 2026. Added 18 references,
  including earlier self-test error measurements, methods that improve verification,
  and newer evidence of requirements–oracle mismatches. The revised Related Work limits
  novelty and conclusions to the measured protocol. See the [literature review](LITERATURE_REVIEW.md).

Detailed evidence: [statistical review](STATISTICAL_REVIEW.md),
[instrument review](INSTRUMENT_REVIEW.md), and [publication review](PUBLICATION_REVIEW.md).
The generated audit records input and runner hashes, source revision, execution time,
Python version, and resampling seed. Its numerical TeX macros are generated into the paper
directory so the submission source is self-contained.

## What remains unresolved

These issues cannot be repaired by wording or by recomputing saved scores:

1. **Semantic error rate on RGRBench is unknown.** Independently adjudicate accepted
   oracle failures against the exact visible requirements and adapter behavior, blinded
   to experimental condition. This is the highest-priority evidence upgrade before
   interpreting the full rate as agent misunderstanding.
2. **A direct reviewer baseline is missing.** Freeze existing candidates and evaluate a
   final reviewer given the full original specification. The current GREEN judge is
   asked to predict outcomes of generated tests and does not receive that full text.
   This baseline would address a major reviewer objection at lower cost than rerunning
   every generation experiment.
3. **Historical auditability remains incomplete.** Recover original protocol commits,
   exact source-tree mappings for recorded SHAs, and discarded attempts if available.
   The present checkout cannot establish their content or chronology.
4. **Broader claims require new experiments.** Generator diversity, randomized feedback
   ablation, and comparable weak/strong threshold curves remain future work. Register
   these prospectively rather than treating this review as registration.

No new benchmark model calls, benchmark-oracle executions, VPS jobs, or public
communications were performed during this review. The checks reanalyze retained
observations; they do not constitute an independent experimental replication.
The detailed illustration's labels were edited with the built-in image tool;
its source and prompt are recorded in the figure notes above.

## Validation and deliverables

- The existing instrument and asymmetry tests pass: **38 tests**.
- Each original analysis stage was run successfully: exp006, exp007, exp010, all four
  exp011 arms, and exp013. The audit and all six figure generators also completed.
  Stages were checked individually; a single uninterrupted `./reproduce.sh` execution
  was not completed because its initial cache approval was interrupted.
- Recomputed original outcome counts agree with the archived data. Regeneration updates
  timestamps/provenance and corrects stale spend headers; it does not change raw outcomes.
- The manuscript builds with Tectonic 0.17.0 and BibTeX, with no undefined references,
  undefined citations, overfull boxes, or duplicate PDF destinations. Remaining warnings
  concern underfull spacing. All 39 bibliography entries are cited and render successfully;
  all 23 pages use letter portrait dimensions with zero rotation. Long bibliography links
  wrap with `xurl` and remain clickable without colored outlines. The title page, result tables, and replacement figures were
  visually checked. The source archive also builds independently, and its extracted PDF
  text matches the reviewed PDF. Archive/source hashes were verified.
- [Local PDF](../release/self-grading-gap-reviewed.pdf),
  [self-contained TeX source](../release/self-grading-gap-reviewed-source.tar.gz),
  [revised abstract](../release/abstract.txt), and
  [submission comments](../release/submission-comments.txt) are prepared under `release/`,
  with file hashes and a source manifest. This revision has **23 pages, 6 figures, and 7 tables**.

## arXiv and public release

Keep **submit/7939730**. arXiv explicitly advises against deleting/resubmitting a held
submission because this causes further delays. Its moderation is not peer review, and
the hold alone does not identify a scientific defect. Use the
[tailored inquiry](PUBLICATION_REVIEW.md#arxiv-hold-recommended-next-action) to ask how to supply
the revision and whether the displayed **Primary: None** needs correction. That field's
cause is unknown. Based on subject matter, cs.SE is a sensible primary-category request
with cs.LG as a cross-list. See [official status guidance](https://info.arxiv.org/help/submit_status.html#on-hold)
and [moderation guidance](https://info.arxiv.org/help/moderation/index.html).

The related [context paper](https://arxiv.org/abs/2607.09691) is cited for independent
evaluation and controlled ablation methodology. It is not evidence that the present
pipeline results replicate. An arXiv posting also does not establish peer-reviewed status.

Release the corrected PDF and source as a dated author preprint, tied to an immutable
artifact revision. The [publication review](PUBLICATION_REVIEW.md) describes an optional
Zenodo DOI archive and contains a support-message draft. No submission or release has
been sent or published here.

Suggested community description:

> We instrumented a self-testing coding pipeline and compared its success claims with
> held-out tests. Stronger test authors and reviewers leave residual false accepts, while
> also changing correct output and acceptance. We release the retained runs, corrected
> oracle-specific analyses, and limitations, and invite independent replication and
> audits of requirements–oracle agreement.
