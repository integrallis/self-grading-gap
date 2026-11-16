# Venue variants

Working folders for the plan in [Verification_Gap_Submission_Guide.docx](Verification_Gap_Submission_Guide.docx). Venue requirements were checked on **23 September 2026**. The scientific source remains [paper/main.tex](../paper/main.tex); figures, bibliography, and generated numerical macros are shared. No venue submission has been made by this preparation work.

| Variant | Local deliverable | Next requirement |
| --- | --- | --- |
| [SE4AgenticAI 2026](se4agenticai-2026/) | [10-page review PDF](se4agenticai-2026/review.pdf), IEEE wrapper, build checks, and 17-page unabridged reflow baseline | Author review and remaining workshop upload requirements |
| [VST 2027](vst-2027/) | IEEE wrapper and [10-page working PDF](vst-2027/review.pdf) | Shorten to eight pages before submission |
| [LLM4Code 2027](llm4code-2027/) | Shared editorial text and verified/provisional requirements | Confirm the final 2027 template and paper portal |
| [TrustedSoftwAIr 2027](trustedsoftwair-2027/) | Shared editorial text and venue requirements | Confirm template, anonymity, and archival scope |
| [ENASE 2027](enase-2027/) | Shared editorial text, official SCITEPRESS template, and requirements | Resolve prior-public-preprint eligibility; then prepare its anonymous format and shorter abstract |

The first review PDF retains four result tables, two figures, the existing abstract, and all 39 cited references. It omits appendices and compresses repeated prose and duplicate presentations. See the [editorial notes](_shared/README.md) for the changes. Source tables and numerical values are preserved. The existing long manuscript remains available; the [17-page IEEE baseline](se4agenticai-2026/full-length.pdf) also preserves its appendices.

## Build and edit

Run these from the repository root with Python 3, Tectonic, and Poppler (`pdfinfo`) installed:

```sh
python3 submissions/build.py se4agenticai-2026
python3 submissions/build.py se4agenticai-2026 --full
python3 submissions/build.py vst-2027
```

The first Tectonic build may need network access to fetch its TeX resources. The IEEE template is vendored with [provenance](_templates/ieee/README.md). Each build stages its dependencies under the venue's ignored `build/` folder and writes a PDF and `*-checks.json` beside the wrapper. Check reports record the page limit and any unresolved references or overflowing boxes; compilation alone does not establish submission readiness.

Each venue has a `content.tex` entry point. The IEEE wrappers currently use the same shortened manuscript; edit a venue entry point to introduce a local variant without changing another venue. Templates for the two ICSE workshops are deliberately pending their confirmed 2027 instructions. ENASE's template files are preserved unchanged under its own folder.

The shared editorial sections are maintained by hand. `python3 submissions/prepare.py` extracts the original abstract, unabridged body, and appendices and refreshes the source-hash manifest. **It does not reconcile changes into the shortened manuscript.** If the canonical paper changes, inspect that change and update the shortened sections as needed before refreshing the manifest. Builds reject a changed canonical source until its recorded hashes are refreshed.

## Submission sequence

The guide's plan is one active peer-review submission at a time:

1. SE4AgenticAI: internal upload target **8 October**, official deadline **10 October 2026, 11:59 p.m. AoE**, decision **31 October**.
2. If rejected, choose one ICSE workshop: **13 November 2026 AoE**, decision **11 December**.
3. If rejected again and eligible, ENASE's second round: **21 December 2026 AoE**.

VST is an alternative first choice: mandatory abstract **19 October**, paper **23 October 2026 AoE**. Its paper deadline precedes SE4AgenticAI's decision, and its **8 December** decision follows the ICSE deadlines. It does not fit between those stages.

Dates and unresolved policies are documented with official source links in each venue folder. The Workshop 59 portal confirms SE4AgenticAI's AoE cutoff, resolving the guide's timezone question. No other unresolved item is silently treated as settled. Before uploading, confirm current author information, exact-PDF author approval, presenter, venue-specific anonymity, and any required disclosures. Current PDFs contain the author block from the reviewed manuscript and are local author drafts.
