# Bibliography and research review

## Assessment

The literature supports studying the reliability of a coding agent's success claims. It
does not support treating persistent errors in one pipeline as a general limit on
self-verification. The strongest revision is to present *Who Grades the Grader?* as an
instrumented test-first study of role assignments, acceptance, rejection, and abandonment,
with an application-scale extension and explicit uncertainty about oracle fidelity.

The most important omission was prior work measuring the same kinds of self-test errors.
Chen et al. already analyze incorrect programs accepted by generated tests and correct
programs rejected by them. SFS also reports confusion accounting. These are substantive
antecedents, not merely neighboring code-generation systems.[^chen][^sfs]

There is direct positive evidence for better verification, including improved acceptance
precision, lower acceptance of known faulty programs, and trained reviewers evaluated on
fixed trajectories. These findings challenge an impossibility interpretation of the paper,
while leaving its recorded intervention results intact. Conversely, recent benchmark
audits show that an external failure can reflect an overly narrow test or an incomplete
requirement. Independent evidence remains useful, but independence does not establish
infallibility.[^swt][^solver][^swerm][^pro]

The review covers the 21 original bibliography entries and 26 additional primary sources,
including work posted in September 2026. The evidence inventory is broader than the
manuscript's citation list: sources were selected for the paper when they change its
interpretation, establish a close predecessor, or motivate a concrete comparison.

## The contribution that survives comparison

The general oracle problem is established software-testing research. Tests instantiate
only part of a behavioral contract, and their expected outcomes themselves need
justification. Practitioner terms such as the ugly mirror explain one failure pattern;
they are not evidence for its prevalence in modern agents.[^barr]

The paper's useful distinction is operational. An execution gate produces a verdict on a
specific generated implementation, and an external oracle supplies a second verdict.
Tracking both, including cases where a gate prevents implementation, reveals something
that a final benchmark pass rate alone cannot. The role interventions and application
packages provide the particular empirical contribution; the confusion matrix itself
does not establish methodological priority.

Ahmed et al.'s generated-test versus golden-test comparison is a close repository-scale
predecessor. Its refinement intervention should be discussed separately from this
paper's observational grouping by retry count. A difficult task that retries more often
does not establish that retries caused its failure.[^ahmed]

The phrase *verification gap* also appears in General AgentBench, where it describes a
shortfall between oracle pass@K and model selection of trajectories. The paper may use
the phrase with its own explicit definition, but should not imply ownership of the term
or equivalence between those metrics.[^general]

| Quantity | Denominator or evaluation unit | What it answers |
| --- | --- | --- |
| Conditional gap | Outputs accepted by the pipeline | How often does a declared success fail the chosen oracle? |
| False-positive rate on known negatives | Implementations already labeled incorrect | How often does a verifier miss a known fault? |
| Acceptance precision | Outputs retained by a filter | What fraction of accepted outputs are labeled correct? |
| Final pass rate | All evaluated tasks under a specified generation policy | How often does the system produce an oracle-passing output? |
| Oracle pass@K | All evaluated tasks, with K candidates per task | How much success is available to an ideal selector? |
| Discrimination and calibration | A fixed labeled set of candidates or trajectories | Do scores order correctness and reflect observed frequencies? |

These quantities cannot be pooled into a field-wide error percentage. Even precision
and the conditional gap are complements only when they use the same acceptance event,
labels, population, and treatment of missing outcomes. A verifier can raise precision by
rejecting more candidates while reducing the number of correct solutions delivered.

## Bibliographic accuracy and citation fit

All 21 original entries identify real sources. The main defects were stale publication
status, incomplete bibliographic fields, and overly broad descriptions of what a source
measured. The [entry-by-entry audit](research/bibliography_audit.md) records primary
publisher, proceedings, arXiv, and publisher-deposited metadata for every entry.

