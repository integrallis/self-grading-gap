#!/usr/bin/env bash
# Recompute the supported analyses and figures from committed results. No model calls.
set -euo pipefail
cd "$(dirname "$0")"
echo "== environment =="
uv sync --frozen
echo "== unit tests =="
uv run --frozen pytest src experiments/exp006_model_asymmetry/test_asym.py -q
echo "== exp006 model asymmetry (HumanEval subset-30): re-derive analysis =="
uv run --frozen python experiments/exp006_model_asymmetry/run_asym.py --stage analyze
echo "== exp007 model asymmetry (LiveCodeBench lcb30): re-derive analysis =="
uv run --frozen python experiments/exp007_lcb_asymmetry/run_lcb.py --stage analyze
echo "== exp010 application-scale replication =="
uv run --frozen python experiments/exp010_flagship/run_flagship.py --stage analyze
echo "== exp011 verifier replication =="
for verifier in claude gemini; do
  uv run --frozen python experiments/exp011_verifier_generalization/run_he.py --verifier "$verifier" --stage analyze
  uv run --frozen python experiments/exp011_verifier_generalization/run_lcb.py --verifier "$verifier" --stage analyze
done
echo "== exp013 threshold sweep =="
uv run --frozen python experiments/exp013_tau_sweep/run_tau_sweep.py --stage analyze
echo "== review audit: package-level uncertainty and sensitivity analyses =="
uv run --frozen python experiments/review_audit/run_audit.py
echo "== figures =="
uv run --frozen python scripts/make_figures.py
echo "== done: analyses regenerated under experiments/; figures in paper/figures/ =="
