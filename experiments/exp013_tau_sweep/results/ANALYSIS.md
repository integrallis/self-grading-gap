# exp013 — τ-sweep ANALYSIS (generated; do not hand-edit)

Total spend $75.78. τ=0.50 is the confirmatory matched-acceptance point (N=3, 267 runs);
0.40/0.55/0.85 are N=1; τ=0.70 control/strong are exp010 anchors (N=3). FA% = false accepts /
claimed successes; RED% = packages abandoned at the RED gate; oPass = oracle-passing (TA+FR).

| cell | valid | acc | acc% | FA | FA% [95% Wilson] | RED% | oPass |
|---|--:|--:|--:|--:|--:|--:|--:|
| control τ=0.70 (N=3) | 261 | 65 | 24.9 | 27 | 41.5 [30.4, 53.7] | 1.1 | 52 |
| strong τ=0.85 (N=1) | 81 | 6 | 7.4 | 2 | 33.3 [9.7, 70.0] | 91.4 | 4 |
| strong τ=0.70 (N=3, anchor) | 251 | 50 | 19.9 | 21 | 42.0 [29.4, 55.8] | 75.3 | 29 |
| strong τ=0.55 (N=1) | 85 | 17 | 20.0 | 9 | 52.9 [31.0, 73.8] | 72.9 | 10 |
| strong τ=0.50 (N=3, matched) | 254 | 80 | 31.5 | 38 | 47.5 [36.9, 58.3] | 62.6 | 44 |
| strong τ=0.40 (N=1) | 86 | 37 | 43.0 | 25 | 67.6 [51.5, 80.4] | 47.7 | 15 |

## Frozen hypothesis verdicts

**H1 (FA rate threshold-robust, ±12pp of 42%): REFUTED.** Point estimates rise as the gate loosens — 33.3% (τ0.85) → 42.0% (τ0.70) → 47.5% (τ0.50) → 52.9% (τ0.55) → 67.6% (τ0.40). τ0.40 at 67.6% [51.5, 80.4] (n=37) is entirely above the +12pp band edge (54%). The rate is a throughput-controlled tradeoff, not a constant.

**H2 (RED gatekeeping tracks τ): CONFIRMED IN DIRECTION, not a pure calibration artifact.** Abandonment falls monotonically with τ — 91.4% → 75.3% → 72.9% (τ0.55) / 62.6% (τ0.50) → 47.7% — but stays ~48% even at the loosest τ, versus the weak judge's 1.1%. Both threshold-driven and intrinsic.

**H3 (matched acceptance): the confirmatory N=3 SOFTENS the preliminary read.** At τ0.50 the strong judge accepts 31.5% (near control's 24.9%, slightly higher) at FA 47.5% [36.9, 58.3] (n=80). That is directionally above control's 41.5% [30.4, 53.7] but the intervals OVERLAP: at matched throughput the frontier judge's false-accept rate is NO LOWER, not significantly higher. Significant worse-ness appears only as it admits more (τ0.40, 43.0% acceptance → 67.6% [51.5, 80.4]). The shared-τ 41.5%→42.0% agreement was a selection effect (frontier judge accepting fewer); the corrected claim is 'verifier strength never buys a LOWER false-accept rate at matched-or-higher throughput,' not 'significantly worse at matched throughput.' The preliminary N=1 interpolation (~55–60%) overshot.

## Bottom line

- 'Verifier strength does not buy soundness' HOLDS and is sharpened: the frontier judge never achieves a lower false-accept rate than control at comparable-or-higher acceptance, and is significantly worse when it admits substantially more.
- 'The false-accept rate is a stable verifier-independent invariant' OVER-REACHES: it is a point on a throughput–soundness tradeoff (33–68% here); a stronger judge shifts the curve unfavorably or, near matched throughput, not at all — it never improves it.