| Reference | Correction or clarification |
| --- | --- |
| Mathews and Nagappan | Use the published ASE 2024 title, *Test-Driven Development and LLM-based Code Generation*, rather than the earlier preprint title. |
| LiveCodeBench | Cite the ICLR 2025 publication; the internal key can retain its historical 2024 year. |
| Ahmed et al. | Cite the FSE 2026 Ideas, Visions and Reflections publication. |
| CodeJudgeBench | Cite ACL 2026. Its evaluated Claude 4 models still do not supply results for Claude 4.5. |
| TDFlow | Cite EACL 2026; preserve the distinction between supplied-test and generated-test experiments. |
| Jin and Chen | Cite ASE 2025 NIER and describe the measured false rejection of correct code. |
| ConVerTest | Cite ICST 2026. |
| Stroebl et al. | Cite ICLR 2026 while retaining the earlier title/version history. |
| TENET | Identify its current version and reported ISSRE 2026 acceptance; do not invent final proceedings details. |
| HumanEval | The original entry existed but was not cited, so it did not appear in the rendered bibliography. Add it separately from EvalPlus. |

The distinction between publication year and first posting matters. A citation key is
only an internal label; renaming keys solely to match updated years would create noise.
Version pinning matters more when titles, authors, datasets, or reported results change.
Accepted future-conference papers remain distinguishable from completed proceedings
publications. No withdrawal or retraction notice was visible in the inspected records;
that is a bounded records check, not a guarantee about every possible index.

Citation use also needed refinement. TiCoder combines a small human study with a
separate scaled evaluation using idealized feedback; those are different evidence
sources. TENET relies on developer-written tests. TDFlow studies distinct supplied and
generated testing regimes. None should be summarized as having measured the conditional
error rate of the present autonomous acceptance loop.[^ticoder][^tenet][^tdflow]

The connection to the context-ablation paper remains appropriate as methodology: fixing
localization and varying representation while checking external outcomes complements
the present test-authorship intervention. It is neither a replication nor independent
validation of the verification-gap estimates.[^context]

## Evidence reinforcing the need for external checks

### Earlier self-test and benchmark studies

The strongest historical comparison is a sequence of different questions, not one
continuous benchmark leaderboard. Chen et al. examine self-debugging with generated
tests; Ahmed et al. evaluate generated-test-passing repository patches; UTBoost and
PatchDiff question benchmark oracles. Their agreement is that apparent success can
survive inadequate evaluation. Their populations and truth standards differ.

UTBoost's augmentation results apply to selected tasks with insufficient tests. Its
reported newly exposed errors also involve fixes to evaluation machinery. This makes it
useful support for auditing both a suite and its harness, but unsuitable for importing an
error percentage into RGRBench.[^utboost]

PatchDiff reports behavioral disagreement for 260 of 877 plausible patches. The essential
qualification is its manual sample: of 77 suspicious patches, 22 were classified
incorrect, four correct, and 51 uncertain. Calling the full disagreement rate a confirmed
semantic-error rate would repeat the interpretation problem the revised paper now
avoids.[^patchdiff]

### Application-scale evidence

BackendForge is a particularly relevant July 2026 addition because it evaluates backend
services rather than only standalone algorithms. Its strongest model passes 31 of 56
tasks with the base oracle and 16 with the strengthened oracle. The authors also reject
candidate assertions that exceed the visible contract. The lesson concerns both finding
missing cases and checking whether a proposed test is justified.[^backend]

This is an application-scale comparison of two external oracles. It does not reproduce
the paper's self-verdict experiment, establish that RGRBench has the same defect rate, or
show that every stronger suite is better. Its contract-review procedure is a useful
design precedent for a future RGRBench audit.

### Tests that inherit implementation errors

Zhao, Zhou, and Cohen study tests that pass buggy code and fail its fixed counterpart.
Supplying buggy implementations increases this misleading-test behavior, while a
specification-based intervention mitigates it. The paired outcome definition is more
informative than labeling every test that passes buggy code as misguided.[^misguidance]

This is direct evidence for a code-conditioned mechanism. The present pipeline starts
with tests before an implementation exists, so the mechanism cannot simply be copied
into its explanation. Later feedback can introduce implementation dependence, but
establishing that causal pathway would require a separate intervention or trace audit.

Their companion replication study also cautions against treating coverage as a universal
quality proxy. It distinguishes tests generated from correct code from tests intended to
expose existing bugs and finds useful mutation associations in some settings. It does
not establish universal uselessness of coverage or mutation scores, and does not measure
RGRBench's semantic oracle error.[^coverage]

## Evidence that constrains pessimistic conclusions

