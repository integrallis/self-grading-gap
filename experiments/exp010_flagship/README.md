# exp010 — FLAGSHIP: the verification gap on error-barred oracles (pre-registered)

**Committed before the first API call. The definitive measurement: the full RED-GREEN-VERIFY
TDD pipeline builds each package from its requirements document alone (tests never shown);
its executed self-verdict is captured; the produced implementation is graded by the
package's hand-verified oracle (mutation kill 0.981, survivors classified) through the
frozen protocol-v3.1 non-cheating harness. Replication targets from the literature are
built into the hypotheses (docs/LITERATURE_POSITIONING.md).**

## Design (frozen)

- System under test: vgap pipeline v4 (RED test-author -> judge -> GREEN -> exec gate ->
  VERIFY; escalation off; judge threshold 0.70; max retries 3). Anchoring blocks inactive
  (requirements carry no canonical I/O examples by design).
- Input: requirements/<pkg>.md from rgrbench @ pinned SHA. All 89 packages.
- Cells: **control** (gpt-4o-mini in every role) and **strong_judge** (gpt-4o-mini
  generation + tests, gpt-5.6-terra all judge roles) — the production-relevant asymmetry
  cells from exp006/007. N=3 runs per cell per package (534 pipeline runs).
- Grading: adapter authored by gpt-5.6-terra (protocol v3.1: import-surface + call shapes,
  one repair round); harness evaluate() with screened fault-injection transparency.
- Self-verdict = the pipeline's executed final test run (harness-captured, not reported).
- FA = self-verdict success AND oracle pass fraction < 1.0 on a VALID evaluation;
  FR = self-verdict failure AND oracle pass fraction = 1.0. Conditional gap =
  FA / claimed successes. Invalid evaluations are excluded and their taxonomy reported.

## Hypotheses (frozen; replication targets cited)

- **H-D1 (field constant; replicates Ahmed et al. 2511.16858, SWE-ABS):** the conditional
  false-accept rate of claimed successes lies in 15-35% (their range 19.7-33%; our prior
  18-29%). Report point estimate + Wilson 95% CI per cell — the first prospective,
  error-barred measurement of the constant.
- **H-D2 (refinement worsens; replicates Ahmed's 21.8->25.5):** among claimed successes,
  conditional FA rate is higher for cycles that used >1 GREEN attempt than for
  first-attempt successes (directional; report both rates + CI).
- **H-D3 (soundness invariance; confirmatory from exp006/007):** strong_judge does not
  reduce conditional FA (bar: |delta| > 5pp AND p<.05, two-proportion); FR falls and
  oracle pass rate rises (the coach effect), now on application-shaped tasks.
- **H-D4 (complexity scaling):** conditional FA rate is higher on advanced than beginner
  tier (directional with CI; the axis prior algorithmic benchmarks cannot exhibit).
- Descriptives: per-provenance splits; self-authored suite size vs oracle suite size;
  per-package transparency; adapter validity taxonomy; per-cell cost.

**Budget cap $250** (estimate $70-120), runner-enforced. Runs resumable per package/cell.
Results per package under results/<cell>/<pkg>/runN/; ANALYSIS.md generated, never edited.
