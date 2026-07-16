#!/usr/bin/env bash
# Reproduce every analysis table from committed raw results. No API keys.
set -e
cd "$(dirname "$0")"
echo "== environment =="
uv sync 2>&1 | tail -1
echo "== unit tests =="
uv run pytest src -q
echo "== exp006 model asymmetry (HumanEval subset-30): re-derive analysis =="
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage analyze | tail -14
echo "== exp007 model asymmetry (LiveCodeBench lcb30): re-derive analysis =="
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage analyze | tail -14
echo "== figures =="
uv run python scripts/make_figures.py
echo "== done: analyses match the committed ANALYSIS files; figures in paper/figures/ =="
