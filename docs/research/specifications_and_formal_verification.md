# Specifications, formal verification, and terminology

Scope: primary sources available through 2026-09-13. These are complementary studies;
none reruns the present pipeline or estimates its semantic error rate.

## VERINA

Zhe Ye, Zhengxu Yan, Jingxuan He, Timothe Kasriel, Kaiyu Yang, and Dawn Song.
*VERINA: Benchmarking Verifiable Code Generation*. ICLR 2026;
[official proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/41b8c80f9113b9f8e2e129447221682a-Abstract-Conference.html),
[full text, v3 dated 2026-03-16](https://arxiv.org/html/2505.23135v3).

Sections 3–4 separate code, specification, and proof generation on curated Lean tasks.
Generated specifications are checked against reference specifications, with unknown
outcomes explicitly bounded. A proof of a generated specification therefore does not
by itself establish fidelity to the original requirement. Appendix C.5 also warns
against equating proof failure with incorrectness: failed proof search can leave a
correct specification unverified. Cite as a constructive formal-verification direction,
with specification fidelity and proof-search completeness treated separately. Do not
use the difference between test-pass and proof-pass as an observed bug rate.

## Requirement-derived test oracles

Tiancheng Ma and Nasir U. Eisty. *From Business Requirements to Test Assertions:
Evaluating LLM-Generated Oracles on Real Bugs*. Preprint, 2026-07-11,
[arXiv:2607.10277v1](https://arxiv.org/html/2607.10277v1).

Sections 4–6 compare generated oracles with both a requirement-derived reference and
the system under test. This supports separating requirement agreement from agreement
with an implementation. The pilot covers ten bugs from one Java component and five
models. Requirements and reference oracles were manually derived from fixes; failed
compilations are excluded from performance aggregates. Weak correlations with
LLM-rated ambiguity do not establish that ambiguity is irrelevant. This is useful
support for adjudicating the RGRBench contract mismatch, not a replication of its
conditional false-accept rate.

## General-agent terminology

Xiaochuan Li, Ryan Ming, Pranav Setlur, Abhijay Paladugu, Andy Tang, Hao Kang,
Shuai Shao, Rong Jin, and Chenyan Xiong. *Benchmark Test-Time Scaling of General
LLM Agents*. Preprint, 2026-02-22,
[arXiv:2602.18998v1](https://arxiv.org/html/2602.18998v1).

Sections 4.1–4.3 use “verification gap” for the shortfall between oracle pass@K and
the agent's ability to select a correct trajectory. Point-wise and pair-wise selection
also have different scoring definitions. This is related terminology, not the present
paper's fraction of accepted outputs rejected by an oracle. Its externally assigned
GPT-5 verifier does not generally outperform self-judgment under that protocol;
this does not imply that independent verification is generally worse. Explicitly
distinguish the metrics and avoid claiming coinage of the term.

## IdeaAMBIG

Yiling Ma, Yilun Zhao, Sihong Wu, Manasi Patwardhan, and Arman Cohan.
*IdeaAMBIG: Benchmarking Implementation-Critical Gaps in Research-Idea
Specifications*. Preprint, 2026-09-09,
[arXiv:2609.10539v1](https://arxiv.org/html/2609.10539v1).

The study concerns research-method specifications, not ordinary application
requirements. Section 4.4 supplies gold clarification on 50 paired instances and
finds improved specification readiness; Appendix D.4 adds executable checks on
20 bounded components. These are oracle-assisted interventions, not autonomous
recovery of missing requirements. The result motivates a clarification experiment,
but neither the specification-readiness rate nor the small component experiment
should be described as an application-scale coding-agent success rate. Keep in the
research review rather than expanding the manuscript with a distant benchmark.

## Additional scope decisions

- The anonymous OpenReview position paper *AI Coding Benchmarks Need Proofs, Not
  Just Tests* was a discovery lead. Stable author/publication metadata were not
  established. VERINA supplies a stronger attributable source for the relevant
  formal-specification distinction; the anonymous paper is not added to the manuscript.
- *Test Oracle Automation in the Era of LLMs* is a useful further roadmap. Its
  two-author 2024 arXiv record differs from the later three-author journal record;
  these should not be conflated. It is not needed for the current argument, already
  grounded in Barr et al. and directly measured newer studies.
- The original `chen2021humaneval` bibliography entry was present but uncited. Cite
  it when introducing HumanEval, alongside the distinct EvalPlus citation.
