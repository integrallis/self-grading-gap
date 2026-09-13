# Post hoc statistical review (generated; do not hand-edit)

No new model calls. Original results are preserved. This supplementary analysis is not preregistered.
Bootstrap: 20,000 replicates, seed 20260913; whole problems/packages retain all repeated runs.
Intervals characterize resampling of the selected tasks, not representative benchmark sampling.

## Complete matrices: per-run means on each oracle

| Experiment | Cell | Oracle | Pass | TA | FA | FR | TR | Conditional FA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| exp006 | control_rerun | base | 24.0 | 18.6 | 3.0 | 5.4 | 3.0 | 13.9% |
| exp006 | control_rerun | plus | 22.6 | 17.6 | 4.0 | 5.0 | 3.4 | 18.5% |
| exp006 | strong_both | base | 26.2 | 24.6 | 2.0 | 1.6 | 1.8 | 7.5% |
| exp006 | strong_both | plus | 24.8 | 23.2 | 3.4 | 1.6 | 1.8 | 12.8% |
| exp006 | strong_judge | base | 24.6 | 22.2 | 3.4 | 2.4 | 2.0 | 13.3% |
| exp006 | strong_judge | plus | 23.4 | 21.2 | 4.4 | 2.2 | 2.2 | 17.2% |
| exp006 | strong_testgen | base | 25.2 | 21.6 | 2.2 | 3.6 | 2.6 | 9.2% |
| exp006 | strong_testgen | plus | 24.2 | 20.6 | 3.2 | 3.6 | 2.6 | 13.4% |
| exp007 | control | hidden | 15.2 | 11.8 | 4.8 | 3.4 | 10.0 | 28.9% |
| exp007 | strong_both | hidden | 21.4 | 21.4 | 3.0 | 0.0 | 5.6 | 12.3% |
| exp007 | strong_judge | hidden | 20.2 | 20.2 | 2.4 | 0.0 | 7.4 | 10.6% |
| exp007 | strong_testgen | hidden | 16.4 | 14.2 | 2.8 | 2.2 | 10.8 | 16.5% |
| exp011_he_gemini | control | base | 23.6 | 19.6 | 3.8 | 4.0 | 2.6 | 16.2% |
| exp011_he_gemini | control | plus | 22.4 | 18.6 | 4.8 | 3.8 | 2.8 | 20.5% |
| exp011_he_gemini | strong_both | base | 25.6 | 23.4 | 3.8 | 2.2 | 0.6 | 14.0% |
| exp011_he_gemini | strong_both | plus | 24.2 | 22.4 | 4.8 | 1.8 | 1.0 | 17.6% |
| exp011_he_gemini | strong_judge | base | 23.6 | 20.8 | 2.8 | 2.8 | 3.6 | 11.9% |
| exp011_he_gemini | strong_judge | plus | 22.4 | 19.6 | 4.0 | 2.8 | 3.6 | 16.9% |
| exp011_he_gemini | strong_testgen | base | 26.4 | 22.0 | 1.2 | 4.4 | 2.4 | 5.2% |
| exp011_he_gemini | strong_testgen | plus | 24.4 | 20.0 | 3.2 | 4.4 | 2.4 | 13.8% |
| exp011_he_claude | control | base | 23.8 | 19.0 | 2.8 | 4.8 | 3.4 | 12.8% |
| exp011_he_claude | control | plus | 22.8 | 18.0 | 3.8 | 4.8 | 3.4 | 17.4% |
| exp011_he_claude | strong_both | base | 26.0 | 24.6 | 2.6 | 1.4 | 1.4 | 9.6% |
| exp011_he_claude | strong_both | plus | 24.2 | 23.0 | 4.2 | 1.2 | 1.6 | 15.4% |
| exp011_he_claude | strong_judge | base | 24.6 | 22.4 | 2.8 | 2.2 | 2.6 | 11.1% |
| exp011_he_claude | strong_judge | plus | 23.8 | 21.8 | 3.4 | 2.0 | 2.8 | 13.5% |
| exp011_he_claude | strong_testgen | base | 26.0 | 22.0 | 1.6 | 4.0 | 2.4 | 6.8% |
| exp011_he_claude | strong_testgen | plus | 24.8 | 20.8 | 2.8 | 4.0 | 2.4 | 11.9% |
| exp011_lcb_gemini | control | hidden | 15.2 | 12.6 | 3.8 | 2.6 | 11.0 | 23.2% |
| exp011_lcb_gemini | strong_both | hidden | 21.6 | 21.2 | 2.6 | 0.4 | 5.8 | 10.9% |
| exp011_lcb_gemini | strong_judge | hidden | 16.0 | 12.6 | 3.4 | 3.4 | 10.6 | 21.2% |
| exp011_lcb_gemini | strong_testgen | hidden | 18.8 | 17.4 | 1.8 | 1.4 | 9.4 | 9.4% |
| exp011_lcb_claude | control | hidden | 14.8 | 12.0 | 3.6 | 2.8 | 11.6 | 23.1% |
| exp011_lcb_claude | strong_both | hidden | 16.6 | 15.2 | 3.6 | 1.4 | 9.8 | 19.1% |
| exp011_lcb_claude | strong_judge | hidden | 15.0 | 13.0 | 3.4 | 2.0 | 11.6 | 20.7% |
| exp011_lcb_claude | strong_testgen | hidden | 16.8 | 13.8 | 2.0 | 3.0 | 11.2 | 12.7% |

