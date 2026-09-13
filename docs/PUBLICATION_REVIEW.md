# Publication and literature review — 2026-09-13

The subsequent [deep literature review](LITERATURE_REVIEW.md) extends this initial audit
through September 13, 2026, with updated publication metadata, earlier self-test error
studies, and newer supporting and contrary evidence. Use that review and its
[entry-by-entry audit](research/bibliography_audit.md) for the current bibliography.

This review covers the manuscript, bibliography, literature-positioning notes, and release
metadata present at the start of the audit. It records findings for the accompanying manuscript
revision; it is not a fresh experimental analysis. Statistical and oracle corrections require
the separate raw-artifact review. No submission, public release, support message, or account
change was made. The roughly three-month arXiv hold is author-reported. The author supplied
submission-page details during review: `submit/7939730`, status **on hold**, **Primary: None**,
optional cross-lists **cs.LG** and **cs.SE**, license **CC BY 4.0**, and comments reporting
**21 pages, 6 figures, 7 tables**. These are the supplied page details; the private account and
earlier correspondence were not independently accessed.

The paper has a useful contribution as an empirical study of how model-role interventions
change an executed pipeline's success claims, oracle outcomes, and abstentions. Its strongest
release pitch is reproducible verdict accounting and bounded evidence about these interventions.
It should not be pitched as a proof that stronger verification cannot help, the discovery of
the test-oracle problem, or a universal error rate across coding agents.

## Findings to resolve before promoting the preprint

| Priority | Finding | Required treatment |
|---|---|---|
| High | Absence of a detected false-accept reduction is repeatedly presented as soundness invariance or inability to help. | Distinguish a failed superiority decision rule from demonstrated equivalence. State the tested generator, verifier roles, tasks, and thresholds. A sizable directional reduction remains compatible with a nonsignificant comparison. |
| High | The full `numbers_to_words` example fails because the oracle requires `ValueError` while the displayed requirements allow an unspecified error type. | Describe this as specification–oracle disagreement. It is not evidence that the generated implementation contradicts the requirements. Audit similar mismatches before interpreting the application-scale gap as semantic incorrectness. |
| High | `PROVENANCE.md` says release history was linearized and run SHAs refer to private history, while broad manuscript/README wording suggests the public history independently proves pre-registration. | Disclose the distinction. Release contemporaneous protocol evidence and a source-tree mapping for historical run SHAs where possible. Reconstructed commit dates alone cannot establish prospective registration. |
| High | The literature-positioning memo treats percentages from different designs as a field constant and suggests other studies have been nullified. | Retire those claims. Denominators, tests, populations, and interventions differ; a new empirical result cannot invalidate a different experiment without reproducing the relevant contrast. |
| Medium | Related work understates judge capability and conflates generated-test ranking with a correctness guarantee. | Describe what those methods actually evaluate; current experiments do not reproduce CodeT or ConVerTest. |
| Medium | The contribution is insufficiently connected to the established oracle problem and imperfect-verifier inference scaling. | Add the two primary-source anchors below, then explain the incremental contribution of role interventions and executed verdict accounting. |
| Medium | Related work says a frontier model supplies “either the tests or the code,” although the implementation generator is held fixed. | Say test author or reviewer. |
| Medium | The release README and reproducibility commands describe only the two older experiments. | Bring the public entry point into agreement with the revised paper and include the application-scale analyses and their external dependencies. |

The first two findings follow directly from the manuscript's definitions and displayed example,
not from a literature citation. They should determine the wording of the abstract, discussion,
figures, and community announcement, rather than being confined to a limitations paragraph.

## Verified literature and appropriate positioning

All newer arXiv identifiers in `paper/refs.bib` were found and correspond to the intended works.
The problems are attribution details and overextension of the cited findings, rather than
nonexistent papers.

