# exp007 — model asymmetry on LiveCodeBench (pre-registered)

**Confirmatory replication of exp006's central result on a contamination-controlled oracle.
exp006 (HumanEval subset-30) finds that a frontier judge — or frontier judge + frontier test
author — cuts FALSE REJECTS beyond floor while FALSE ACCEPTS stay within noise in every
cell: asymmetric verification buys completeness, not soundness. HumanEval problems predate
every model's training data; this experiment asks whether the pattern holds on problems the
weak model cannot have memorized.**

## Design (frozen)

Same pipeline, cells, and parameters as exp006 (anchoring **both**, escalation **OFF**,
judge threshold 0.70, max retries 3; W = gpt-4o-mini, S = gpt-5.6-terra; S test-author
cells pin T=1.0 — gpt-5.x models accept only their default temperature). $N{=}5$ runs per
cell.

| cell | test author | code generator | judge (all three judge roles) |
|---|---|---|---|
| control        | W | W | W |
| strong_testgen | **S** | W | W |
| strong_judge   | W | W | **S** |
| strong_both    | **S** | W | **S** |

**Problem set (frozen, `problems/lcb30.json`):** LiveCodeBench code_generation_lite
release_v6, LeetCode platform only (functional task shape), contest_date >= 2025-01-01 —
more than a year past W's training cutoff (Oct 2023) and ~6 months past its release.
Deterministic rule: sort by (contest_date, question_id); all 19 easy problems in the window
plus the first 11 medium = 30 problems. Basis (pilot, `experiments/pilots/`): gpt-4o-mini
one-shot pass@1 is 0.75 on easy and 0.00 on medium/hard, so easy problems put W in the
measurable band and mediums give the strong cells headroom. The tier mix is recorded
per-problem and reported in descriptives.

**Oracle:** each stored implementation is scored against the problem's full public+private
LCB test set via `codegen_metrics` — the same function the official LCB evaluator calls —
in the LCB harness venv (`score_lcb.py`). Prompts see the problem statement and its public
worked examples only; private tests never leave the harness. Unlike HumanEval there is one
oracle (no base/plus split): FA = tdd_success ∧ oracle fail; FR = cycle failed ∧ oracle
pass.

**Contamination note (recorded honestly):** the window controls contamination for W (both
roles it plays) and for the claims about W's self-grading. S's training cutoff is not
public; if S has seen these problems, strong-judge cells could be flattered. The
FR-vs-FA decomposition is robust to this in one direction: memorization in the judge could
only *reduce* false accepts — so if FA still does not move (H-B2), the soundness-invariance
conclusion survives; if FA does move, S-contamination is a live alternative explanation and
is reported as such.

## Hypotheses and decision rules (frozen)

Floors as in exp006 (pre-registered practical floors): pass 4, FA 2, FR 2, verdict-error 3,
with the same escape valve (if this control's observed max pairwise spread exceeds a floor,
the larger value is used and recorded). Contrasts vs `control`: exact McNemar on per-problem
majority-of-5; SIGNAL requires $p<.05$ AND the floor.

- **H-B1 (confirmatory, from exp006):** strong_judge and strong_both reduce FR beyond
  floor vs control.
- **H-B2 (confirmatory, the soundness-invariance claim):** FA stays within noise in ALL
  cells (no strong cell moves FA beyond floor + significance).
- **H-B3 (open, directional):** strong_testgen raises oracle pass rate.
- Descriptives: per-cell tests/run and canonical-test counts, per-tier (easy/medium)
  breakdowns, judge score distributions, cost per cell.

Outcome mapping: H-B1 ∧ H-B2 → the completeness-not-soundness result generalizes off
HumanEval and the paper's discussion carries it as a main claim. H-B2 fails (FA drops beyond
floor + significance in strong-judge cells) → either the gap is partially closable by a
strong grader on unseen problems or S-contamination — the discussion reports both readings.
H-B1 fails → the FR effect was HumanEval-specific; report the null.

Contingencies as in exp006 (provider-rejected params recorded and retried with required
values; terminal API errors = failed problem-run). **Budget cap $80**, runner-enforced.

## Run

```bash
uv run pytest src/vgap/pipeline/test_lcb_adapter.py -q
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage plan
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage smoke    # 1 problem, strong_judge
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage run --cell <cell>
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage score    # LCB harness venv, no API
uv run python experiments/exp007_lcb_asymmetry/run_lcb.py --stage analyze
```

Scoring requires the LiveCodeBench harness checkout with its venv (see docs/RUNBOOK.md);
set `LCB_VENV_PY` if it is not at the default sibling path. Outputs under `results/`:
per-run summaries + tagged usage logs, `scores/`, `asym_summary.json`, `ANALYSIS.md`
(generated — never hand-edited).
