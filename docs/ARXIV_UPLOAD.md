# arXiv upload troubleshooting

On September 13, 2026, the author reported that uploading
`self-grading-gap-reviewed-source.tar.gz` and clicking **Check Files** produced
“Error: Missing files or top-level files.” The accompanying server error gave
the timestamp **Sun Sep 13 18:05:48 2026**. The original submission had not shown
this error. The server-side cause has not been established.

The reviewed archive contains `main.tex` at its root, including an ordinary
`\documentclass{article}` directive, together with all referenced figures,
generated numerical macros, local styles, and `main.bbl`. Its extracted source
builds independently with Tectonic. That does not test arXiv's upload service.

## Prepared workaround

Use [self-grading-gap-arxiv.zip](../release/self-grading-gap-arxiv.zip).
The ZIP contains the same 14 source files, verified against the reviewed manifest,
plus `00README.json`, which explicitly selects `main.tex` and `pdflatex`.
It omits the ordinary archive README. The paper and reviewed PDF are unchanged.

1. Return to **Prepare Files / Return to Upload Step** within existing submission
   **7939730**.
2. Replace the uploaded file set using **Delete All on the file-upload page**.
   Keep the submission itself.
3. Choose the ZIP above and click **Upload**. Wait for the extracted-file list;
   confirm that it includes `main.tex`, `audit_numbers.tex`, and `main.bbl`.
4. Click **Check Files**. If the selection controls appear, verify that the
   top-level file is `main.tex` and the processor is `pdflatex`.
5. Continue to compilation and review arXiv's resulting PDF before finalizing.
   The local reviewed PDF uses Tectonic/XeTeX; arXiv's rendering must be checked.

These steps follow arXiv's [upload workflow](https://info.arxiv.org/help/submit/index.html#upload-and-prepare-your-submission-file)
and [explicit compiler/top-level configuration](https://info.arxiv.org/help/00README.html).
Both tar.gz and ZIP are supported; no tar-format defect has been demonstrated.
The ZIP is a diagnostic workaround, not a confirmed repair of the remote failure.

If the same error recurs, report it through [arXiv support](https://info.arxiv.org/help/contact.html),
including submission ID, the exact error and timestamp above, the uploaded filename,
the Check Files action, and whether `main.tex` appeared in the extracted-file list.
Do not delete or recreate the held submission. No support message has been sent here.

## Reproduction

After rebuilding the manuscript and running `python3 scripts/package_paper.py`, run:

```sh
python3 scripts/package_arxiv_upload.py
```

The script refuses changed source hashes, writes the ZIP and its SHA-256 sidecar,
and checks every ZIP member against its source bytes.
