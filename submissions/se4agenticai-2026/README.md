# SE4AgenticAI 2026

[Review PDF](review.pdf): **10 pages**, including references, with four result tables and two figures. It builds in the official IEEE conference class at 10 pt without margin or font compression. The [build report](review-checks.json) records page count, unresolved references, and overflow checks. The [17-page full-length PDF](full-length.pdf) is the unabridged reflow baseline, including appendices, and exceeds the venue limit.

The guide recommends this as the first venue. This is a local author draft; it has not been uploaded or submitted.

Submission preparation on 23 September added an AI-use acknowledgment for manuscript assistance and the documented AI edit to Figure 2, following [IEEE's disclosure policy](https://conferences.ieeeauthorcenter.ieee.org/author-ethics/guidelines-and-policies/submission-policies/). The PDF remains ten pages. The correct [paper form](https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submitform.php?subarea=S59&submittype=&upload_only=0) uses `subarea=S59`; `subarea=ProW` is for proposing a workshop. Author contact details are still needed before the paper can be submitted.

## Confirmed requirements

Checked **23 September 2026** against the [workshop call](https://cs.uwaterloo.ca/~palencar/se4agenticai/) and [Workshop 59 submission portal](https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submit.php?subarea=S59&undisplay_detail=1&wh=/cyberchair/2026/bigdata26/scripts/ws_submit.php).

- Regular paper: **8–10 pages including references**, IEEE two-column conference format.
- Submission: **10 October 2026, 11:59 p.m. Anywhere on Earth (UTC−12)**, confirmed by the portal.
- Notification: **31 October 2026**. Camera-ready: **14 November 2026**.
- IEEE Big Data: **14–17 December 2026**, Phoenix. The exact workshop day and presentation arrangements still need confirmation.
- Upload through the conference's Workshop 59 paper submission route. Confirm the workshop name before entering metadata.

The workshop call does not settle anonymity or appendix allowances. The parent conference's single-blind policy and appendix prohibition are context, not confirmed workshop-specific instructions. This review PDF contains authors and no appendix. Confirm the workshop rules before uploading, together with author details, exact-PDF approval, presenter, and any required AI-use disclosure. The working files do not represent a final submission approval.

## Files

- `main.tex`: IEEE wrapper; title and abstract preserved from the reviewed paper.
- `content.tex`: entry point for shared editorial text; local substitutions can be added here.
- `review.pdf` and `review-checks.json`: shortened local draft and build report.
- `full-length.pdf` and `full-length-checks.json`: unabridged layout diagnostic.
- `venue.json`: dates, requirements, and open items with sources.

From the repository root: `python3 submissions/build.py se4agenticai-2026`. Add `--full` for the unabridged version. See [shared editorial notes](../_shared/README.md) and [template provenance](../_templates/ieee/README.md).
