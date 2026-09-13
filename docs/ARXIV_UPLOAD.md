# arXiv upload troubleshooting

## Current status: original record still errors; fresh draft compiles but is not submitted

On September 13, 2026, fresh draft **8074393** passed arXiv's live preflight and
compiled successfully with **pdfLaTeX / TeX Live 2025**, producing a **23-page PDF**.
Saving its metadata then produced an explicit duplicate-submission block referring
to the existing submission **7939730**. The revised paper has **not been submitted**
through the fresh draft. The existing submission remains preserved. Both records
are listed as **incomplete**, with the same September 27 expiration date; this
date is not their original submission date. The author subsequently preferred
repairing the original record and retiring the fresh draft if possible. Preserving
the original record does not establish that it retains a moderation queue position.

The author authorized trying a fresh submission if needed. The new record contains
the same paper, so the interface's exception for a different article with a report
number does not apply. The remaining blocker is the duplicate-submission check;
the original record's server error also remains unresolved. The
[support draft](ARXIV_SUPPORT_REQUEST.txt) records both problems and has not been sent.

## Original record: missing controls and a remaining server exception

The author first reported that uploading `self-grading-gap-reviewed-source.tar.gz`
to **7939730** and clicking **Check Files** produced
“Error: Missing files or top-level files.” The accompanying server exception gave
the timestamp **Sun Sep 13 18:05:48 2026**. Retrying with
[self-grading-gap-arxiv.zip](../release/self-grading-gap-arxiv.zip), which adds
`00README.json` explicitly selecting `main.tex` and `pdflatex`, produced the same
errors. Both archives contain the complete reviewed source.

Inspection of the authenticated upload page found individual extracted files,
including `main.tex`. The page's detected top-level list contained `main.tex`, but
the DOM contained no `fieldset.top-level-tex .tex-dropdown` selection controls.
The live Check Files JavaScript derives the submitted `topLevelFiles[]` values
from those controls, so the normal request omitted the selected top-level file.
This was a UI defect; it was not evidence that `main.tex` was absent from the archive.

Restoring a visible `main.tex` selection and invoking the normal Check Files
handler removed the explicit missing-files error. A generic server exception
persisted, including at **Sun Sep 13 18:25:55 2026**. Thus the missing control
explains the initial validation failure, but does not establish the cause of the
remaining server exception. No source-file, local-style, or tar-format defect has
been demonstrated.

## Fresh draft: live preflight and compilation passed

Draft **8074393** received `/private/tmp/arxiv-reviewed-source-only.zip`, containing
the **14 exact reviewed source files**, without either `00README.json` or an
ordinary README. The normal interface reached **Review Files**, selected
`main.tex` and `pdflatex`, and reported empty issue lists for the dependency tree.
No DOM repairs were needed on this record.

Live arXiv compilation then produced a 23-page PDF with TeX Live 2025. A downloaded
local copy is `/private/tmp/arxiv-8074393-compiled.pdf`. Inspection confirmed that
all 23 pages are portrait with no rotation, both detailed diagrams are upright
and unclipped, all six figures and seven tables are present, and all 39 references
render without unresolved citation markers. Compilation success is separate from
final submission: metadata saving subsequently displayed
“Do not make duplicate submissions of the same article.” and identified **7939730**.

The fresh-record success does not isolate whether omitting configuration,
changing record state, or another difference affected the original error. It
does show that arXiv can process the reviewed manuscript and its bundled styles.

## Attempt to preserve and update the original record

The author preferred updating **7939730** if possible. Its Start page displayed
an on-hold classification notice but exposed enabled archive and subject controls
(`disabled=false`, `:disabled=false`, no disabled fieldset). Normal **Continue**
with the existing blank selections returned “You must select an archive” and
“You must select a subject class.” Choosing Computer Science and Artificial
Intelligence through those enabled controls, then clicking **Continue**, produced
another generic arXiv server exception at **Sun Sep 13 18:51:28 2026**. No disabled
control or server restriction was bypassed.

Neither record has been deleted. Removing the fresh draft would not repair this
original-record failure. The prepared support request therefore asks administrators
to repair the original and advise how to reconcile the fresh draft. It has not
been sent. The [status guidance](https://info.arxiv.org/help/submit_status.html)
defines incomplete as not submitted; preserving the old identifier does not prove
that a previous queue position remains.

## Source and packaging verification

The reviewed source also builds independently with Tectonic/XeTeX and with
pdfLaTeX/BibTeX in a separate TeX Live installation. A full run of arXiv's public
[preflight parser](https://github.com/arXiv/submission-tools/blob/d59a60aec535eb36310a8b54cc8bc40ad589eea3/tex2pdf-tools/tex2pdf_tools/preflight/__init__.py)
using actual `texlua`/`kpse` package lookup returned success, `main.tex` as the sole
top-level file, and no source-node or top-level issues for both the reviewed
package and repository revision `f02775d2`. All six current figures were detected.
The earlier revision is not a recovered copy of the originally uploaded archive.

That public-parser run used Debian TeX Live 2022 with the required standard
packages, including `texlive-science`. It did not reproduce arXiv's deployed
services or private plugins. The separate successful live compilation above used
arXiv's TeX Live 2025 environment.

The reproducible [source-only ZIP](../release/self-grading-gap-arxiv-source-only.zip)
has the same member names and source bytes as the uploaded source-only ZIP.
Its fixed timestamps and permissions make the archive bytes differ from the
original upload; even the compressed member payloads match.

| Artifact | SHA-256 |
| --- | --- |
| Uploaded `/private/tmp/arxiv-reviewed-source-only.zip` | `8618ced7b92d1fd48be3925a0a831257a55bb0d1fc9570be83d8ad60cf0e4807` |
| Reproducible `release/self-grading-gap-arxiv-source-only.zip` | `09282b25b5c6b49adeb4d6b29a814c4657df9a1d0dcdef57bd888f76be1c2de8` |

## Reproduction

After rebuilding the manuscript and running `python3 scripts/package_paper.py`,
create the source-only upload package with:

```sh
python3 scripts/package_arxiv_upload.py --without-config
```

The original configuration-bearing ZIP remains reproducible with:

```sh
python3 scripts/package_arxiv_upload.py
```

The script refuses changed source hashes, writes each ZIP and its SHA-256 sidecar,
and checks the member list and every member's bytes. Repeated source-only packaging
produces the same archive bytes in the verified environment. Paper sources are
unchanged by either packaging command.

Both tar.gz and ZIP are supported by arXiv's
[upload workflow](https://info.arxiv.org/help/submit/index.html#upload-and-prepare-your-submission-file).
The optional configuration follows the documented
[compiler/top-level schema](https://info.arxiv.org/help/00README.html).
