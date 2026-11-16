# Shared manuscript sources

The [canonical paper](../../paper/main.tex) remains unchanged. Its unabridged reflow in the official IEEE conference template is [17 pages](../se4agenticai-2026/full-length.pdf); the editorially shortened [SE4AgenticAI draft](../se4agenticai-2026/review.pdf) is **10 pages including references**. These are local drafts, not submissions.

## What the shorter version retains

- The canonical abstract, verbatim, and all **39 citation keys** used by the full paper; both were checked against `paper/main.tex`.
- Four result tables: the main configuration results, frontier verifiers, RGRBench results, and threshold follow-up.
- Two key figures: the pipeline overview and the requirement/oracle disagreement example.
- The distinction between benchmark disagreement and semantic correctness, inconclusive intervention evidence, prompt and information-access limitations, reconstructed registration chronology, post-hoc analyses, and benchmark/selection caveats.

The introduction and related work are shorter; methods and discussion are condensed into prose. Redundant result plots, the separate configuration table, algorithm pseudocode, and long appendices remain in the full-length edition and supporting [artifact](https://github.com/integrallis/self-grading-gap). Their essential methodological details and qualifications remain in the review text. Shortening adds no experiments or results.

## Source layout

| Files | Purpose |
| --- | --- |
| `abstract.tex`, `full-body.tex`, `appendices.tex` | Generated extracts of the canonical manuscript, with layout adaptations for the full-length IEEE edition. |
| `source-manifest.json` | Hashes of the canonical text, bibliography, numerical inputs, and figures. |
| `review-body.tex`, `sections/*.tex` | Hand-edited shorter manuscript, shared by venue variants. |
| `pipeline-figure.tex` | Shared pipeline figure and caption. |
| `ieee-preamble.tex`, `authors-ieee.tex` | Shared IEEE presentation and author information. |

Each venue's `content.tex` selects the shared editorial manuscript. Venue wrappers control presentation; unresolved calls do not yet have final wrappers.

## Updating the drafts

`python3 submissions/prepare.py` regenerates **only** `abstract.tex`, `full-body.tex`, `appendices.tex`, and `source-manifest.json`. It does not update `review-body.tex` or `sections/`. Changes to the canonical paper therefore require manual scientific reconciliation of the shortened text before rebuilding; a fresh manifest alone does not establish consistency.

`python3 submissions/build.py se4agenticai-2026` builds the shorter IEEE draft; add `--full` for the unabridged edition. The build checks canonical input hashes and records page count, unresolved references, and overfull boxes in the venue's check report. The current ten-page review build reports no unresolved references or overfull boxes.