| Study | Evidence relevant to the paper | Boundary on the inference |
| --- | --- | --- |
| SWT-Bench, NeurIPS 2024 | Generated-test filtering raises accepted-fix precision to 47.8%, at 20% recall. | Filtering quality and retained correct output must be reported together; this is not merely a generation pass-rate result. |
| Sol-Ver, inspected March 2026 revision | Acceptance of known flawed solutions falls from 12.75% to 9.60% on MBPP and 20.76% to 18.63% on LiveCodeBench. | The denominator is known faulty solutions. Training changes the solver and test generator, unlike a fixed-generator model swap. |
| CodeHacker, ACL 2026 | Calibrated adversarial augmentation improves rejection of submissions labeled incorrect. | Reference solutions and human-checked validation infrastructure supply information absent from a wholly self-authored loop. |
| SWE-RM, ICLR 2026 | Evaluates learned scores on fixed trajectories using AUC, calibration error, and selected-solution accuracy. | Ranking, probability calibration, and a deployed acceptance threshold are separate questions. |
| RETRACE, August 2026 | Reconstructs the issue from a patch without the original issue, reconciles both directions, and improves final resolution. | It uses the same backbone and changes the patch; it does not isolate fixed-patch verdict accuracy. |
| ReVeal, ICLR 2026 | Explicit training for self-verification makes iterative refinement useful. | Its training supervision and verification rewards differ from the present prompted policy. |
| TCS, September 3, 2026 | Trains reference consistency and adversarial discrimination in stages and improves test-based selection. | The reported acceptance notice is for forthcoming Findings of EMNLP; reliable-reference assumptions and selection endpoints must remain explicit. |

Sources and result locations for the table are the original papers, not comparative
marketing summaries.[^swt][^solver][^codehacker][^swerm][^retrace][^reveal][^tcs]

These are not interchangeable remedies. Some change training, some introduce reference
information, some select among several candidates, and some revise the output. A model
substitution inside the current rubric tests only one part of this design space. The
paper should therefore say that the tested role changes leave residual errors with
uncertain effects on their rate—not that verification quality is invariant to effort or
model capability.

Nor does improvement establish complete reliability. A method can reduce known-negative
acceptance while retaining substantial error among deployment successes, especially when
task prevalence or selection changes. The constructive implication is to evaluate
promising verification procedures with the paper's explicit acceptance accounting.

## Evidence that the external oracle also needs review

SWE-Bench Pro Verified, posted September 8, identifies overly narrow tests and misleading
descriptions among its refined tasks. Its contract repairs and anti-leakage measures are
separate interventions. The selected cases establish examples of evaluation problems,
not their unbiased prevalence across all tasks.[^pro]

OpenAI's February and July 2026 benchmark audits provide additional primary evidence,
with vendor authorship and selection procedures explicitly acknowledged. The February
report's 59.4% concerns 138 difficult audited tasks, not all 500 SWE-bench Verified
instances. The July report likewise combines screening and human review rather than a
random sample. Neither supplies a numerical correction factor for the present
paper.[^openai-feb][^openai-jul]

An August study of exception-oracle generation is closely relevant to the type mismatch
in the paper's illustration. It finds that documentation and structural code cues affect
specialized oracle models differently. This motivates testing whether a model follows the
stated contract; it does not show that the present frontier judge used the same shortcut
or caused the omission.[^exceptions]

Ma and Eisty's July pilot separately compares generated test oracles with a
requirement-derived reference and the system under test. Its small single-component
sample and exclusion of non-compiling outputs limit generalization. Its value here is
the separation of targets: agreement with an implementation and agreement with a
requirement are not the same outcome.[^requirements]

The `numbers_to_words` interpretation should therefore remain unchanged: the visible
requirement specifies an error message but omits an exception type. The held-out oracle
adds `ValueError`. The observed failure is oracle-relative; the example alone does not
establish a violation of the visible requirement. Wider literature reinforces this
qualification rather than licensing dismissal of all observed failures as benchmark noise.

## Formal verification and the newest adjacent work

VERINA is a useful constructive addition because it separately evaluates generated code,
specifications, and proofs, including checks against reference specifications. Proofs can
strengthen assurance about a formal contract, but translating the intended requirement
into that contract remains an evaluation target. Failed proof search must not be counted
as demonstrated incorrectness.[^verina]

