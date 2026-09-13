# exp013 — τ-sweep ANALYSIS (generated; do not hand-edit)

Total spend $75.78. Regenerate with run_tau_sweep.py --stage analyze.
τ=0.70 anchors reuse exp010. τ=0.50 is an adaptive follow-up outside the originally
enumerated threshold set; it approximates throughput rather than matching it exactly.
The parameter changes both RED and GREEN judge thresholds. Wilson intervals below
are nominal run-level intervals and do not account for repeated packages.

| cell | valid | acc | acc% | FA | FA% [95% Wilson] | RED% | oPass |
|---|--:|--:|--:|--:|--:|--:|--:|
| control τ=0.70 (N=3) | 261 | 65 | 24.9 | 27 | 41.5 [30.4, 53.7] | 1.1 | 52 |
| strong τ=0.85 (N=1) | 81 | 6 | 7.4 | 2 | 33.3 [9.7, 70.0] | 91.4 | 4 |
| strong τ=0.70 (N=3, anchor) | 251 | 50 | 19.9 | 21 | 42.0 [29.4, 55.8] | 75.3 | 29 |
| strong τ=0.55 (N=1) | 85 | 17 | 20.0 | 9 | 52.9 [31.0, 73.8] | 72.9 | 10 |
| strong τ=0.50 (N=3, adaptive follow-up) | 254 | 80 | 31.5 | 38 | 47.5 [36.9, 58.3] | 62.6 | 44 |
| strong τ=0.40 (N=1) | 86 | 37 | 43.0 | 25 | 67.6 [51.5, 80.4] | 47.7 | 15 |

## Interpretation and deviations

- H1: the loosest threshold's point estimate is outside the registered ±12pp band
  around 42% (67.6% versus upper edge 54.0%).
  Its Wilson interval [51.5, 80.4]% overlaps that edge;
  the previous claim that the entire interval lies above it was incorrect.
- H2: RED abandonment decreases as the threshold decreases in these runs, but the
  shared threshold also changes GREEN gating, so this is not a RED-only intervention.
- H3: compare acceptance percentages, not raw claim counts from different run counts.
  The τ=0.50 follow-up was not in the originally enumerated grid and shares selection
  data with its N=3 aggregate. It is adaptive rather than an independent confirmatory
  comparison. Similar throughput also does not equalize which packages are accepted.
- Overlapping separate intervals establish neither equality nor the absence of an
  improvement. These point estimates show no improvement at the tested settings with
  comparable-or-higher throughput; a paired, package-cluster analysis is needed for
  uncertainty on contrasts. No pure verifier-strength or whole-curve claim follows.
- The conditional FA point estimates are not monotone at every adjacent threshold
  (τ=0.50 versus τ=0.55), and the strictest setting has a lower point estimate than 42%.
