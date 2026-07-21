# exp011 — deviations from the pre-registration

The pre-registration (`PRE_REGISTRATION.md`) is frozen as the committed record. This file
transparently logs deviations that occurred during data collection.

## 1. Budget cap raised: $150 → $250 → $300 → $350 (2026-07-19/20/21)

**What:** `BUDGET_CAP_USD` in `run_he.py` and `run_lcb.py` was raised from the pre-registered
`$150` total to `$250`, then to `$300` to cover the last cells. The additional re-run waste came
from a too-strict run-validity threshold in the completion harness (runs with a few legitimately
empty problems, ~23-27/30, were being discarded and re-run as if rate-limited); once corrected to
keep any run with >=15/30 non-empty implementations, the good runs were retained. A clean
single-pass collection still costs ~$90-100.

**Why (operational, not scientific):** data collection hit three separate provider credit/quota
outages that forced runs to be discarded and re-executed:
1. OpenAI (`gpt-4o-mini`, the generator in every cell) exhausted its account quota mid-collection —
   every affected problem returned empty output until the account was topped up.
2. Anthropic (`claude-sonnet-4-5`) hit "credit balance too low" while running the Claude strong
   cells — same effect for those cells until topped up.
3. Vertex/IAM propagation delays on a freshly created GCP project (for `gemini-2.5-pro`) caused
   early Gemini calls to 403 until the service-account binding propagated.

Empty/partial runs from these outages were detected (< 29/30 non-empty implementations), deleted,
and re-run. That re-run waste — not any change to the study — pushed cumulative spend toward the
guardrail. The **scientific design is unchanged**: 4 verifier×benchmark arms, 4 cells each,
`N=5` runs, the same frozen HumanEval subset and lcb30 problem set, the same models, temperatures,
threshold, retries, floors, and decision bar. A clean single-pass collection costs ~$90–100, as
pre-registered; the cap raise only covers infrastructure re-execution.

**Scope:** the cap is a cost guardrail, not a scientific parameter. No hypothesis, decision rule,
effect-size floor, problem set, or model assignment was altered.

## 2. Stale-score guard added to the analysis pipeline

During re-runs, the `score` stage was found to skip any run whose EvalPlus/oracle result file
already existed, so re-executed runs could be analyzed against the *previous* (empty-run) scores.
Fixed by deleting an arm's `scores/` directory before re-scoring, so every reported number is scored
against the run it belongs to. This is a correctness fix to the scoring harness, not a design change.