IdeaAMBIG, posted September 9, is an especially recent clarification study. It concerns
research-method specifications, with oracle-provided resolutions and a small executable
component study. Those results motivate investigating requirement clarification but do
not establish autonomous discovery and repair of missing application requirements. It is
included in the review rather than added as a distant benchmark citation in the
manuscript.[^idea]

Several additional verified papers broaden the follow-up design space:

- **μCODE:** learned verifier scores complement execution feedback in trained multi-turn
  generation. The reported endpoint is final output quality.[^mucode]
- **Agentic Verifier:** searches for discriminating inputs and improves candidate
  selection. Its Best@K is the score of a selected answer, not oracle pass@K.[^agentic]
- **LLM-as-a-Verifier:** studies repeated, decomposed judgments over diverse candidate
  trajectories. Diversity and inference procedure matter alongside model size.[^llmverifier]
- **Verification Limits Code LLM Training:** studies verification when constructing
  synthetic training data. Its selection-versus-diversity tradeoff is conceptually close,
  but its outcome is downstream training quality rather than runtime acceptance
  reliability.[^training]

These papers are retained in the evidence inventory without expanding the manuscript
into a general survey of all verifier methods. SFS is cited in the manuscript because
its earlier confusion accounting directly affects the contribution's positioning.

## Manuscript changes warranted by the evidence

The revised Related Work section gives explicit credit to prior self-test error
measurements. It separates benchmark adequacy, self-debugging, test-first generation,
generated-test filtering, trained reviewers, and formal specification evaluation.
The contribution statement emphasizes instrumentation and gate abandonment rather than
introducing confusion accounting as a new concept.
The introduction also replaces unsupported claims about deployment prevalence and a
general failure mechanism with the interventions and outcomes actually studied.

The positive verifier studies are included alongside negative results. Direct acceptance
evidence receives priority over headline pass-rate improvements. The discussion of a
future fixed-candidate reviewer comparison now has concrete precedents in learned
trajectory scoring and reconstruction-based verification.

The oracle limitations are also connected to newer empirical work. Coverage, mutation,
reference divergence, exception-type prediction, and requirements repair each answer
different questions. Their presence in a benchmark cannot substitute for adjudicating
whether a disputed implementation violates the input contract.

Bibliography metadata is updated without renaming existing keys. Eighteen references are
added, bringing the bibliography to 39 entries. HumanEval receives its missing citation.
The abstract's accessible wording, experimental outcomes, and portrait
figure layout are preserved. These are literature and interpretation changes, not new
benchmark measurements.

## Highest-value follow-up experiments

**First, adjudicate existing accepted failures against the exact visible contract.**
Reviewers should be blinded to the experimental condition and distinguish demonstrated
implementation defects, omitted requirements, overly narrow assertions, adapter failures,
and unresolved cases. Use multiple reviewers and record disagreements. Preserve the
historical scores; any repaired contract becomes a separately frozen evaluation version.
This would strengthen interpretation of the application-scale headline more directly
than adding another undifferentiated model swap.

**Second, freeze candidates and compare verification procedures.** Give reviewers the
same full original specification and candidate pool. Compare the current rubric with a
specification-aware reviewer, a reconstruction procedure, and an adversarial execution
procedure. Report both off-diagonal errors, acceptance, correct outputs retained, missing
verdicts, calibration where scores exist, and cost. Predefine thresholds or evaluate
coverage–risk curves rather than selecting a favorable threshold afterward.

**Third, separate feedback from selection.** A factorial design can hold the gate decision
fixed while changing whether its feedback reaches the generator, and separately hold
candidates fixed while comparing gate decisions. This would test whether useful coaching
and reliable rejection come from the same intervention. Repeating only the existing
observational retry grouping cannot answer that causal question.

These are proposed follow-ups. The reviewed literature does not establish their effects
in the present pipeline, and no new model runs or external experiments were performed for
this review.

## Coverage and remaining uncertainty

The cutoff is September 13, 2026. The review used primary papers, official proceedings,
publisher-deposited metadata, author manuscripts, and clearly labeled first-party research
reports. It followed references and newer versions across self-debugging, generated tests,
learned verification, repository benchmarks, requirements, and formal specifications.
It is a targeted narrative review, not an exhaustive systematic search supporting a
universal priority claim.

