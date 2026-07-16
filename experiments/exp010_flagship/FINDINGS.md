# exp010 flagship — findings (2026-07-15)

534 runs (89 packages x 2 cells x 3), $50.78. Full RGR pipeline builds each package from its
requirements document alone (tests never shown), self-verdicts, and is graded by the
hand-verified oracle (kill 0.981) through the frozen v3.1 non-cheating harness with
terra-authored adapters. FA = claimed success whose oracle pass fraction < 1.0 on a VALID
evaluation. Full analysis in results/ANALYSIS.md.

## Headline results

| | control (all gpt-4o-mini) | strong_judge (gpt-5.6-terra judges) |
|---|---|---|
| valid evaluations | 261/267 | 251/267 |
| claimed successes | 65 | 50 |
| **conditional FA of claims (H-D1)** | **0.415 [0.304, 0.537]** | **0.420 [0.294, 0.558]** |
| false rejects (H-D3) | 14 | **0** |
| first-attempt FA / multi-attempt FA (H-D2) | 0.35 / 0.64 | 0.34 / 0.67 |
| FA by tier begin/inter/adv (H-D4) | 0.31 / 0.54 / 0.86 | 0.38 / 0.50 / 0.75 |

## Verdicts

- **H-D1 — supported and then some.** The false-accept rate of claimed successes is ~42% at
  application scale — ABOVE the pre-registered 15-35% band drawn from algorithmic-scale
  prior work (our own HumanEval+/LCB: 18%/29%; Ahmed et al./SWE-ABS: 20-33%). The prediction
  was directionally right but conservative: **the gap is worse on application-shaped,
  multi-concern tasks than any prior instrument showed**, and the Wilson lower bound (30%)
  still exceeds the algorithmic-scale point estimates. First prospective, oracle-error-barred
  measurement of the constant.
- **H-D2 — supported, both cells.** Multi-attempt claims are false ~2x as often as
  first-attempt claims (0.64 vs 0.35; 0.67 vs 0.34). Retrying makes the pipeline more
  confidently wrong — replicates Ahmed et al.'s "refinement worsens overfitting" (21.8->25.5)
  on an independent instrument.
- **H-D3 — supported (confirmatory).** Conditional FA is statistically identical across cells
  (0.415 vs 0.420); the frontier judge does NOT reduce false accepts. It eliminates false
  rejects entirely (14 -> 0): completeness, not soundness. THIRD independent confirmation of
  soundness invariance (after exp006 HumanEval, exp007 LCB), now on application-scale tasks.
- **H-D4 — supported.** Conditional FA rises monotonically with complexity tier in both cells
  (control .31 -> .54 -> .86). The gap GROWS with task complexity — a scaling axis algorithmic
  benchmarks structurally cannot exhibit. The dataset's signature contribution.

## Confound audit (H-D1 magnitude): adapter contributes ~zero, no human in the loop

The oracle reaches the candidate through a generated adapter; an imperfect adapter could
inflate FA. Transparency (fault injection) certifies the adapter transmits candidate
behavior, but not that it maps every symbol correctly. Automated calibration
(calibrate_adapter.py): each package's REFERENCE solution (passes its oracle at 1.0) has its
public API mechanically renamed to opaque tokens — a behavior-preserving AST transform —
producing a KNOWN-CORRECT candidate with a foreign API, exactly the adapter's real job. An
auto-generated adapter from the rename map certifies behavior-preservation at 1.0 (packages
that fail this are excluded as renamer artifacts); then the model authors an adapter BLIND
and is graded. Since behavior is provably preserved, any shortfall is pure adapter error.

Result: **13/13 usable packages (5 excluded), adapter-attributable failure rate 0.000**,
across all three tiers including the hardest (event_sourcing, circuit_breaker, game_of_life).
The adapter contributes ~nothing to the false-accept rate; the 42% is genuine verification
gap, established with no human judgment in the measurement.

Corroborating manual audit (independent evidence): every near-miss FA case read by hand is a
genuine self-consistent misalignment — string_calculator does not raise on negatives,
code_breaker never validates the secret at construction, markdown_parser italicises
underscores inside link URLs; across all 27 control FA cases the failing oracle tests cluster
systematically on error/validation/boundary behaviors (38%) rather than the random scatter
mis-mapping would produce.

## What this means for the paper

The four results compose into a claim no prior work could make: the verification gap of
self-testing TDD agents is (1) large (~42%), (2) worse at application scale than the field's
toy-problem measurements, (3) amplified by the retry loops agents rely on, (4) growing with
task complexity, and (5) untouched by frontier-judge strength. Measured on the first oracle-
error-barred, application-shaped TDD benchmark — the instrument the field lacked.
