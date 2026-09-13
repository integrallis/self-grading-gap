# Recent primary evidence: self-tests, oracle adequacy, and specification mismatch

Review cutoff: **2026-09-13**. This is a targeted literature review, not a systematic review. Full text was inspected for all ten main sources below. Citation-ready records are in [supporting_additions.bib](supporting_additions.bib). The revised manuscript cites the first eight; the two corporate reports remain supporting material in the [literature review](../LITERATURE_REVIEW.md).

The most consequential omission is Chen et al. (ACL 2025): self-generated-test false positives and false negatives already have a directly comparable operationalization. The defensible contribution here is the test-first workflow, crossed verifier-role interventions, and application-scale oracle-disagreement evaluation. Recent external-benchmark audits reinforce the need for independent evidence while also qualifying what an oracle failure establishes. They are not replications of this paper's conditional false-accept rate.

## Ten sources to prioritize

### 1. Chen et al., ACL 2025 — direct novelty overlap

**Key:** `chen2025revisit`. Published July 2025; arXiv first posted January 22, 2025. Use the final ACL author list, which includes Xinyu Zhang.

**Evidence location:** §3.3, Figure 3, pp. 18007–18008; Appendix Figure 6. They explicitly distinguish flawed programs accepted by generated tests from correct programs rejected by them, using external labels. Table 1 reports both improvements and regressions from self-debugging across model/feedback settings. Thus neither the confusion-matrix concept nor the existence of misleading self-test feedback is new here. [Final paper and metadata](https://aclanthology.org/2025.acl-long.881/), [full PDF](https://aclanthology.org/2025.acl-long.881.pdf).

**Comparison:** Their code-first self-debugging study does not reproduce our test-first role-crossing intervention or application adapters. Cite prominently in Related Work and contribution framing; do not claim the first measurement of a self-verification gap.

### 2. Zhao, Zhou, and Cohen, ISSTA 2026 — tests inherit buggy behavior

**Key:** `zhao2026misguidance`. Public July 24, 2026; accepted ISSTA/PACMSE article ISSTA113.

**Evidence location:** §2.2 uses 318 Defects4J focal methods; Table 2 defines misguided tests as passing buggy code but failing its fixed counterpart. Table 4's model-average misguided-test fraction rises from 0.46% with fixed input to 3.84% with buggy input; effective tests fall from 8.51% to 2.98%. Table 6 evaluates replacing the implementation with a generated behavioral docstring, demonstrating mitigation rather than inevitability. [Full paper](https://arxiv.org/html/2607.22883v1), [metadata/DOI](https://arxiv.org/abs/2607.22883v1).

**Comparison:** This directly supports implementation-conditioned error propagation, but operates code-first and labels individual tests against paired code versions. Our test-first ordering removes that particular initial conditioning path; shared specification interpretation remains a hypothesis, not a mechanism established by their experiment or ours.

### 3. Wang, Pradel, and Liu, PatchDiff — benchmark passes can conceal defects

**Key:** `wang2025patchdiff` (retains first-publication year in key). First posted March 19, 2025; inspected version 2, September 9, 2025, carrying ICSE 2026 proceedings metadata and DOI 10.1145/3744916.3764576.

**Evidence location:** §4.1/Table 1: 7.8% mean of originally plausible patches fail the full developer suites across three agents. §4.2/Table 2: 260/877 patches (29.6%) differ behaviorally from the reference under additional tests. Crucially, §4.4/Table 8 manually inspects 77 suspicious patches: 22 incorrect, four correct, and 51 uncertain. **29.6% is disagreement, not a verified semantic-error prevalence.** [Full paper](https://arxiv.org/html/2503.15223v2), [version metadata](https://arxiv.org/abs/2503.15223v2).

**Comparison:** Supports oracle incompleteness, while illustrating why reference disagreement needs adjudication. Their denominator is benchmark-passing repository patches, not our internally accepted runs. Use beside EvalPlus, with this distinction explicit.

### 4. Yu et al., UTBoost, ACL 2025 — inadequate tests and evaluation bugs

**Key:** `yu2025utboost`. Final ACL proceedings, July 2025; first arXiv posting June 10.

**Evidence location:** §4.2, p. 3767: on selected tasks found to have insufficient tests, augmentation invalidates 170/599 previously passing Lite patches (28.4%) and 92/584 Verified patches (15.7%). These are **conditional subsets**, not all patches submitted to either benchmark. §4.1 describes manual review; the conclusion's total 345 newly exposed wrong patches also includes evaluation-parser fixes. [Final paper and metadata](https://aclanthology.org/2025.acl-long.189/), [full PDF](https://aclanthology.org/2025.acl-long.189.pdf).

**Comparison:** Establishes two separate failure sources—test coverage and evaluation machinery. Its independently reviewed differentiating tests are useful counterevidence against the claim that generated tests cannot improve verification. It does not establish that our adapter has a particular error rate.

### 5. Guo et al., BackendForge — application-scale oracle strengthening

**Key:** `guo2026backendforge`. Version 1, July 13, 2026; preprint.

**Evidence location:** §4.2/Table 2: GPT-5.5 xhigh passes 31/56 backend-service tasks (55.36%) under the base oracle and 16/56 (28.57%) under the final oracle. §5.1 adds 640 tests to 7,250 original tests. §3.4 and §5.2 audit proposed assertions against the visible contract and reject 113 candidate tests, including unsupported requirements. [Full paper](https://arxiv.org/html/2607.11042v1), [metadata](https://arxiv.org/abs/2607.11042v1).

**Comparison:** Especially relevant to RGRBench's application setting, but the comparison is base versus strengthened external HTTP oracles, not self-verdict versus oracle. The contract review matters as much as test growth. Do not use §5.3's DeepSeek improvement without resolving its starting-count inconsistency with Table 2.

### 6. Zhao, Zhou, and Cohen, ISSTA 2026 — proxy metrics need context

**Key:** `zhao2026coverage`. Public July 24, 2026; accepted ISSTA/PACMSE article ISSTA002.

**Evidence location:** §3.4 reports 8,268 suites/101,123 tests. §5.4 and Figure 4 show coverage losing usefulness for bug detection when supplied code is buggy, including a test that adopts erroneous equality behavior. §6/Tables 13–14 also find useful mutation-score correlations in regression-style settings with correct source. §3.1 footnote 1 explicitly **does not run mutation analysis on buggy-input detection**, because requiring a green suite excludes the bug-revealing tests. [Full paper](https://arxiv.org/html/2607.22880v1), [metadata](https://arxiv.org/abs/2607.22880v1).

**Comparison:** Supports caution around test-volume telemetry and mutation-based calibration; does not establish universal proxy uselessness or measure our adapter's error. It shares authors, benchmark, and model settings with source 2, so do not portray them as independent replications of the same claim.

### 7. Zheng et al., SWE-Bench Pro Verified — newest specification/oracle audit

**Key:** `zheng2026sweproverified`. Version 1, September 8, 2026; preprint.

**Evidence location:** §3.1.2/Table 2 classifies the 102 refined tasks: 75 overly narrow tests, 22 misleading descriptions, three insufficiently restrictive test sets, two other defects. §3.3 describes human final edits. §4.4/Table 9 shows 92 tasks receiving requirement edits and 17 receiving test-patch edits; overlap is permitted. This is contract repair, not simply adding tests. [Full paper](https://arxiv.org/html/2609.08149v1), [metadata](https://arxiv.org/abs/2609.08149v1).

**Comparison:** Closely supports the need to adjudicate the RGRBench exception-type mismatch. Tasks were selected from public issue evidence, so this is not an unbiased prevalence estimate across 731 tasks. Anti-leakage changes are a separate intervention; combined score changes cannot isolate oracle repair.

### 8. Hossain, Dwyer, and Tasnim — exception-oracle shortcut evidence

**Key:** `hossain2026exceptionpatterns`. Public August 1, 2026; ASE 2026 proceedings metadata appears in the paper, but the October conference is after this review cutoff.

**Evidence location:** §3.2/Table 2: removing Javadoc exception clauses changes overall accuracy by less than one percentage point. §3.3/Tables 5–6: 97.81% of TOGLL's layer-6 first-flip tokens are structural. **Qualification:** §3.4/Table 9 gives only 23.44% structural tokens for Doc2OracLL on the same benchmark; cue reliance differs substantially. [Full paper](https://arxiv.org/html/2608.00884v1), [metadata](https://arxiv.org/abs/2608.00884v1).

**Comparison:** Warns against interpreting exception prediction accuracy as demonstrated semantic grounding. It studies specialized models of roughly 110M–7B parameters, not our frontier judges. Token substitutions do not establish that our observed exception mismatch arose from this mechanism.

### 9. OpenAI, February 2026 — external oracles can reject valid alternatives

**Key:** `openai2026verifiedaudit`. Primary corporate research report, February 23, 2026; not a peer-reviewed paper.

**Evidence location:** “Too narrow and too wide tests”: 59.4% of 138 audited tasks have material evaluation issues, including 35.5% with overly restrictive tests and 18.8% with unspecified requirements. The 138 were selected for difficulty using repeated o3 runs, and each was reviewed by multiple engineers. **59.4% does not describe the entire 500-task benchmark.** [Primary report](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/).

**Comparison:** Supports keeping oracle-relative failure separate from violation of the visible requirement. Selection, vendor authorship, and adjudication conventions limit generalization; this is corroborating audit evidence, not a calibration correction for our data.

### 10. OpenAI, July 2026 — specification disagreements persist in SWE-bench Pro

**Key:** `openai2026codingsignal`. Primary corporate research report, July 8, 2026; not peer reviewed.

**Evidence location:** The report describes 286 initially screened candidates, 200/731 tasks flagged by a deeper human-supervised agent review, and 249/731 by a separate multi-engineer process; its approximately 30% characterization is an audit estimate. Examples distinguish overspecific tests, missing instructions, insufficient coverage, and contradictory requirements. These screened procedures and partially disagreeing judgments are not a random-sample prevalence study. [Primary report](https://openai.com/index/separating-signal-from-noise-coding-evaluations/).

**Comparison:** Useful context for the later independent Pro Verified curation. It supports manual contract adjudication in a follow-up RGRBench study, not an inference that our observed disagreement is entirely oracle noise.

## Recommended exact manuscript edits

These are proposed insertions, not claims that additional experiments were performed.

1. **Related Work / novelty paragraph, mandatory:** “Chen et al. already distinguish incorrect programs accepted by self-generated tests from correct programs rejected by them in code-first self-debugging. Our contribution is a test-first study that crosses verifier roles and extends oracle-disagreement measurement to application packages.” Add `\cite{chen2025revisit}` after the first sentence.

2. **Discussion of shared errors:** “Experiments with paired buggy and fixed implementations show that supplying buggy code can induce tests that validate its errors, while specification-based prompting can mitigate that effect. Our test-first design removes that initial implementation-conditioning path; it does not by itself identify why later disagreements occur.” Add `\cite{zhao2026misguidance}` after sentence one.

3. **Related Work / benchmark audits:** “SWE-bench audits expose incomplete tests and evaluation errors, while BackendForge demonstrates large score changes after contract-reviewed oracle strengthening. These evaluate external-oracle adequacy, a different comparison from our internal-verdict disagreement.” Cite `wang2025patchdiff,yu2025utboost,guo2026backendforge` after sentence one.

4. **RGRBench limitations, near the exception example:** “Recent benchmark audits also repair requirements and overly restrictive assertions. An independent oracle therefore supplies additional evidence, but its failure is not automatically proof of violating the supplied specification.” Cite `zheng2026sweproverified,openai2026verifiedaudit,openai2026codingsignal` after sentence one. The current example already justifies preserving this qualification.

5. **Telemetry/calibration:** “Coverage and mutation evidence is setting-dependent and cannot substitute for direct contract validation.” Cite `zhao2026coverage`. “Exception-oracle studies likewise show that predictive accuracy can coexist with sensitivity to structural cues.” Cite `hossain2026exceptionpatterns`; add only if the paragraph explains the much smaller specialized-model setting.

No external percentage above should be placed beside the manuscript's conditional FA rates as if the numerators, denominators, or truth standards matched.

## Search coverage and lower-priority/excluded leads

Searched primary arXiv papers, final ACL papers, author-hosted accepted manuscripts, OpenReview PDFs, and first-party benchmark audit reports. Queries combined self-generated tests, self-debugging false positives/negatives, tests reproducing implementation bugs, plausible SWE-bench patches, specification/test mismatch, oracle incompleteness, coverage/mutation effectiveness, and exception-oracle documentation. Followed citations from the two Zhao papers and recent repository-agent testing work. Checked posting/version dates against September 13, 2026. Existing references—including EvalPlus, Mathews/Nagappan, CodeJudgeBench, Ahmed, SWEABS, TENET, TDFlow, and ConVerTest—were treated as already covered. Search is targeted and cannot support an exhaustive “first” claim.

- **Earlier relevant predecessor, lower priority rather than rejected:** Dong Huang, Jie M. Zhang, Mark Harman, Mingzhe Du, Heming Cui, *Measuring the Influence of Incorrect Code on Test Generation*, arXiv:2409.09464v3 (March 28, 2025; first version September 14, 2024). Earlier title: *Rethinking the Influence of Source Code on Test Case Generation*. Zhao's misguidance paper explicitly critiques the predecessor's metric for treating any test passing buggy code as misguided. The newer paired-outcome definition is safer to use; the predecessor still matters to historical novelty. [Full v3](https://arxiv.org/html/2409.09464v3), [history](https://arxiv.org/abs/2409.09464).
- **Observational context only:** Andre Hora and Romain Robbes, *Are Coding Agents Generating Over-Mocked Tests? An Empirical Study*, arXiv:2602.00409v1, January 30, 2026, accepted MSR 2026. Reports mocking frequency, not a measured semantic failure rate; avoid equating mocks with bad tests. [Author manuscript](https://andrehora.github.io/pub/2026-msr-agents-over-mocked-tests.pdf), [metadata](https://arxiv.org/abs/2602.00409v1).
- **Watchlist, metadata unresolved:** *Do More Agent-Generated Tests Help LLM Code Agents? Evidence from Repository Issue Resolution*, anonymous OpenReview manuscript. Full PDF inspected, but stable author/date/status could not be established. Interesting repository-agent intervention evidence; do not cite as an established named result until resolved. [PDF](https://openreview.net/pdf?id=VnEZnbX84i).
- **Counterevidence lead handed to the broader review:** *LLM-Powered Test Case Generation for Detecting Bugs in Plausible Programs* (TrickCatcher), ACL 2025. Its independently assessed test-generation improvements should not be described as closed-loop self-verification. [Final primary paper](https://aclanthology.org/2025.acl-long.20/).
- **Not selected:** small nine-task cross-context studies, anonymous proof-versus-test benchmark proposals, and secondary commentary lacked either comparable outcomes or sufficiently stable primary metadata. Failure to construct a proof is not proof that a test-passing program is wrong. A journal issue dated November 2026 was excluded because a pre-cutoff first-publication date was not established.

## Concrete research implication

The literature supports a follow-up that independently adjudicates each RGRBench disagreement against the visible contract, separates adapter failures from underspecified requirements and genuine violations, and freezes the repaired contract/oracle before a held-out rerun. A separate matched-candidate intervention could then compare code-conditioned tests, spec-only tests, and independently authored tests. Those are proposed experiments; the present artifact cannot claim their conclusions.
