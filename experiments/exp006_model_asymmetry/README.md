# exp006 — model asymmetry: strong test author / strong judge (pre-registered)

**Motivated by a direct challenge to the thesis from production experience: deployed TDD
agent systems reportedly work well with a frontier model authoring tests and a cheaper model
writing code, and a frontier judge is the other natural upgrade. If a strong test author or
a strong judge dramatically shrinks the verification gap, the thesis narrows from "the loop
cannot grade itself" to "the loop cannot grade itself under model symmetry" — and asymmetric
verification becomes the paper's constructive answer. Predictions are directional per that
challenge; the outcome is open and either result reshapes the discussion.**

## Design (frozen)

The study pipeline on a 30-problem HumanEval subset enriched for run-unstable problems
(problem IDs frozen in `run_asym.py`; rates on this subset are not benchmark rates).
Anchoring **both** (default templates), **escalation OFF** in all cells (escalation model
pinned to the generator), judge threshold 0.70, max retries 3. Weak model W = gpt-4o-mini
(generation T=0.7 / judging T=1.0); strong model S = gpt-5.6-terra (same provider as W —
single-variable manipulation, no cross-provider format confound; gpt-5.x models accept only
their default temperature, so S test-author cells pin T=1.0). $N{=}5$ runs per cell.

| cell | test author | code generator | judge (all three judge roles) |
|---|---|---|---|
| control_rerun | W | W | W |
| strong_testgen | **S** | W | W |
| strong_judge | W | W | **S** |
| strong_both | **S** | W | **S** |

## Measures and decision rules (frozen)

Oracle scoring (EvalPlus base+plus on every stored implementation) is a protocol stage.
Per cell and run: oracle pass /30, false accepts vs base and vs plus (tdd_success ∧ oracle
fail), false rejects (cycle failed ∧ base pass), total verdict error (FA-plus + FR), cost.

Contrasts vs `control_rerun`, exact McNemar on per-problem majority-of-5 status, gated on
pre-registered practical floors: **pass-rate floor 4**, **FA floor 2**, **FR floor 2**,
**verdict-error floor 3**. If the control's observed max pairwise spread exceeds a floor,
the larger value is used (and recorded in the analysis). SIGNAL requires $p<.05$ AND the
floor.

- **H-A1 (challenger's primary):** strong_judge reduces FA-plus vs control.
- **H-A2:** strong_testgen reduces FA-plus vs control.
- **H-A3 (thesis-critical):** strong cells reduce TOTAL verdict error — reduction, not
  relocation between FA and FR.
- Descriptives: per-cell test-suite size and canonical-test counts; judge score
  distributions; cost per cell (asymmetry's price is part of the production question).

Contingencies: provider-rejected parameters are recorded and retried with the provider's
required values; terminal API errors count as failed problem-runs. **Budget cap $120**,
runner-enforced.

## Run

```bash
uv run pytest experiments/exp006_model_asymmetry -q
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage plan
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage smoke     # 1 problem, strong_judge
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage run --cell <cell>   # resumable
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage score    # EvalPlus, no API
uv run python experiments/exp006_model_asymmetry/run_asym.py --stage analyze
```

Outputs under `results/`: per-run summaries + tagged usage logs, `scores/`,
`asym_summary.json`, `ANALYSIS.md` (generated — never hand-edited).