## Original majority-outcome tests, completed for all outcomes

These p-values are unadjusted. Majority-of-five and mean-per-run changes are different estimands.
The original runners tested only FA and pass, omitting FR and total-error p-values.

| Experiment | Cell | Oracle | Outcome | Δ per 30 | McNemar p | Problem bootstrap Δ CI |
|---|---|---|---|---:|---:|---:|
| exp006 | strong_both | base | FA | -1.0 | 1.00000 | [-3.0, 0.2] |
| exp006 | strong_both | base | FR | -3.8 | 0.12500 | [-6.4, -1.4] |
| exp006 | strong_both | base | verdict_error | -4.8 | 0.03125 | [-7.8, -2.0] |
| exp006 | strong_both | base | oracle_pass | +2.2 | 1.00000 | [-0.2, 5.0] |
| exp006 | strong_both | plus | FA | -0.6 | 1.00000 | [-2.6, 1.0] |
| exp006 | strong_both | plus | FR | -3.4 | 0.12500 | [-6.0, -1.2] |
| exp006 | strong_both | plus | verdict_error | -4.0 | 0.03125 | [-7.0, -1.2] |
| exp006 | strong_both | plus | oracle_pass | +2.2 | 0.62500 | [-0.6, 5.4] |
| exp006 | strong_judge | base | FA | +0.4 | 1.00000 | [-1.0, 1.8] |
| exp006 | strong_judge | base | FR | -3.0 | 0.25000 | [-5.6, -0.8] |
| exp006 | strong_judge | base | verdict_error | -2.6 | 0.12500 | [-5.4, -0.0] |
| exp006 | strong_judge | base | oracle_pass | +0.6 | 1.00000 | [-0.8, 2.4] |
| exp006 | strong_judge | plus | FA | +0.4 | 1.00000 | [-1.0, 1.8] |
| exp006 | strong_judge | plus | FR | -2.8 | 0.25000 | [-5.4, -0.6] |
| exp006 | strong_judge | plus | verdict_error | -2.4 | 0.12500 | [-5.2, -0.0] |
| exp006 | strong_judge | plus | oracle_pass | +0.8 | 1.00000 | [-0.8, 2.8] |
| exp006 | strong_testgen | base | FA | -0.8 | 1.00000 | [-2.6, 0.4] |
| exp006 | strong_testgen | base | FR | -1.8 | 0.62500 | [-4.2, 0.4] |
| exp006 | strong_testgen | base | verdict_error | -2.6 | 0.21875 | [-5.4, -0.0] |
| exp006 | strong_testgen | base | oracle_pass | +1.2 | 1.00000 | [-0.8, 3.8] |
| exp006 | strong_testgen | plus | FA | -0.8 | 1.00000 | [-2.6, 0.4] |
| exp006 | strong_testgen | plus | FR | -1.4 | 0.62500 | [-3.8, 1.0] |
| exp006 | strong_testgen | plus | verdict_error | -2.2 | 0.21875 | [-5.0, 0.4] |
| exp006 | strong_testgen | plus | oracle_pass | +1.6 | 1.00000 | [-0.8, 4.4] |
| exp007 | strong_both | hidden | FA | -1.8 | 0.37500 | [-4.6, 0.6] |
| exp007 | strong_both | hidden | FR | -3.4 | 0.50000 | [-5.8, -1.4] |
| exp007 | strong_both | hidden | verdict_error | -5.2 | 0.12500 | [-8.4, -2.2] |
| exp007 | strong_both | hidden | oracle_pass | +6.2 | 0.01562 | [3.4, 9.4] |
| exp007 | strong_judge | hidden | FA | -2.4 | 0.12500 | [-5.2, 0.0] |
| exp007 | strong_judge | hidden | FR | -3.4 | 0.50000 | [-5.8, -1.4] |
| exp007 | strong_judge | hidden | verdict_error | -5.8 | 0.03125 | [-8.8, -3.0] |
| exp007 | strong_judge | hidden | oracle_pass | +5.0 | 0.03125 | [2.2, 8.2] |
| exp007 | strong_testgen | hidden | FA | -2.0 | 0.12500 | [-4.2, -0.2] |
| exp007 | strong_testgen | hidden | FR | -1.2 | 1.00000 | [-2.6, -0.0] |
| exp007 | strong_testgen | hidden | verdict_error | -3.2 | 0.21875 | [-5.6, -1.0] |
| exp007 | strong_testgen | hidden | oracle_pass | +1.2 | 0.50000 | [-0.8, 3.2] |
| exp011_he_gemini | strong_both | base | FA | +0.0 | 1.00000 | [-4.0, 4.0] |
| exp011_he_gemini | strong_both | base | FR | -1.8 | 0.37500 | [-5.4, 1.6] |
| exp011_he_gemini | strong_both | base | verdict_error | -1.8 | 0.28906 | [-6.2, 2.6] |
| exp011_he_gemini | strong_both | base | oracle_pass | +2.0 | 0.37500 | [-1.4, 5.6] |
| exp011_he_gemini | strong_both | plus | FA | +0.0 | 1.00000 | [-4.4, 4.2] |
| exp011_he_gemini | strong_both | plus | FR | -2.0 | 0.37500 | [-5.6, 1.4] |
| exp011_he_gemini | strong_both | plus | verdict_error | -2.0 | 0.34375 | [-6.8, 2.6] |
| exp011_he_gemini | strong_both | plus | oracle_pass | +1.8 | 0.68750 | [-1.8, 5.8] |
| exp011_he_gemini | strong_judge | base | FA | -1.0 | 1.00000 | [-2.6, 0.0] |
| exp011_he_gemini | strong_judge | base | FR | -1.2 | 0.25000 | [-4.0, 1.0] |
| exp011_he_gemini | strong_judge | base | verdict_error | -2.2 | 0.25000 | [-5.0, 0.0] |
| exp011_he_gemini | strong_judge | base | oracle_pass | +0.0 | 0.50000 | [-2.0, 2.2] |
| exp011_he_gemini | strong_judge | plus | FA | -0.8 | 1.00000 | [-2.4, 0.4] |
| exp011_he_gemini | strong_judge | plus | FR | -1.0 | 0.25000 | [-3.6, 1.0] |
| exp011_he_gemini | strong_judge | plus | verdict_error | -1.8 | 0.25000 | [-4.6, 0.6] |
| exp011_he_gemini | strong_judge | plus | oracle_pass | +0.0 | 1.00000 | [-2.4, 2.4] |
| exp011_he_gemini | strong_testgen | base | FA | -2.6 | 0.25000 | [-5.8, 0.0] |
| exp011_he_gemini | strong_testgen | base | FR | +0.4 | 1.00000 | [-2.2, 3.4] |
| exp011_he_gemini | strong_testgen | base | verdict_error | -2.2 | 0.45312 | [-6.4, 2.0] |
| exp011_he_gemini | strong_testgen | base | oracle_pass | +2.8 | 0.12500 | [0.2, 6.0] |
| exp011_he_gemini | strong_testgen | plus | FA | -1.6 | 0.62500 | [-5.2, 1.6] |
| exp011_he_gemini | strong_testgen | plus | FR | +0.6 | 1.00000 | [-2.2, 3.6] |
| exp011_he_gemini | strong_testgen | plus | verdict_error | -1.0 | 0.72656 | [-5.6, 3.4] |
| exp011_he_gemini | strong_testgen | plus | oracle_pass | +2.0 | 0.62500 | [-1.2, 5.6] |
| exp011_he_claude | strong_both | base | FA | -0.2 | 1.00000 | [-2.8, 2.6] |
| exp011_he_claude | strong_both | base | FR | -3.4 | 0.25000 | [-6.0, -1.2] |
| exp011_he_claude | strong_both | base | verdict_error | -3.6 | 0.21875 | [-6.8, -0.6] |
| exp011_he_claude | strong_both | base | oracle_pass | +2.2 | 0.25000 | [-0.6, 5.4] |
| exp011_he_claude | strong_both | plus | FA | +0.4 | 1.00000 | [-2.2, 3.4] |
| exp011_he_claude | strong_both | plus | FR | -3.6 | 0.25000 | [-6.2, -1.4] |
| exp011_he_claude | strong_both | plus | verdict_error | -3.2 | 0.21875 | [-6.6, 0.0] |
| exp011_he_claude | strong_both | plus | oracle_pass | +1.4 | 0.50000 | [-1.2, 4.6] |
| exp011_he_claude | strong_judge | base | FA | +0.0 | 1.00000 | [-1.4, 1.6] |
| exp011_he_claude | strong_judge | base | FR | -2.6 | 0.62500 | [-5.6, 0.0] |
| exp011_he_claude | strong_judge | base | verdict_error | -2.6 | 0.68750 | [-5.6, 0.2] |
| exp011_he_claude | strong_judge | base | oracle_pass | +0.8 | 1.00000 | [-1.2, 2.8] |
| exp011_he_claude | strong_judge | plus | FA | -0.4 | 1.00000 | [-2.0, 1.4] |
| exp011_he_claude | strong_judge | plus | FR | -2.8 | 0.62500 | [-5.8, -0.2] |
| exp011_he_claude | strong_judge | plus | verdict_error | -3.2 | 0.68750 | [-6.2, -0.4] |
| exp011_he_claude | strong_judge | plus | oracle_pass | +1.0 | 1.00000 | [-1.0, 3.2] |
| exp011_he_claude | strong_testgen | base | FA | -1.2 | 1.00000 | [-2.6, -0.2] |
| exp011_he_claude | strong_testgen | base | FR | -0.8 | 1.00000 | [-3.4, 1.6] |
| exp011_he_claude | strong_testgen | base | verdict_error | -2.0 | 0.62500 | [-4.8, 0.6] |
| exp011_he_claude | strong_testgen | base | oracle_pass | +2.2 | 0.50000 | [-0.2, 5.2] |
| exp011_he_claude | strong_testgen | plus | FA | -1.0 | 1.00000 | [-2.4, 0.0] |
| exp011_he_claude | strong_testgen | plus | FR | -0.8 | 1.00000 | [-3.4, 1.6] |
| exp011_he_claude | strong_testgen | plus | verdict_error | -1.8 | 0.62500 | [-4.6, 0.8] |
| exp011_he_claude | strong_testgen | plus | oracle_pass | +2.0 | 0.50000 | [-0.4, 5.0] |
| exp011_lcb_gemini | strong_both | hidden | FA | -1.2 | 1.00000 | [-2.8, 0.4] |
| exp011_lcb_gemini | strong_both | hidden | FR | -2.2 | 1.00000 | [-4.4, -0.2] |
| exp011_lcb_gemini | strong_both | hidden | verdict_error | -3.4 | 0.50000 | [-6.0, -1.0] |
| exp011_lcb_gemini | strong_both | hidden | oracle_pass | +6.4 | 0.01562 | [3.0, 10.0] |
| exp011_lcb_gemini | strong_judge | hidden | FA | -0.4 | 0.50000 | [-2.6, 1.6] |
| exp011_lcb_gemini | strong_judge | hidden | FR | +0.8 | 1.00000 | [-1.2, 2.6] |
| exp011_lcb_gemini | strong_judge | hidden | verdict_error | +0.4 | 1.00000 | [-2.4, 3.2] |
| exp011_lcb_gemini | strong_judge | hidden | oracle_pass | +0.8 | 1.00000 | [-2.4, 4.0] |
| exp011_lcb_gemini | strong_testgen | hidden | FA | -2.0 | 0.50000 | [-4.0, -0.4] |
| exp011_lcb_gemini | strong_testgen | hidden | FR | -1.2 | 1.00000 | [-3.6, 1.0] |
| exp011_lcb_gemini | strong_testgen | hidden | verdict_error | -3.2 | 0.62500 | [-6.0, -0.4] |
| exp011_lcb_gemini | strong_testgen | hidden | oracle_pass | +3.6 | 0.62500 | [0.8, 6.6] |
| exp011_lcb_claude | strong_both | hidden | FA | -0.0 | 1.00000 | [-2.4, 2.4] |
| exp011_lcb_claude | strong_both | hidden | FR | -1.4 | 0.50000 | [-4.0, 0.8] |
| exp011_lcb_claude | strong_both | hidden | verdict_error | -1.4 | 1.00000 | [-4.6, 1.6] |
| exp011_lcb_claude | strong_both | hidden | oracle_pass | +1.8 | 0.50000 | [-0.8, 4.6] |
| exp011_lcb_claude | strong_judge | hidden | FA | -0.2 | 1.00000 | [-2.2, 1.8] |
| exp011_lcb_claude | strong_judge | hidden | FR | -0.8 | 0.50000 | [-3.2, 1.2] |
| exp011_lcb_claude | strong_judge | hidden | verdict_error | -1.0 | 0.62500 | [-3.8, 1.6] |
| exp011_lcb_claude | strong_judge | hidden | oracle_pass | +0.2 | 0.50000 | [-2.0, 2.8] |
| exp011_lcb_claude | strong_testgen | hidden | FA | -1.6 | 1.00000 | [-3.6, 0.2] |
| exp011_lcb_claude | strong_testgen | hidden | FR | +0.2 | 1.00000 | [-1.8, 2.6] |
| exp011_lcb_claude | strong_testgen | hidden | verdict_error | -1.4 | 1.00000 | [-4.2, 1.6] |
| exp011_lcb_claude | strong_testgen | hidden | oracle_pass | +2.0 | 0.50000 | [0.0, 4.4] |

