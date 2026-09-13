# Provenance

This repository's history was reconstructed and linearized for release. Experiment design
documents retain the authors' registration claims, hypotheses, decision rules, and budget
caps, but the public Git history does not independently establish their original timing.
For example, exp010's design document and results first appear together in the public
release commit. A release commit timestamp must not be used as evidence that a design was
fixed before collection.

The team's private working history — including two precursor artifact-reconstruction
studies that informed early direction but contribute no numbers to the paper — is retained
privately. Historical `vgap_git_sha` values in result files refer to that working history
and may not resolve in this checkout; the authors offer the corresponding private records
on request. Independent verification of the original registration sequence requires those
records or another contemporaneously timestamped archive. Later changes and collection
deviations are described in the experiment-specific records, including exp011's
`DEVIATIONS.md`; the released collection is not a complete archive of every discarded
attempt.

The pipeline under `src/vgap/pipeline/` originates in a system from earlier, informal
experiments (late 2025), recreated here under line-by-line review and deliberately diverged
from it: the review's defects are fixed and the prompts rewritten to the contract the paper
describes. `src/vgap/pipeline/REVIEW.md` is the defect register. Every result in the paper
was produced on this instrument; the working notes and intermediate instrument revisions
live in the team's private archive, resolvable on request.

Template integrity: `src/vgap/pipeline/templates/MANIFEST.sha256` fingerprints the five
pipeline templates and their configuration. Pipeline user-turn prompts use these templates;
two judge calls additionally attach fixed system messages defined in `coordinator.py`.
Offline adapter-authoring prompts are constructed separately in experiment runners.
`src/vgap/pipeline/templates_variants/` (anchoring-ablation variants) is regenerated
mechanically from `{# ANCHOR #}` markers by `scripts/make_variants.py` and carries its own
manifest. These released fingerprints identify current files; they do not reconstruct
missing per-run historical hashes.

The artifact supports reanalysis of released model outputs and stored oracle verdicts.
Exact historical replay has additional limits: some model IDs are aliases rather than
resolved snapshots, historical dependency and input hashes are incomplete, and the
RGRBench runs do not include all intermediate prompts, judge feedback, or execution
transcripts. See `docs/INSTRUMENT_REVIEW.md` for concrete coverage and limitations. A fresh
generation run or oracle execution is distinct from the offline analysis stages in
`reproduce.sh` and may require external datasets, harnesses, or paid model access.
