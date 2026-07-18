# exp011 — verifier generalization: do the findings hold for proven-strong, cross-provider verifiers? (pre-registered)

**Status: registered. Frozen before any data collection. Verifier identifiers and API keys resolved (see end of document).**

**Motivation.** The paper's soundness-invariance result — a frontier model in the verification
roles leaves the false-accept rate unchanged — rests on a single frontier verifier, GPT-5.6 Terra
(`gpt-5.6-terra`). Terra is a real, public model (released 2026-07-09), but as of this
registration it has **no published judging or specification-verification pedigree**: no code-judge
or NL-conformance benchmark reports a number for it. That is a defensible stance for the paper — a
just-released frontier model of unknown verification strength, whose findings we ask whether they
generalize — but it invites the question of whether the null is an artifact of *that particular*
model rather than of the self-testing loop. This experiment answers that by rerunning the
exp006/exp007 asymmetry design with two verifiers chosen for the **opposite** property: each is the
best-evidenced model on a capability the verification gap should depend on.

- **Gemini-2.5-Pro** — the strongest execution-grounded **code judge** in the literature
  (CodeJudgeBench, 82.1 avg; arXiv:2507.10535).
- **Claude-4.5-Sonnet** — the strongest model at **NL-requirement / specification conformance**
  (CodeSpecBench repository-level, arXiv:2604.12268; requirement-conformance recognition,
  arXiv:2508.12358), the capability the paper argues the gap actually stresses ("the gap is a
  validation failure, born at comprehension").

Both are **non-OpenAI**, so a shared null also rules out an OpenAI-family artifact. Directional
predictions follow the challenger's view (a proven-best judge / NL-understander *should* reduce
false accepts if the thesis is wrong); the outcome is open and either result reshapes the
discussion. Terra stays in the paper as a third verifier — the "unknown-pedigree, just-released
frontier model" arm — so the three verifiers span **unknown / proven-judge / proven-NL-understanding**.

## Design (frozen)

The exp006 (HumanEval subset-30) and exp007 (LiveCodeBench lcb30) designs, unchanged except for the
identity of the strong model S. Both frozen problem sets are reused verbatim (HumanEval IDs from
`exp006_model_asymmetry/results/plan.json`; lcb30 from `exp007_lcb_asymmetry/problems/lcb30.json`;
rates on these subsets are not benchmark rates). Anchoring **both** (default templates),
**escalation OFF** in all cells (escalation model pinned to the generator), judge threshold 0.70,
max retries 3, **N=5** runs per cell. All LLM calls via `ChatLiteLLM` (VCR-recorded).

Weak model **W = `gpt-4o-mini`** (generation T=0.7 / judging T=1.0), unchanged — its Oct-2023
training cutoff preserves the LiveCodeBench contamination control (lcb30 postdates 2025-01-01).
Strong model **S ∈ {`gemini/gemini-2.5-pro`, `claude-sonnet-4-5`}**, run as two separate experiments
(resolved provider snapshot recorded in each `plan.json`). Unlike terra (which accepts only its
default temperature), both permit temperature selection; to keep the manipulation single-variable we
pin S judge and S test-author to **T=1.0**, matching terra's effective setting. A
post-2025 verifier cutoff is admissible: per §Threats, judge-side exposure to the LCB problems could
only *reduce* false accepts, so a memorizing verifier biases toward the challenger, not the thesis.

Per verifier S, per benchmark:

| cell | test author | code generator | judge (all three judge roles) |
|---|---|---|---|
| control        | W     | W | W     |
| strong_testgen | **S** | W | W     |
| strong_judge   | W     | W | **S** |
| strong_both    | **S** | W | **S** |

A fresh `control` is run in each experiment for within-experiment pairing and a control-stability
cross-check against exp006/exp007.

## Measures and decision rules (frozen)

Identical to exp006/exp007. Oracle scoring is a protocol stage (EvalPlus base+plus on HumanEval; the
private LiveCodeBench suites through the non-cheating adapter on lcb30). Per cell and run: oracle
pass /30, false accepts vs base and vs plus (self_verdict ∧ oracle fail), false rejects (cycle
failed ∧ oracle pass), total verdict error (FA-plus + FR), cost.

Contrasts vs `control`, exact McNemar on per-problem majority-of-5 status, gated on pre-registered
practical floors: **pass-rate floor 4, FA floor 2, FR floor 2, verdict-error floor 3**. If the
control's observed max pairwise spread exceeds a floor, the larger value is used (and recorded in the
analysis). SIGNAL requires **p<.05 AND the floor**.

- **H1 (soundness; challenger's primary):** strong_judge reduces FA-plus vs control.
- **H2:** strong_testgen reduces FA-plus vs control.
- **H3 (thesis-critical):** strong cells reduce TOTAL verdict error — a reduction, not a relocation
  between FA and FR.
- **Registered expectation (completeness):** strong_judge reduces FR (per exp006/exp007); reported
  as a result whether or not it replicates.
- Descriptives: per-cell test-suite size and canonical-test counts; judge score distributions; cost
  per cell.

**Primary registered outcome.** If H1–H3 are NULL under both proven-strong verifiers (as they were
under terra), soundness-invariance generalizes across three verifiers spanning unknown, proven-judge,
and proven-NL-understanding capability. A SIGNAL under either verifier is a finding against the
thesis and is reported as such. Null results are reported as results.

## Contingencies

Provider-rejected parameters are recorded and retried with the provider's required values; terminal
API errors count as failed problem-runs. Exact API model identifiers and provider are recorded in
each `plan.json`. **Budget cap $150 total (runner-enforced); expected ~$90–100** across both
verifiers × both benchmarks. Token volume for a new judge may differ from terra's, so the cap carries
headroom. Scope is the asymmetry experiments only (exp006/exp007 analogues); the RGRBench (exp010)
replication is a separate, later registration decided after these results.

## Run (mirrors exp006/exp007 stages, S set per experiment)

```bash
# per (verifier, benchmark): plan -> smoke -> run -> score -> analyze, resumable
# HumanEval analogue reuses run_asym.py machinery; LCB analogue reuses run_lcb.py.
# Outputs under results/: per-run summaries + tagged usage logs, scores/, *_summary.json,
# ANALYSIS.md (generated — never hand-edited).
```

## Resolved at registration

- **Strong verifiers (frozen LiteLLM ids):** `gemini/gemini-2.5-pro` (Google AI Studio; knowledge
  cutoff January 2025) and `claude-sonnet-4-5` (Anthropic; resolved snapshot recorded in `plan.json`
  at run time). Both accept `temperature`, so both are pinned to **T=1.0**.
- **Verifier chosen for pedigree, not recency.** Claude-4.5-Sonnet, not the newer Claude Sonnet 5:
  Sonnet 5 has no published judge or specification-conformance benchmark (only agentic-coding
  scores), so it would duplicate terra's unknown-pedigree role rather than serve as the proven
  NL-understanding arm; Sonnet 5 also rejects non-default temperature, breaking the single-variable
  protocol.
- **Keys verified present** in `.env` (gitignored, untracked): `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`,
  and `OPENAI_API_KEY` (weak generator). All calls via `ChatLiteLLM` so VCR records them.