## RGRBench: package-cluster uncertainty and missing-oracle bounds

Δ = strong minus control conditional FA, in percentage points. Each bootstrap samples the same
package IDs for both cells and retains all runs, allowing different accepted sets in each cell.
This is an operating-policy comparison, not a judge discrimination test on fixed candidates.

| Strong threshold | Control FA% [cluster CI] | Strong FA% [cluster CI] | Δ FA pp [cluster CI] | Strong missing-oracle bounds |
|---|---:|---:|---:|---:|
| tau0.70 | 41.5 [26.0, 58.2] | 42.0 [23.1, 63.4] | +0.5 [-19.4, 20.8] | [40.4, 44.2] |
| tau0.40 | 41.5 [26.0, 58.2] | 67.6 [51.5, 82.1] | +26.0 [11.2, 40.9] | [65.8, 68.4] |
| tau0.50 | 41.5 [26.0, 58.2] | 47.5 [32.6, 63.4] | +6.0 [-9.4, 21.5] | [46.9, 48.1] |
| tau0.55 | 41.5 [26.0, 58.2] | 52.9 [28.6, 76.9] | +11.4 [-9.3, 31.9] | [52.9, 52.9] |
| tau0.85 | 41.5 [26.0, 58.2] | 33.3 [0.0, 75.0] | -8.2 [-45.5, 32.5] | [33.3, 33.3] |

Control missing-oracle bounds: [41.5, 41.5]%.
Bounds classify all claimed successes with missing oracle verdicts as correct or incorrect;
they do not repair possible oracle/specification disagreement or adapter errors in valid cases.

## Adapter calibration

Observed failures: 0/13 usable cases; 5 excluded.
Even under an illustrative IID binomial model, the one-sided 95% upper bound is 20.6%, not zero.
Illustrative binomial bound only; these selected synthetic packages are not a random sample of generated candidates.

## Interpretation limits

- Failure to pass a significance/effect-size bar does not demonstrate equivalence or absence of benefit.
- Treat unadjusted p-values as nominal; no familywise correction was preregistered.
- GREEN retry count and difficulty strata are observational subsets; their differences do not establish a causal retry or complexity effect.
- The tau sweep changes RED and GREEN thresholds, and its 0.50 point is an adaptive follow-up.
- New complete HumanEval+ pass/FR matrices correct the original mixture of base pass/FR with plus FA.