| Source checked | What it supports and what needs correcting |
|---|---|
| [Ahmed et al., *Investigating Test Overfitting on SWE-bench*, v3](https://arxiv.org/html/2511.16858v3) | Closest empirical predecessor: generated-test acceptance versus held-out golden tests, with a code/test refinement loop. Table 1 reports 21.8% and 33.0% before refinement, 25.5% and 35.9% after. Its denominator is generated-test-passing patches. These are related observations, not a common population estimate. The current version identifies an FSE Companion 2026 publication and DOI `10.1145/3803437.3805574`; citing the 2025 preprint remains valid if the version is clear. |
| [Yu et al., *SWE-ABS*, v1](https://arxiv.org/abs/2603.00520) | Strengthening benchmark tests rejects 19.71% of previously passing patches. Its denominator is benchmark-passing patches, not agent self-claims. Keep this as evidence of oracle sensitivity, and label it separately in any comparison plot. The exact title ends in singular **“Test-based Benchmark”**. |
| [Jiang et al., *CodeJudgeBench*, v2](https://arxiv.org/html/2507.10535v2) | Shows performance variation, response-order effects, and difficulty judging generated tests. Table 3's leading averages are 82.12% for Gemini-2.5-Pro and 79.93% for Claude-4-Sonnet, so “only slightly aligned” misrepresents the full result. The evaluated Sonnet is **4**, not **4.5**; the paper supports selecting a model family, not assigning its measured rank to a later release. |
| [Hu et al., *TENET*, current record](https://arxiv.org/abs/2509.24148) | Repository-level generation using developer-written tests; distinguish this input regime from fully autonomous test authorship. Correct author order: **Yiran Hu, Shanchao Liang, Nan Jiang, Yi Wu, Lin Tan**. The current record reports acceptance at ISSRE 2026. |
| [Han et al., *TDFlow*, v2](https://arxiv.org/html/2510.23761v2) | The human-test experiment explicitly exposes normally hidden tests; its 94.3% result is a test-resolution setting. Table 2 also reports 68.0% with generated tests. These are distinct input regimes, not a measured conditional false-accept gap. Avoid the memo's blanket “no held-out oracle” statement across the entire study. The [current abstract record](https://arxiv.org/abs/2510.23761) identifies EACL 2026 publication. |
| [Taherkhani et al., *ConVerTest*, v1](https://arxiv.org/html/2602.10522v1) | Combines self-consistency, code verification, and dual execution agreement. Its evaluation includes test validity, coverage, and mutation scores; it does not claim that agreement proves correctness. The current pipeline's failure cases motivate evaluating residual error in such systems but do not refute its reported improvements. |
| [Jin and Chen, code-verification failures, v1](https://arxiv.org/abs/2508.12358) | Title, authors, and identifier match. This is relevant evidence about checking code against natural-language specifications; keep its task and models distinct from executed pipeline calibration. |
| [Liu et al., EvalPlus](https://arxiv.org/abs/2305.01210) | The stronger-suite evaluation and changed rankings support oracle-sensitivity motivation. Authors and identifier match. Expanded tests detect more faults; that does not establish a calibrated probability that any held-out verdict is semantically correct. |
| [Jain et al., LiveCodeBench](https://arxiv.org/abs/2403.07974) | Authors, title, and identifier match. Rolling contest problems support selection of a window after a documented cutoff. They do not independently prove that a particular provider's served model has never encountered a problem. |
| [Mathews and Nagappan, test-driven generation](https://arxiv.org/abs/2402.13521) | Title and authors match. Tests supplied with a problem are an input intervention; keep that distinction from tests independently written inside the evaluated loop. |
| [Fakhoury et al., TiCoder, author institution's publication page](https://www.microsoft.com/en-us/research/publication/llm-based-test-driven-interactive-code-generation-user-study-and-empirical-evaluation/) | TSE 2024 title and author list match; the workflow includes human intent clarification through tests. Its large-scale experiment uses idealized proxy feedback, while its user study is a separate part of the evidence. The bibliography can add the journal metadata/DOI rather than rely on an ancillary journal-first note. |
| [Chen et al., CodeT](https://arxiv.org/abs/2207.10397) | Author list matches. It ranks candidate solutions by dual execution agreement and measures downstream generation performance; it does not equate every agreement with semantic correctness. |
| [Hong et al., MetaGPT](https://arxiv.org/abs/2308.00352) | Identifier and first author match. Its multi-agent development results justify a neighboring-work citation. One example does not establish that all multi-agent frameworks omit gate calibration. |

Two additions materially improve the framing:

- [Barr, Harman, McMinn, Shahbaz, and Yoo, *The Oracle Problem in Software Testing: A
  Survey*](https://coinse.github.io/publications/pdfs/Barr2015qd.pdf), IEEE TSE 41(5),
  507–525, 2015, DOI `10.1109/TSE.2014.2372785`. This places correctness checking,
  specification ambiguity, and external oracle information in their established software-testing
  context. Prefer it to relying primarily on practitioner anti-pattern names.
- [Stroebl, Kapoor, and Narayanan, *The Limits of Inference Scaling Through
  Resampling*](https://arxiv.org/abs/2411.17501), arXiv:2411.17501v3, 2026. The original
  2024 version was titled *Inference Scaling fLaws: The Limits of LLM Resampling with
  Imperfect Verifiers*. This directly precedes the imperfect-verifier argument. Explain that
  the present study intervenes on test authors and judges inside an executed self-testing
  pipeline; its observational retry groups do not establish a causal refinement penalty.

The July literature memo was replaced during review. Its earlier statements saying
“field constant,” “never soundness,” “candidate nullifications,” or “nobody mutation-scores”
are superseded. Any narrow novelty claim needs an explicit comparison of what was measured. ConVerTest and
SWE-ABS alone demonstrate why an unqualified dismissal of earlier mutation-based evaluation
would be misleading. A benchmark weakness warrants a sensitivity study, not an assumption that
another paper's positive or null effect must reverse.

## Connection to the existing arXiv paper

[Brian Sam-Bodden, *What Context Does a Coding Agent Actually Need to Act?*,
arXiv:2607.09691](https://arxiv.org/abs/2607.09691) is a complementary study of agent
measurement. It fixes localization and varies code representation, then evaluates editing
outcomes and repeat-run variability. The shared methodological concern is whether internal
representations and signals preserve information needed for externally checked behavior.
It does not study autonomous self-tests, estimate the verification gap, or independently
replicate the current verifier interventions.

Suggested related-work wording:

> Sam-Bodden's context ablation isolates code representation at fixed localization and measures
> its effect on independently evaluated edits. The present study isolates a different component:
> the authorship and review of tests used to certify an agent's output. Both designs separate an
> internal proxy from the behavior evaluated outside it, but they address different interventions
> and outcomes.

Use a normal citation rather than an endorsement argument. The prior article's arXiv posting
does not establish peer review or predict the moderation outcome of this submission. A release
page can link the two as a research sequence without importing either paper's effect sizes.

## arXiv hold: recommended next action

Do **not** delete and re-create the submission to try to accelerate it. arXiv's official
[submission-status guidance](https://info.arxiv.org/help/submit_status.html#on-hold) says
duplicates during a hold should be avoided, deletion/resubmission adds delay, and held
submissions do not expire. A long hold supplies no reliable diagnosis of the paper's scientific
quality; [arXiv states that moderation is not peer review](https://info.arxiv.org/help/moderation/index.html).

One factual status inquiry is reasonable after the reported delay. Use the
[moderation support route](https://info.arxiv.org/help/contact.html#moderation-queries), include
the existing submission ID and prior correspondence, and ask whether anything is required
and how to supply the corrected manuscript within the current submission. Use the same case
thread for follow-up. The available guidance does not establish that revision will accelerate
moderation, and the original hold reason is unknown.

The supplied **Primary: None** field deserves a factual question in that inquiry. It may reflect
the interface or a moderation state; it does not establish that a missing category caused the
hold. My scope recommendation is **cs.SE** as primary, with **cs.LG** as a relevant cross-list:
this is primarily an empirical software-testing and agent-evaluation paper. This is a fit
judgment based on the manuscript and [arXiv's category definitions](https://arxiv.org/category_taxonomy),
not a promise of faster processing. The submitter should ask whether the stored classification
needs correction rather than create another submission. The comments' page, figure, and table
counts must be regenerated for the revised PDF before uploading it. The supplied CC BY 4.0
choice can be carried consistently into the manuscript release metadata.

Draft, for the submitter to review and send:

```text
Subject: Status and revision guidance for submit/7939730 — Who Grades the Grader?

Hello arXiv moderation team,

I am the submitter of submit/7939730, “Who Grades the Grader? The Verification Gap in
Self-Testing Code Agents,” submitted on [actual submission date].
It has shown “on hold” since [date]. [Prior correspondence or case number, if any.]

Could you let me know whether any information or action is required from the authors?
The submission page currently shows “Primary: None,” with cs.LG and cs.SE listed as
optional cross-lists. Is this an expected display for its current status, or does its
classification need correction? The paper's main subject is empirical software testing
and evaluation of self-testing code agents; we would suggest cs.SE as primary.

We have prepared a substantive revision that clarifies the statistical claims, oracle
limitations, related work, and artifact provenance. Please advise how we should provide
that revision within the existing submission while the hold is active.

Thank you,
Brian Sam-Bodden
[email associated with the arXiv account]
```

The scope statement above is a description of the intended revision; retain only items actually
completed in the final packet. Supply real submission metadata rather than guessing a public
identifier for a work that has not been announced.

## Community release while moderation continues

Release the corrected document as an **author preprint**, with a visible version/date, the
artifact commit, and a concise limitations statement. There is no need to invent a
“pre-pre-publication” status. The public pitch should invite independent reruns and audits of
specific failure cases and estimation choices.

Recommended release sequence:

1. Finish the manuscript/data consistency corrections and rebuild the PDF from the reviewed
   source. Document unresolved oracle ambiguity and provenance limitations. If these remain
   substantial, label the release as a research draft and make the uncertainty part of its abstract.
2. Prepare a GitHub release tied to a specific commit, including the PDF, source, commands,
   analysis outputs, and dependency information. GitHub releases package a tagged project
   snapshot with downloadable assets; see the [official release documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
3. Archive the version on Zenodo for a durable citation. A manual manuscript deposit provides
   precise control over paper metadata; a separate software record can archive the repository.
   Zenodo supports saving a draft and reserving a DOI before publication; the DOI is registered
   only when the record is published. Do not use the other paper's DOI for this object. See
   [Zenodo's upload guide](https://help.zenodo.org/docs/deposit/create-new-upload/).
4. If using automatic GitHub archiving, connect the repository before the intended release;
   subsequent releases are ingested automatically once enabled. See
   [Zenodo's integration guide](https://help.zenodo.org/docs/github/enable-repository/).
5. Link the manuscript and software records, the active repository, and the companion context
   paper. Once an arXiv record exists, add it to the release metadata. Preserve this version's
   identity so later corrections can be tracked.

Concrete local metadata work: `CITATION.cff` currently describes software and has no release
version or repository URL; retain that software identity and add the paper as a preferred
citation once its public identifier exists. The repository has an MIT license; use the supplied
CC BY 4.0 choice for the manuscript and make third-party benchmark assets' applicable licensing
clear without silently relicensing them. The README must match the final number of benchmarks and
provide the complete regeneration path. These are preparation items, not claims that a release
or DOI already exists.

The preprint should be easy to critique: provide the per-condition denominators, separate
failure categories, immutable raw outcomes, reproducible post-hoc corrections, and a short
list of the specific replications sought. That will contribute more to community uptake than
a stronger universal slogan or a duplicate arXiv submission.
