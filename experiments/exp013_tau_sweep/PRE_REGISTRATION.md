# exp013 — RGRBench RED-threshold (τ) sweep and matched-acceptance point

**Status: pre-registered. Frozen before any data is collected.** Raw `result.json` and
`usage.jsonl` are committed; every number in the paper that cites this experiment traces to a
committed file. Honest nulls: all swept τ are reported, including non-monotonic or null results.

## 1. Question

The RGRBench flagship (exp010) ran the strong-judge cell at a single fixed threshold τ=0.70 and
found (a) the false-accept rate unchanged versus control (41.5%→42.0%) but (b) total correct
output down (52→29 oracle passes), because the frontier judge abandons 189/251 packages at the
RED gate. Two reviewer objections have no answer in the committed data:

- **Calibration confound (#1):** is the RED-gate abandonment a property of a frontier judge, or an
  artifact of the fixed τ=0.70 shared with the weak judge?
- **Selection confound (#2):** the cross-cell FA rate is conditioned on differently-selected
  claim sets (258 vs 62 packages produce code). What is the FA rate at *equalized* acceptance?

## 2. Design (frozen)

Identical to exp010's strong-judge cell in every respect except the RED/GREEN judge threshold τ:

- **Generator / test author:** `gpt-4o-mini`, temperature 0.7 (unchanged).
- **All judge roles + adapter author:** `gpt-5.6-terra`, temperature 1.0 (unchanged).
- **Packages:** the same 89 RGRBench packages; same terra-authored adapter grading (v3.1 harness).
- **Swept thresholds:** τ ∈ {0.40, 0.55, 0.85} run here; **τ=0.70 is reused from exp010** as the
  anchor (not re-run).
- **Runs per package:** **N=1** at each new τ (89 runs/τ). This powers aggregate accept/FA rates
  per τ, not per-package run variance; a confirmatory N=3 at the single matched-acceptance τ is a
  pre-approved cheap follow-up if that point lands informatively.
- **Budget cap:** $120 hard stop (`spent_usd` gate). Raised from $60 to $120 before the run,
  authorized after a smoke run measured the per-run cost at $0.358 (3m42s, 26 calls) — the full
  89-package × 3-τ × N=1 design projects to ~$96. If the cap is hit, report exactly where it
  stopped (honest partial).
- **Exclusions:** the exp010 rule unchanged — runs whose oracle collects no tests (adapter import
  failure / harness error) are invalid and dropped; report the count per τ.

## 3. Hypotheses and decision rules (frozen)

- **H1 — soundness is threshold-robust.** The conditional false-accept rate (FA / claimed
  successes) stays within ±12 percentage points of exp010's 42% at every swept τ.
  *Confirm* → soundness invariance is not a τ=0.70 coincidence. *Refute* (any τ outside the band)
  → report it; the invariance claim becomes threshold-specific.
- **H2 — gatekeeping tracks τ.** RED-gate abandonment (packages that never reach GREEN) decreases
  monotonically as τ decreases. If at the lowest τ (0.40) abandonment falls near control's (~1%),
  the gatekeeping is threshold-driven, not an intrinsic frontier-judge behavior — and the
  "gates rather than coaches" framing must be scoped to τ.
- **H3 — matched acceptance (#2).** Among {0.40, 0.55, 0.70, 0.85}, take the τ whose accepted-claim
  count is closest to control's 65. Report its conditional FA rate with a Wilson CI. *Decision:*
  if that rate is within the H1 band of control's 41.5%, soundness invariance holds even at
  equalized selection; the selection confound does not explain the gap.

## 4. Primary outcomes per τ (pre-specified)

Per τ, computed from committed `result.json` (self_verdict × oracle.pass_fraction) and the
red/green attempt fields: claimed successes (TA+FA); FA count, conditional FA rate, Wilson CI;
RED-gate abandonment (green_attempts==0); packages reaching GREEN; TA; oracle passes (TA+FR).

## 5. Constraints

- **Direct API calls, no VCR** in this harness — every run is fresh spend; hence the N=1 /
  budget-cap design. ChatLiteLLM throughout (as exp010).
- Pre-registration frozen and committed **before** the first run. Raw per-run artifacts
  (`result.json`, `self_tests.py`, `candidate/`, `usage*.jsonl`) committed after collection.
- Provenance: `run_tau_sweep.py` is exp010's `run_flagship.py` with τ parameterized
  (`EXP013_TAU`) and outputs nested per τ; no other pipeline change.
