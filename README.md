# Who Grades the Grader? The Verification Gap in Self-Testing Code Agents

Reproducer repository for the paper ([`paper/main.pdf`](paper/main.pdf)). An instrumented
self-testing code pipeline is evaluated against held-out oracles on selected HumanEval and
LiveCodeBench problems and RGRBench application packages. Frontier test authors and judges
leave residual false accepts in every measured condition; no original false-accept contrast
meets the specified decision rule. This does **not** establish that stronger verification
cannot help. Some point estimates improve, and stricter application-scale gating reduces
correct output as well as acceptance.

The September 2026 review corrects mixed HumanEval oracle reporting, adds uncertainty that
accounts for repeated tasks, and distinguishes specification errors from requirements–oracle
mismatches. See [the review and changes](docs/REVIEW_AND_RELEASE.md),
[statistical audit](docs/STATISTICAL_REVIEW.md), and
[instrument audit](docs/INSTRUMENT_REVIEW.md). Original raw observations are preserved;
new analyses are explicitly post hoc. Public release history is reconstructed and does not
independently prove the private registration chronology; see [PROVENANCE.md](PROVENANCE.md).

Related methodological work: [What Context Does a Coding Agent Actually Need to Act?](https://arxiv.org/abs/2607.09691).
It studies context representation with independent outcome evaluation; it is not a replication
of this paper's verification-gap experiment.

## Layout

```
paper/                        the paper (main.tex, refs.bib, figures, PDF)
src/vgap/pipeline/            the pipeline under study: engine, judges, prompt templates
                              (ANCHOR-marked anchoring blocks), anchoring template variants,
                              REVIEW.md defect register, cost instrumentation
experiments/
  pilots/                     benchmark feasibility pilots (LiveCodeBench, SWT-Bench,
                              TDD-Bench Verified, TEBench) behind the exp007 oracle choice
  exp006_model_asymmetry/     pre-registered 4-cell model-asymmetry experiment on the
                              HumanEval subset-30 (EvalPlus oracles)
  exp007_lcb_asymmetry/       pre-registered confirmatory replication on LiveCodeBench
                              (post-cutoff problem window, hidden-test oracle)
  exp009_dataset_pilot/       RGRBench feasibility pilot and retained protocol revisions
  exp010_flagship/            application-scale RGRBench replication and adapter calibration
  exp011_verifier_generalization/ cross-provider verifier replication on both subsets
  exp013_tau_sweep/           RGRBench judge-threshold sensitivity study
  review_audit/               reproducible review analyses and manuscript-number macros
scripts/make_figures.py       regenerates every paper figure from committed result files
scripts/make_variants.py      regenerates the anchoring template variants from ANCHOR markers
docs/RUNBOOK.md               experimenter guide: keys, environments, running and scoring
docs/INSTRUMENT_REVIEW.md     implementation and provenance review, with remaining limitations
PROVENANCE.md                 history, instrument versioning, and artifact provenance notes
```

## Reproduce (no API keys)

```bash
./reproduce.sh
```

This installs the versions in `uv.lock`, runs the instrument and asymmetry-analysis tests,
then regenerates the exp006, exp007, exp010, exp011, and exp013 analyses, the review audit,
and paper figures. Initial dependency installation may need internet access. The analysis
stages use committed per-run outputs and stored oracle scores; they require no API keys,
RGRBench checkout, or LiveCodeBench checkout. They do not re-execute benchmark oracles or
regenerate model outputs. Generated analysis timestamps and current-checkout provenance
can differ from the archived analyses; the script does not assert byte-for-byte equality.

For individual stages, use the commands in [`reproduce.sh`](reproduce.sh). The original
asymmetry analyses retain their historical decision rules; the review audit reports
additional uncertainty and sensitivity analyses. Adapter calibration and the benchmark's
mutation measurements are archived empirical inputs, not rerun by this command.

## Run the experiments

See [`docs/RUNBOOK.md`](docs/RUNBOOK.md): required API keys, environments (including the
LiveCodeBench harness checkout that exp007's score stage shells out to), budget caps,
measured costs, and the original exp006/exp007 staged runners. Later experiments document
their designs in `README.md` or `PRE_REGISTRATION.md`; exp011 records collection changes in
[`DEVIATIONS.md`](experiments/exp011_verifier_generalization/DEVIATIONS.md). Read these
records before launching fresh runs. RGRBench generation and scoring additionally require
the separate dataset checkout named by `DATASET_DIR` (default `../rgrbench`).

The pipeline is a reviewed recreation of a 2025 system with its defects fixed and its
prompts rewritten; `src/vgap/pipeline/REVIEW.md` is the defect register, and PROVENANCE.md
records the artifact's provenance.

The release history was reconstructed, and historical run SHAs refer to private working
history. The public checkout supports reanalysis of the released outputs, but does not by
itself establish the original timing of every registration or supply every intermediate
prompt and discarded run. See [`PROVENANCE.md`](PROVENANCE.md) and the instrument review
for the limits of exact historical replay.

## Paper

```bash
./reproduce.sh
cd paper && latexmk -pdf main.tex
```

The PDF build additionally requires a TeX installation with `latexmk`. If only the standard
TeX executables are available, run `pdflatex main.tex`, `bibtex main`, then
`pdflatex main.tex` twice from `paper/` after regenerating the analyses.
Alternatively, `tectonic --untrusted --keep-intermediates paper/main.tex` builds the PDF
and bibliography with Tectonic. `python3 scripts/package_paper.py` then prepares a local
PDF/source bundle and submission text under `release/`; it does not upload anything.
