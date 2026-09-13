# arXiv upload troubleshooting

## Current status: submission 8074393 confirmed; processing

On September 13, 2026, arXiv confirmed **“Article submitted”** and redirected to the
user dashboard. Its row for **submit/8074393** shows **processing**, with no
expiration date. Submission is complete; moderation and public announcement are
not yet confirmed. The final preview showed **CC BY 4.0**, primary **cs.AI**, and
cross-lists **cs.LG** and **cs.SE**, with the full 244-word abstract and comments
reporting 23 pages, 6 figures, and 7 tables. The
[submission receipt](../release/arxiv-submission.json) records the verified outcome
and artifact checksums.

On September 13, 2026, fresh draft **8074393** passed arXiv's live preflight and
compiled successfully with **pdfLaTeX / TeX Live 2025**, producing a **23-page PDF**.
Saving its metadata initially produced a duplicate-submission block referring to
**7939730**. After attempts to update the original record failed, the author
authorized proceeding with the new submission and declined a repair request.
The normal Delete action removed **7939730**; arXiv confirmed “Submission deleted,”
and the dashboard then listed only **8074393**. Metadata saving then succeeded,
allowing final preview and the confirmed submission above. No former queue
position is claimed.

The [support draft](ARXIV_SUPPORT_REQUEST.txt) is retained as an **unsent historical
record** and is **not to be sent**, per the author's instruction. The troubleshooting
details below describe earlier attempts, not the current existence of both records.

## Historical original-record errors

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

Live arXiv compilation then produced a 23-page PDF with TeX Live 2025. The actual
download is preserved as [self-grading-gap-arxiv-compiled.pdf](../release/self-grading-gap-arxiv-compiled.pdf),
with a [SHA-256 sidecar](../release/self-grading-gap-arxiv-compiled.pdf.sha256).
This is arXiv's pdfLaTeX output, separate from the locally built Tectonic/XeTeX
[reviewed PDF](../release/self-grading-gap-reviewed.pdf). The preserved file is
byte-identical to `/private/tmp/arxiv-8074393-compiled.pdf` (1,948,665 bytes), with
SHA-256 `47cd2628753b55931e0ef6af84eb4081137d10ad68cbfe84b76cd370ee6c8362`.
Inspection confirmed that
all 23 pages are portrait with no rotation, both detailed diagrams are upright
and unclipped, all six figures and seven tables are present, and all 39 references
render without unresolved citation markers. Compilation success is separate from
final submission: metadata saving subsequently displayed
“Do not make duplicate submissions of the same article.” and identified **7939730**.

The fresh-record success does not isolate whether omitting configuration,
changing record state, or another difference affected the original error. It
does show that arXiv can process the reviewed manuscript and its bundled styles.

## Historical attempt to preserve and update the original record

The author preferred updating **7939730** if possible. Its Start page displayed
an on-hold classification notice but exposed enabled archive and subject controls
(`disabled=false`, `:disabled=false`, no disabled fieldset). Normal **Continue**
with the existing blank selections returned “You must select an archive” and
“You must select a subject class.” Choosing Computer Science and Artificial
Intelligence through those enabled controls, then clicking **Continue**, produced
another generic arXiv server exception at **Sun Sep 13 18:51:28 2026**. No disabled
control or server restriction was bypassed.

At that stage, both records were incomplete. The author subsequently chose the
new-record route, and **7939730** was deleted as recorded above. The original server
failure was not repaired. The [status guidance](https://info.arxiv.org/help/submit_status.html)
defines incomplete as not submitted; keeping an old identifier would not by itself
establish that a previous queue position remained.

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

[manifest.json](../release/manifest.json) preserves the source hashes and the
packaging-time provenance of the local reviewed release. Its original “not
uploaded” status and old submission ID describe that earlier build, not the
current submission. [arxiv-submission.json](../release/arxiv-submission.json)
records the subsequent confirmed arXiv submission separately.

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