Anonymous OpenReview manuscripts about additional agent tests and proof-based benchmark
evaluation were discovery leads. Stable author/date/status information was insufficient
for adding them as established manuscript references. Secondary summaries and anecdotes
were not used as research evidence. Future updates should check those records and newly
published proceedings, rather than treating a present access failure as proof of absence.

External numerical findings remain source-reported. They were checked against primary
methods and tables, but their experiments were not independently rerun. Different
benchmarks, repeated-trial policies, incomplete labels, and selected audit samples prevent
a pooled effect size or a claim that any particular new method will close this pipeline's
gap.

## Sources

The [complete original-entry audit](research/bibliography_audit.md) provides the 21-source
metadata inventory. The companion [supporting-evidence inventory](research/recent_supporting_evidence.md),
[counterevidence inventory](research/counterevidence_and_novelty.md), and
[specification review](research/specifications_and_formal_verification.md) record versions,
full-text locations, and inclusion decisions for the additional sources.

1. Xiancai Chen et al. *Revisit Self-Debugging with Self-Generated Tests for Code Generation*. ACL 2025. [Paper](https://aclanthology.org/2025.acl-long.881/).
2. Jonathan Light et al. *SFS: Smarter Code Space Search Improves LLM Inference Scaling*. ICLR 2025. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/387982dbf23d9975c7fc45813dd3dabc-Abstract-Conference.html).
3. Toufique Ahmed et al. *Investigating Test Overfitting on SWE-bench*. FSE 2026, Ideas, Visions and Reflections. [Publication](https://doi.org/10.1145/3803437.3805574).
4. Niels Mündler et al. *SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents*. NeurIPS 2024; inspected v3. [Paper](https://arxiv.org/abs/2406.12952v3).
5. Zi Lin et al. *Learning to Solve and Verify: A Self-Play Framework for Code and Test Generation*. Preprint, 2025; inspected March 2026 v4. [Paper](https://arxiv.org/abs/2502.14948v4).
6. Jingwei Shi et al. *CodeHacker: Automated Test Case Generation for Detecting Vulnerabilities in Competitive Programming Solutions*. ACL 2026. [Paper](https://aclanthology.org/2026.acl-long.108/).
7. KaShun Shum et al. *SWE-RM: Execution-free Feedback For Software Engineering Agents*. ICLR 2026; quantitative source inspected: arXiv v1. [Version](https://arxiv.org/abs/2512.21919v1).
8. Chenglin Li et al. *Independent Patch Verification for Coding Agents with a Bidirectional Reconstruct-and-Verify Framework*. August 2026 preprint. [Paper](https://arxiv.org/abs/2608.08950v1).
9. Yiyang Jin et al. *ReVeal: Self-Evolving Code Agents via Reliable Self-Verification*. ICLR 2026; inspected arXiv v2. [Version](https://arxiv.org/abs/2506.11442v2).
10. Jiacheng Xu et al. *Two-Stage Reinforcement Learning for Sound and Adversarial Test Generation in Code LLMs*. September 2026 preprint; reports Findings of EMNLP 2026 acceptance. [Paper](https://arxiv.org/abs/2609.03955v1).
11. You Wang, Michael Pradel, Zhongxin Liu. *Are “Solved Issues” in SWE-bench Really Solved Correctly? An Empirical Study*. ICSE 2026; inspected v2. [Paper](https://arxiv.org/abs/2503.15223v2).
12. Boxi Yu et al. *UTBoost: Rigorous Evaluation of Coding Agents on SWE-Bench*. ACL 2025. [Paper](https://aclanthology.org/2025.acl-long.189/).
13. Yuzhe Guo et al. *BackendForge: Benchmarking Agentic End-to-End Code Generation with Backend Services*. July 2026 preprint. [Paper](https://arxiv.org/abs/2607.11042v1).
14. Junda Zhao, Shurui Zhou, Eldan Cohen. *Evaluating and Mitigating the Misguidance Effect of Buggy Code in LLM-Generated Unit Tests*. ISSTA 2026, public July 2026. [Paper](https://arxiv.org/abs/2607.22883v1).
15. Junda Zhao, Shurui Zhou, Eldan Cohen. *Do Coverage and Mutation Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability Study)*. ISSTA 2026, public July 2026. [Paper](https://arxiv.org/abs/2607.22880v1).
16. Pujun Zheng et al. *SWE-Bench Pro Verified: A Reliable Benchmark for Software Engineering Agents*. September 2026 preprint. [Paper](https://arxiv.org/abs/2609.08149v1).
17. Soneya Binta Hossain, Matthew B. Dwyer, Tasfia Tasnim. *Documentation vs. Code Patterns: What Drives LLM-Based Exception Oracle Generation?* August 2026 preprint carrying forthcoming ASE 2026 metadata. [Paper](https://arxiv.org/abs/2608.00884v1).
18. OpenAI. *Why SWE-bench Verified No Longer Measures Frontier Coding Capabilities*. February 23, 2026 research report. [Report](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/).
19. OpenAI. *Separating Signal from Noise in Coding Evaluations*. July 8, 2026 research report. [Report](https://openai.com/index/separating-signal-from-noise-coding-evaluations/).
20. Zhe Ye et al. *VERINA: Benchmarking Verifiable Code Generation*. ICLR 2026. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/41b8c80f9113b9f8e2e129447221682a-Abstract-Conference.html).
21. Xiaochuan Li et al. *Benchmark Test-Time Scaling of General LLM Agents*. February 2026 preprint. [Paper](https://arxiv.org/abs/2602.18998v1).
22. Tiancheng Ma, Nasir U. Eisty. *From Business Requirements to Test Assertions: Evaluating LLM-Generated Oracles on Real Bugs*. July 2026 preprint. [Paper](https://arxiv.org/abs/2607.10277v1).
23. Yiling Ma et al. *IdeaAMBIG: Benchmarking Implementation-Critical Gaps in Research-Idea Specifications*. September 9, 2026 preprint. [Paper](https://arxiv.org/abs/2609.10539v1).
24. Arnav Kumar Jain et al. *Multi-Turn Code Generation Through Single-Step Rewards*. ICML 2025. [Proceedings paper](https://raw.githubusercontent.com/mlresearch/v267/main/assets/jain25a/jain25a.pdf).
25. Zeyao Ma et al. *Scaling Agentic Verifier for Competitive Coding*. February 2026 preprint. [Paper](https://arxiv.org/abs/2602.04254v1).
26. Jacky Kwok et al. *LLM-as-a-Verifier: A General-Purpose Verification Framework*. July 2026 preprint, v2. [Paper](https://arxiv.org/abs/2607.05391v2).
27. Srishti Gureja et al. *Verification Limits Code LLM Training*. September 2025 preprint, inspected v1. [Paper](https://arxiv.org/abs/2509.20837v1).
28. Earl T. Barr et al. *The Oracle Problem in Software Testing: A Survey*. IEEE TSE 2015. [Publication](https://doi.org/10.1109/TSE.2014.2372785).
29. Sarah Fakhoury et al. *LLM-Based Test-Driven Interactive Code Generation: User Study and Empirical Evaluation*. IEEE TSE 2024. [Publication](https://doi.org/10.1109/TSE.2024.3428972).
30. Yiran Hu et al. *TENET: One Step Toward Test-Driven Development for Repository-Level Code Generation*. v4, reported ISSRE 2026 acceptance. [Version](https://arxiv.org/abs/2509.24148v4).
31. Kevin Han et al. *TDFlow: Agentic Workflows for Test Driven Development*. EACL 2026. [Paper](https://aclanthology.org/2026.eacl-long.70/).
32. Brian Sam-Bodden. *What Context Does a Coding Agent Actually Need to Act?* 2026 preprint. [Paper](https://arxiv.org/abs/2607.09691).

[^chen]: Chen et al., ACL 2025, §3.3 and Figure 3. [Full text](https://aclanthology.org/2025.acl-long.881.pdf).
[^sfs]: Light et al., ICLR 2025, Appendix I, Table 18. [Full text](https://proceedings.iclr.cc/paper_files/paper/2025/file/387982dbf23d9975c7fc45813dd3dabc-Paper-Conference.pdf).
[^ahmed]: Ahmed et al., FSE 2026. [Publication](https://doi.org/10.1145/3803437.3805574).
[^swt]: Mündler et al., NeurIPS 2024, §5.3. [Full text, v3](https://arxiv.org/pdf/2406.12952v3).
[^solver]: Lin et al., inspected v4, §4.1 and Table 1. [Full text](https://arxiv.org/pdf/2502.14948v4).
[^codehacker]: Shi et al., ACL 2026, Tables 1/5 and Appendix E. [Full text](https://aclanthology.org/2026.acl-long.108.pdf).
[^swerm]: Shum et al., inspected arXiv v1, §4.1/Table 4. [Full text](https://arxiv.org/pdf/2512.21919v1).
[^retrace]: Li et al., August 2026, Table 1 and ablations. [Full text](https://arxiv.org/pdf/2608.08950v1).
[^reveal]: Jin et al., inspected v2, §3/Table 1. [Full text](https://arxiv.org/pdf/2506.11442v2).
[^tcs]: Xu et al., September 2026, §4/Table 1. [Full text](https://arxiv.org/pdf/2609.03955v1).
[^patchdiff]: Wang et al., inspected v2, §§4.2/4.4, Tables 2/8. [Full text](https://arxiv.org/html/2503.15223v2).
[^utboost]: Yu et al., ACL 2025, §§4.1–4.2. [Full text](https://aclanthology.org/2025.acl-long.189.pdf).
[^backend]: Guo et al., July 2026, §§3.4/4.2/5.2. [Full text](https://arxiv.org/html/2607.11042v1).
[^misguidance]: Zhao et al., July 2026, §2.2 and Tables 2/4/6. [Full text](https://arxiv.org/html/2607.22883v1).
[^coverage]: Zhao et al., July 2026, §3.1 footnote 1, §§5.4/6. [Full text](https://arxiv.org/html/2607.22880v1).
[^pro]: Zheng et al., September 2026, §3.1.2/Table 2 and §4.4. [Full text](https://arxiv.org/html/2609.08149v1).
[^exceptions]: Hossain et al., August 2026, §§3.2–3.4, Tables 2/5/6/9. [Full text](https://arxiv.org/html/2608.00884v1).
[^openai-feb]: OpenAI, February 23, 2026, selected-task audit. [Primary report](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/).
[^openai-jul]: OpenAI, July 8, 2026, screening and adjudication procedures. [Primary report](https://openai.com/index/separating-signal-from-noise-coding-evaluations/).
[^verina]: Ye et al., ICLR 2026, §4.1 and Appendix C.5. [Full text](https://arxiv.org/html/2505.23135v3).
[^general]: Li et al., February 2026, §§4.1–4.3. [Full text](https://arxiv.org/html/2602.18998v1).
[^requirements]: Ma and Eisty, July 2026, §§4–6. [Full text](https://arxiv.org/html/2607.10277v1).
[^idea]: Ma et al., September 2026, §4.4 and Appendix D.4. [Full text](https://arxiv.org/html/2609.10539v1).
[^mucode]: Jain et al., ICML 2025, §4/Table 3. [Full text](https://raw.githubusercontent.com/mlresearch/v267/main/assets/jain25a/jain25a.pdf).
[^agentic]: Ma et al., February 2026, §4/Table 1. [Full text](https://arxiv.org/pdf/2602.04254v1).
[^llmverifier]: Kwok et al., July 2026, §5.2/Table 3. [Full text](https://arxiv.org/pdf/2607.05391v2).
[^training]: Gureja et al., inspected v1, §§4–6. [Full text](https://arxiv.org/pdf/2509.20837v1).
[^barr]: Barr et al., IEEE TSE 41(5), 507–525, 2015. [Publication](https://doi.org/10.1109/TSE.2014.2372785).
[^ticoder]: Fakhoury et al., IEEE TSE 50(9), 2254–2268, 2024. [Publication](https://doi.org/10.1109/TSE.2024.3428972).
[^tenet]: Hu et al., inspected v4. [Version record](https://arxiv.org/abs/2509.24148v4).
[^tdflow]: Han et al., EACL 2026. [Publication](https://aclanthology.org/2026.eacl-long.70/).
[^context]: Sam-Bodden, 2026. [Primary preprint](https://arxiv.org/abs/2607.09691).
