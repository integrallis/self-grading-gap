# Post hoc statistical audit

This analysis was designed during manuscript review after the original results were
available. It is **not a pre-registration**, an independent replication, or new model
data. It does not modify original model outputs or benchmark scores.

Run `python3 experiments/review_audit/run_audit.py` from the repository root. Only the
Python standard library is needed; it makes no API calls and does not execute any
generated code. Outputs are `results/audit.json`, `results/ANALYSIS.md`, and
`results/paper_numbers.tex`, also copied to `paper/audit_numbers.tex`. The JSON records
every consumed input's SHA-256, the runner's SHA-256, source revision, working-tree status,
UTC generation time, Python version, and the fixed resampling seed.

The audit computes complete, separate HumanEval base and HumanEval+ confusion matrices.
The original experiment analysis mixes base-oracle passes/false rejects with plus-oracle
false accepts. Those original results are retained as historical records. For all six
single-function arms, this supplement computes the original majority-of-five exact
McNemar test for false accepts, false rejects, total error, and oracle passes. It also
reports a paired problem-cluster bootstrap for the mean per-run changes.

For RGRBench, each bootstrap samples package IDs jointly across the compared cells and
keeps every run of a selected package together. This permits dependence between repeated
runs of the same package. Percentile intervals use 20,000 resamples and seed 20260913.
They are descriptive sensitivity analyses on selected tasks; they do not make the
benchmark representative of application development. Different cells still accept
different candidates. Conditional-rate contrasts describe complete pipeline policies,
not isolated judge discrimination on a fixed candidate set. Oracle-yield calculations
use the full design denominator; unknown oracle outcomes are not counted as known
passes, and missing-oracle conditional-rate bounds are reported separately.

The supplement also shows that no failures on the selected synthetic adapter-calibration
cases does not establish a zero population error bound. Its binomial upper bound is
illustrative, since the calibration packages were selected, not randomly sampled.

No new analyses in this directory may be described as confirmatory. P-values are
unadjusted; majority-outcome tests and average-per-run changes have different estimands.
