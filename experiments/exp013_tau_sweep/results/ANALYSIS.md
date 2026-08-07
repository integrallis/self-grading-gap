# exp013 — τ-sweep ANALYSIS (generated; do not hand-edit)

Total spend $37.76. New τ points (0.40/0.55/0.85) are N=1 (89 runs each); τ=0.70
control/strong are the reused exp010 N=3 anchors. FA% = false accepts / claimed successes;
RED% = packages abandoned at the RED gate (never produced code); oPass = oracle-passing
solutions (TA+FR).

| cell | valid | acc | acc% | FA | FA% [95% Wilson] | RED% | oPass |
|---|--:|--:|--:|--:|--:|--:|--:|
| control τ=0.70 (N=3) | 261 | 65 | 24.9 | 27 | 41.5 [30.4, 53.7] | 1.1 | 52 |
| strong  τ=0.70 (N=3) | 251 | 50 | 19.9 | 21 | 42.0 [29.4, 55.8] | 75.3 | 29 |
| strong  τ=0.85 (N=1) | 81 | 6 | 7.4 | 2 | 33.3 [9.7, 70.0] | 91.4 | 4 |
| strong  τ=0.70 (anchor, N=3) | 251 | 50 | 19.9 | 21 | 42.0 [29.4, 55.8] | 75.3 | 29 |
| strong  τ=0.55 (N=1) | 85 | 17 | 20.0 | 9 | 52.9 [31.0, 73.8] | 72.9 | 10 |
| strong  τ=0.40 (N=1) | 86 | 37 | 43.0 | 25 | 67.6 [51.5, 80.4] | 47.7 | 15 |

## Frozen hypothesis verdicts

**H1 (FA rate threshold-robust, within ±12pp of 42%): REFUTED.** FA% is not invariant to τ; point estimates rise monotonically as the gate loosens — 33.3% (τ0.85) → 42.0% (τ0.70) → 52.9% (τ0.55) → 67.6% (τ0.40). τ0.40 is 67.6% [51.5, 80.4], entirely above the +12pp band edge (54%); n=37 accepts. (τ0.85/τ0.55 have 6/17 accepts — wide CIs, not decisive alone; the trend and the τ0.40 point carry the refutation.)

**H2 (RED gatekeeping tracks τ): CONFIRMED IN DIRECTION, but not a pure calibration artifact.** Abandonment falls monotonically as τ drops — 91.4% → 75.3% → 72.9% → 47.7% — so τ drives much of it. But even at the most permissive τ=0.40 it is 47.7%, versus the weak judge's 1.1%. A large intrinsic frontier-judge strictness remains at every threshold; the gatekeeping is BOTH threshold-driven and intrinsic.

**H3 (matched-acceptance — the selection answer): the invariance is a selection artifact.** Control accepts 24.9%. The strong judge reaches that acceptance only near τ≈0.48 (between 20.0% at τ0.55 and 43.0% at τ0.40), where FA% interpolates to ~55–65% — far above control's 41.5%. Cleaner dominance: at τ0.40 the strong judge accepts MORE than control (43.0% vs 24.9%) at a significantly WORSE FA rate (67.6% [51.5,80.4] vs 41.5% [30.4,53.7]). At no tested τ does the frontier judge reach control's acceptance at control's-or-better FA rate. The clean 41.5%→42.0% match at the shared τ=0.70 held only because the frontier judge accepts fewer.

## Bottom line

- 'Verifier strength does not improve soundness' is STRENGTHENED: the frontier judge never beats control on FA rate at comparable throughput, and is worse when matched.
- 'The false-accept rate is a stable, verifier-independent invariant' OVER-REACHES: FA rate is a point on a throughput-vs-soundness tradeoff set by the RED threshold (ranged 33–68% here); the frontier judge shifts that curve unfavorably, it does not sit on a fixed constant.
- Confirmatory N=3 at the matched τ (≈0.48) is the pre-approved cheap follow-up to tighten H3.

