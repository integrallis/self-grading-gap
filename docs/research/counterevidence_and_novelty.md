# Counterevidence and novelty audit

Research cutoff: 2026-09-13. These are **reported results from other papers**, not new measurements of this repository. Primary full texts were inspected for methods, result tables, and metric definitions; no experiments were reproduced. Candidate BibTeX is in `counterevidence_additions.bib`.

## What should change in the manuscript

The defensible contribution is an audit of a particular executed test-first pipeline, its role interventions, and its transition to application tasks. It is not the discovery that generated tests can accept incorrect code, the first measurement of false acceptance, or evidence that self-verification cannot improve. Several missing papers directly evaluate rejection of incorrect programs or precision among accepted fixes. Others improve generation or selection, which is useful counterevidence to broad pessimism but does not itself measure the paper's conditional gap.

Prioritize SWT-Bench, Sol-Ver, CodeHacker, RETRACE, ReVeal, and SWE-RM in Related Work. TCS gives a distinct, very recent trained adversarial-test alternative. State that trained verifiers, deliberately independent reconstructions, and adversarial execution were not tested here. They are different interventions from replacing a prompted reviewer with a larger general model.

## Twelve primary candidates

### 1. SWT-Bench — direct acceptance filtering; essential antecedent

**Metadata:** Niels Mündler, Mark Niklas Müller, Jingxuan He, Martin Vechev. *SWT-Bench: Testing and Validating Real-World Bug-Fixes with Code Agents.* NeurIPS 2024; inspected arXiv v3, 2025-02-07; first posted 2024-06-18. [Proceedings record](https://papers.nips.cc/paper_files/paper/2024/hash/94f093b41fc2666376fb1f667fe282f3-Abstract-Conference.html), [versioned full text](https://arxiv.org/pdf/2406.12952v3).

**Evidence:** §5.3, “Filtering Code Fixes with Generated Tests”: SWE-Agent generates both fixes and tests. Retaining fixes whose generated tests have fail-to-pass or pass-to-pass behavior raises precision to **47.8%**, more than twice the baseline, at **20% recall**. Precision's denominator is retained proposed fixes; recall concerns recoverable correct fixes. This is directly closer to our conditional false-accept rate than pass@k. The passage does not print a complete accepted/rejected confusion matrix, so do not reconstruct counts from rounded percentages.

**Implication:** Add to generated-tests and repository-scale related work. Generated tests already have demonstrated filtering value, with an explicit precision–recall tradeoff. This supports auditing their residual errors while ruling out novelty claims about first measuring self-generated tests against external correctness.

### 2. Sol-Ver — direct false-positive reduction from same-model self-play

**Metadata:** Zi Lin, Sheng Shen, Ilia Kulikov, Jingbo Shang, Jason Weston, Yixin Nie. *Learning to Solve and Verify: A Self-Play Framework for Code and Test Generation.* First posted 2025-02-20; inspected **v4, 2026-03-03**, arXiv:2502.14948. [Full text](https://arxiv.org/pdf/2502.14948v4). An earlier five-author version appeared at the NeurIPS 2025 Deep Learning for Code workshop, confirmed by [Yixin Nie's publication list](https://easonnie.github.io/); its longer title and author list should not be conflated with v4.

**Evidence:** §4.1 and Table 1 report TestFP falling **12.75→9.60% on MBPP** and **20.76→18.63% on LiveCodeBench** after iterative solver/test-generator SFT+DPO using Llama-3.1-8B. FP means generated tests accepting known flawed solutions; negatives come from 20 candidate solutions per problem, identified by gold tests; footnote 5 reports 400 negatives per benchmark. It is **not** the fraction of accepted implementations that are wrong. Training jointly adapts code and tests; it is not a fixed-generator reviewer substitution.

**Implication:** Essential counterevidence to blanket same-model/shared-error claims. Cite exact per-benchmark values if needed, avoiding the abstract's aggregate improvement headline and distinguishing test-output accuracy from acceptance calibration. No larger teacher is needed by this framework, but benchmark evaluation still uses external tests.

### 3. CodeHacker — adversarial tests reduce acceptance of known bad programs

**Metadata:** Jingwei Shi, Xinxiang Yin, Jing Huang, Shengyu Tao, Jinman Zhao. *CodeHacker: Automated Test Case Generation for Detecting Vulnerabilities in Competitive Programming Solutions.* ACL 2026, pp. 2352–2382, July 2–7. [Record](https://aclanthology.org/2026.acl-long.108/), [full text](https://aclanthology.org/2026.acl-long.108.pdf).

**Evidence:** Tables 1/5 and Appendix E: across **2,000 CodeContest+ problems**, TNR rises **85.72→96.31%** for traditional judging and **84.04→96.05%** for special judging after calibrated adversarial augmentation. The denominator is originally negative **submissions**, not all problems or accepted outputs; exact submission totals are not printed in these tables. Expected outputs come from reference solutions. Infrastructure is human-audited; fewer than 5% of problems require expert implementation/repair of validators or checkers. A 600-case generated-test audit is reported separately.

**Implication:** Direct evidence that targeted verification reduces missed defects. It does not establish a fully autonomous, reference-free solution to our problem. Avoid treating its unusual interpretation of falling TPR as standard false-rejection accounting: the authors also dispute some original positive labels.

### 4. SWE-RM — fixed-trajectory discrimination and calibration

**Metadata:** KaShun Shum, Binyuan Hui, Jiawei Chen, Lei Zhang, X. W., Jiaxi Yang, Yuzhen Huang, Junyang Lin, Junxian He. *SWE-RM: Execution-free Feedback For Software Engineering Agents.* Published in [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/e7feb9dbd9a94b6c552fc403fcebf2ef-Abstract-Conference.html). Numerical evidence below follows arXiv v1, 2025-12-26, 2512.21919. [Inspected full text](https://arxiv.org/pdf/2512.21919v1).

**Evidence:** §4.1 and Table 4 evaluate **500 SWE-bench Verified tasks × 32 trajectories** per generator. For Qwen3-Coder-Flash, SWE-RM obtains **AUC 0.783, ECE 0.051, RM@32 62.0%**; the DeepSWE execution-free comparator has **0.758, 0.124, 53.2%**. AUC and ECE evaluate all trajectories, whereas RM@32 evaluates one selected trajectory per task. The verifier is trained on execution-labeled trajectories and multiple policies/data sources.

**Implication:** Especially valuable methodological baseline: ranking quality, discrimination, and calibration are separate. This paper already makes that distinction. It supplies evidence for trained verification beyond stronger prompted judges, without demonstrating an acceptance threshold that bounds our conditional gap.

### 5. RETRACE — fresh reconstruction, useful but generation-level endpoint

**Metadata:** Chenglin Li, Yisen Xu, Zehao Wang, Shin Hwei Tan, Tse-Hsun (Peter) Chen. *Independent Patch Verification for Coding Agents with a Bidirectional Reconstruct-and-Verify Framework.* arXiv:2608.08950v1, 2026-08-09, eight-page preprint. [Full text](https://arxiv.org/pdf/2608.08950v1).

**Evidence:** Table 1, **500 SWE-bench Verified issues**, one greedy run/configuration: mini-SWE-agent rises **281→316 resolved** with GPT-5-mini and **379→397** with MiniMax M2.5. A backward stage infers the problem from the patch and trajectory while withholding the original issue, then reconciles with forward reasoning. All added components use the underlying agent's backbone. Ablations/scaffold transfer use a random **120-issue** subset. The endpoint is correctness of the final submitted patch after revisions, not a fixed-patch false-accept matrix.

**Implication:** Add as a concrete approach to interpretation independence. “Independent” here does not mean another provider, no shared context, or an external executable oracle. It overlaps strongly with our motivation, but does not measure reliability of its own alignment verdict separately from the revisions it induces.

### 6. ReVeal — trained self-verification can make retries helpful

**Metadata:** Yiyang Jin, Kunzhao Xu, Hang Li, Xueting Han, Yanmin Zhou, Cheng Li, Jing Bai. *ReVeal: Self-Evolving Code Agents via Reliable Self-Verification.* Published in [ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/f24e8cc1c1c06a689850ee766a7357b2-Abstract-Conference.html). arXiv:2506.11442 was first posted 2025-06-13; numerical evidence follows **v2, 2025-10-21**. [Full text](https://arxiv.org/pdf/2506.11442v2).

**Evidence:** §3/Table 1: on LiveCodeBench V6 (February–May 2025), ReVeal with 25 turns reaches **38.7%**, versus **32.8%** single-turn RL; CodeContests scores are **33.6% versus 21.0%**. Joint training uses reference code/tests and explicit verification rewards. Training permits three turns; inference extrapolates farther. Reported zero degradation of initially correct code is a **revision-transition metric**, not zero false accepts. CTRL comparator values come from a different LiveCodeBench window, explicitly disclosed by the paper.

**Implication:** Cite against any causal/general claim that retries worsen correctness or self-checking is intrinsically futile. Our observed retry association concerns selected trajectories in one untrained pipeline, a materially different intervention.

### 7. TCS — very recent adversarial test training

**Metadata:** Jiacheng Xu, Wentao Zhang, Zhiyi Lyu, Fuxiang Zhang, Chaojie Wang, Yang Liu, Bo An. *Two-Stage Reinforcement Learning for Sound and Adversarial Test Generation in Code LLMs.* arXiv:2609.03955v1, **2026-09-03**; arXiv comments report acceptance to Findings of EMNLP 2026. [Full text](https://arxiv.org/pdf/2609.03955v1).

**Evidence:** §4/Table 1: TACO validation has **1,000 problems**; selection uses **16 candidates on TACO, 32 on LiveCodeBench**, one generated test/candidate. Appendix A uses the August 2024–February 2025 LiveCodeBench window, without printing its task count. With a TCS-trained 7B model, LiveCodeBench pass@1 is **37.03%**; test-based selection yields **48.79% without public tests**, **54.75% with them**. Stage 1 rewards agreement with reference solutions; Stage 2 rewards valid counterexamples to current mistakes. The selection bound assumes valid inputs and a positive separation margin.

**Implication:** A relevant untested alternative to generic stronger reviewers. “Sound” is reference-relative and trained under reliable-reference assumptions; reported success concerns selected answers, not calibrated false acceptance among autonomous success declarations. Cite as recent accepted work with publication status qualified.

### 8. Agentic Verifier — learned counterexample search outperforms generic voting

**Metadata:** Zeyao Ma, Jing Zhang, Xiaokang Zhang, Jiaxi Yang, Zongmeng Zhang, Jiajun Zhang, Yuheng Jing, Lei Zhang, **Mingze Li**, Wenting Zhao, Junyang Lin, Binyuan Hui. *Scaling Agentic Verifier for Competitive Coding.* arXiv:2602.04254v1, 2026-02-04. [Full text](https://arxiv.org/pdf/2602.04254v1).

**Evidence:** §4/Table 1: benchmarks contain **307 USACO, 175 LiveCodeBench, 232 OJBench, 118 ICPC-Eval, 64 CodeForces** problems. With Qwen3-30B-A3B-Thinking-2507 generation, USACO Best@64 is **74.5%**, versus **70.2%** random input-generator voting, with a **512-input** budget. The verifier searches for inputs distinguishing pairs of candidate programs; final choice uses output agreement. Training uses reference solutions, validated labels, and RL. §5.4 gives cases where it finds benchmark-missed errors.

**Implication:** Supports targeted execution and learned verifier comparisons. Best@k here means accuracy of the **single selected solution** from k candidates, not oracle pass@k. Case studies do not estimate a population false-accept reduction. Author names above follow the actual versioned primary text, not search snippets.

### 9. μCODE — learned scores complement execution feedback

**Metadata:** Arnav Kumar Jain, Gonzalo Gonzalez-Pumariega, Wayne Chen, Alexander M. Rush, Wenting Zhao, Sanjiban Choudhury. *Multi-Turn Code Generation Through Single-Step Rewards.* ICML 2025, PMLR 267; arXiv:2502.20380. [Proceedings full text](https://raw.githubusercontent.com/mlresearch/v267/main/assets/jain25a/jain25a.pdf).

**Evidence:** §4/Table 3: evaluation uses **500 MBPP, 164 HumanEval**, and **165 CodeContests** test problems. Up to three turns and five candidates per turn are permitted. With μCODE's 1B generator, public-test-only selection obtains **39.7%** on HumanEval, while public tests plus a learned verifier obtain **41.5%**. The analogous 8B values are **61.4% and 63.8%**. This is a selection ablation on a trained policy; private tests assess the final output.

**Implication:** A peer-reviewed example of combining verifier learning and execution. It supports the paper's finding that feedback can improve outputs, while highlighting that off-the-shelf model substitution is only a small part of the verifier design space. No conditional false-accept bound is reported by these comparisons.

### 10. SFS — useful tests, diversity, and pre-existing confusion accounting

**Metadata:** Jonathan Light, Yue Wu, Yiyou Sun, Wenchao Yu, Yanchi Liu, Xujiang Zhao, Ziniu Hu, Haifeng Chen, Wei Cheng. *SFS: Smarter Code Space Search improves LLM Inference Scaling.* ICLR 2025. [Proceedings record](https://proceedings.iclr.cc/paper_files/paper/2025/hash/387982dbf23d9975c7fc45813dd3dabc-Abstract-Conference.html), [full text](https://proceedings.iclr.cc/paper_files/paper/2025/file/387982dbf23d9975c7fc45813dd3dabc-Paper-Conference.pdf).

**Evidence:** Appendix I/Table 18 compares six self-generated validation tests with added ground-truth tests, GPT-3.5-turbo-0613, ten iterations. Pass@1 rises **82.5→87.2→89.0%** as zero/three/all ground-truth tests become available. The reported “false positive rate” is **6.3%, 9.8%, 1.8%**; the four confusion entries sum to 100%, indicating population shares rather than the conventional negative-class-conditioned FPR. The three-test result illustrates that improved pass@1 need not improve that false-accept entry.

**Implication:** Pre-existing analysis of generated tests versus external tests and both off-diagonal errors limits conceptual novelty. Additional ground-truth tests change the information supplied, so this does not refute a reference-free experiment. Do not transplant these ambiguously labeled percentages into our metric table.

### 11. Verification Limits Code LLM Training — strong novelty overlap

**Metadata:** Srishti Gureja, Elena Tommasone, Jingyi He, Sara Hooker, Matthias Gallé, Marzieh Fadaee. *Verification Limits Code LLM Training.* Inspected arXiv:2509.20837v1, 2025-09-25. [Full text](https://arxiv.org/pdf/2509.20837v1). Cite this version unless conference metadata is independently resolved.

**Evidence:** §§4–6 vary test complexity, quantity, pass thresholds, and model-based filtering in **synthetic training-data creation**. Evaluation is weighted pass@1 across multilingual HumanEval/LBPP/McEval, Python BigCodeBench, LiveCodeBench-v5 (**873 tasks**), and MBPP. Richer suites and softer filtering can improve downstream code generation, while overly strict acceptance can discard useful diversity. Human inspection also distinguishes incorrect test logic from coverage omissions.

**Implication:** The “verification ceiling” is a close conceptual predecessor: self-generated tests constrain the accepted data and its subsequent quality. Our contribution concerns runtime pipeline claims and interventions, not the first recognition of synthetic-verifier bottlenecks. The paper's positive results concern training outcomes, not the residual conditional gap at deployment.

### 12. LLM-as-a-Verifier — current diverse-candidate selection

**Metadata:** Jacky Kwok, Shulu Li, Pranav Atreya, Yuejiang Liu, Yixing Jiang, Chelsea Finn, Marco Pavone, Ion Stoica, Azalia Mirhoseini. *LLM-as-a-Verifier: A General-Purpose Verification Framework.* arXiv:2607.05391, first 2026-07-06; inspected **v2, 2026-07-07**. [Full text](https://arxiv.org/pdf/2607.05391v2).

**Evidence:** §5.2/Table 3: on **500 SWE-bench Verified issues**, a pool contains one trajectory each from Claude Opus 4.5, Gemini 3 Flash, and MiniMax M2.5. Gemini 2.5 Flash verifies using continuous scores, eight repeated evaluations, and criteria decomposition. The pool's mean pass@1 is **76.1%**, selected accuracy **78.2%**, and oracle pass@3 **84.4%**. This is selection over diverse generation, not an autonomous accept/abstain guarantee. Headline “state of the art” claims depend on particular harnesses and dates.

**Implication:** Concrete evidence that a cheaper verifier can help select from stronger models and that inference procedure matters alongside model size. Include in the wider report; prioritize direct false-accept work in the manuscript if space is limited.

## Scope, limitations, and search trail

Searches covered combinations of `code verifier generated tests false positive 2025 2026`, `learned verifier calibration`, `self-play solver verifier`, `independent patch verification`, and `adversarial test generation`; followed primary references from Agentic Verifier, ReVeal, and SWE-RM. Primary hosts used: arXiv, ACL Anthology, ICLR/NeurIPS proceedings, PMLR's repository, and an author institution for venue confirmation. Secondary discovery pages and blogs supplied leads only. Their summaries are not evidence for the findings above.

Downloaded PDFs and extracted text are temporarily at `/private/tmp/self-grading-counterevidence/`; identifiers and versioned URLs above are the durable retrieval record. This is a targeted narrative search, not a systematic review with exhaustive database coverage. Full methods/results passages were inspected, but no source repository was executed and no author-provided metric was independently reproduced. Sampling uncertainty, missing submission counts, changing benchmark versions, and source-specific correctness labels prevent pooling the percentages.

The report deliberately includes counterexamples to broad claims even when the interventions differ from ours. It does not infer that any one method will reduce the gap in the current instrument. A follow-up should freeze candidate outputs and report the acceptance confusion matrix, coverage, calibration, and cost for a prompted stronger judge, a reconstruction verifier, and an execution-based adversarial verifier using the same external evaluation.

## Other leads and exclusions

- **Structural Verification for Reliable EDA Code Generation without Tool-in-the-Loop Debugging**, Jayasuriya et al., arXiv:2604.18834v1 (2026-04-20): [primary full text](https://arxiv.org/pdf/2604.18834v1) reports verifier false positives **20.0→6.7%** and precision **80.0→93.3%** after uncertainty filtering (Table 6). Domain-specific OpenROAD contracts, small bespoke evaluation, and unclear confusion denominators make it secondary to the twelve above. Its similarly named “false positive rate” warrants definition checking.
- **Formal-specification methods:** VERINA, recent program-and-proof planning, and requirements–oracle mismatches are handled by the parallel audit; do not treat formal proof of a generated specification as proof that its natural-language translation is faithful.
- **Already cited:** CodeT, ConVerTest, TENET, TDFlow, EvalPlus, and imperfect-verifier resampling were not counted as new contributions here. The existing bibliography needs its own version audit; no comprehensive update search for every cited paper was completed in this subtask.
- **Excluded:** Reddit/workflow anecdotes, provider marketing comparisons without a primary experiment, mathematical-only verifier studies, and “no external teacher” claims that silently conflate no teacher at inference with no reference supervision during training.
