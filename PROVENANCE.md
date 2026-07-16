# Provenance

This repository's history was linearized for release: each experiment appears as a
pre-registration commit (hypotheses, decision rules, budget cap — always predating its data)
followed by a results commit. The team's private working history — including two precursor
artifact-reconstruction studies that informed early direction but contribute no numbers to
the paper — is retained privately; `vgap_git_sha` values recorded inside result files refer
to the private working history and are resolvable on request.

The pipeline under `src/vgap/pipeline/` originates in a system from earlier, informal
experiments (late 2025), recreated here under line-by-line review and deliberately diverged
from it: the review's defects are fixed and the prompts rewritten to the contract the paper
describes. `src/vgap/pipeline/REVIEW.md` is the defect register. Every result in the paper
was produced on this instrument; the working notes and intermediate instrument revisions
live in the team's private archive, resolvable on request.

Template integrity: `templates/MANIFEST.sha256` fingerprints the five templates — every
user-turn prompt the pipeline sends is a template (the two judge calls additionally attach
short fixed system messages, defined in `coordinator.py`);
`templates_variants/` (anchoring-ablation variants) is regenerated mechanically from
`{# ANCHOR #}` markers by `scripts/make_variants.py` and carries its own manifest.
