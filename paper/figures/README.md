# Figure sources

The manuscript explicitly selects these illustration files:

| File | Source and use |
| --- | --- |
| `fig1_loop.png` | Original supplied loop illustration, unchanged. Included at full text width to preserve its positioning and improve legibility. |
| `fig6_requirements_oracle.png` | Corrected copy of the supplied `fig6_misalignment.png`, preserving its detailed requirements, test, code, pipeline, and oracle layout. Printed on a landscape page so the code remains legible. |

The original `fig6_misalignment.png` is retained for provenance. It is not included in
the manuscript because its title and footer incorrectly interpret the example as a
demonstrated misreading of the supplied requirement.

The corrected copy was made on 2026-09-13 with the built-in image generation tool in
edit mode. The [complete edit prompt](fig6_edit_prompt.txt) records the requested
changes. The title and footer now identify an omitted exception type; the test
annotation distinguishes exception type from the message check, and the oracle
annotation identifies its additional type requirement. The original layout, code
callouts, and recorded 20/22 oracle result are preserved. The caption identifies the
snippets as simplified: the displayed self-test omits the raw-string notation and
regex escaping shown in the recorded test and Appendix D.

This is an explanatory illustration, not a new experiment or a generated source of
evidence. Appendix D of `paper/main.tex` contains the full requirement and code
excerpts. The recorded candidate, self-tests, and oracle result are in
`experiments/exp010_flagship/results/strong_judge/numbers_to_words/run1/`.

`scripts/make_figures.py` regenerates the four data plots (`fig2_asym.pdf`,
`fig3_complexity.pdf`, `fig4_convergence.pdf`, and `fig5_verifiers.pdf`) from the
recorded results and post hoc audit. It also produces simplified vector schematic
alternatives, `fig1_loop.pdf` and `fig6_misalignment.pdf`. The manuscript uses the
PNG illustrations above; running the script does not overwrite those assets.
Figure numbers in the compiled paper follow their order in `main.tex`, which differs
from the numeric prefixes in the filenames.
