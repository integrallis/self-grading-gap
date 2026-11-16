# VST 2027

The [working PDF](review.pdf) currently has **10 pages** in the required IEEE format. Its [build report](review-checks.json) flags that it exceeds the **eight-page limit**. It shares the SE4AgenticAI editorial text and needs further local shortening; it is not ready to upload.

This is an alternative first venue in the guide. VST's paper deadline precedes SE4AgenticAI's decision, so the two are not a sequential fallback pair. No abstract or paper has been registered.

## Confirmed requirements

Checked **23 September 2026** against the [official VST 2027 call](https://vstworkshop.github.io/vst2027/).

- Research paper: at most **eight pages including references, figures, and appendices**.
- Use `IEEEtran` with `10pt,conference`. The call explicitly excludes `compsoc` and `compsocconf`.
- Mandatory abstract: **19 October 2026 AoE**. Paper: **23 October 2026 AoE**.
- Notification: **8 December 2026**. Final copy: **8 January 2027**.
- Workshop: **9 March 2027**, Richmond, Virginia, with SANER.
- Portal: [VST 2027 EasyChair](https://easychair.org/conferences/?conf=vst2027). It reported submissions closed when checked; recheck when registering.
- Concurrent review elsewhere is prohibited.

The inspected call does not explicitly specify anonymity. Confirm it in the live instructions before uploading. The current local draft includes authors; exact-PDF approval, current author information, presenter, and any required disclosures remain to be completed.

## Editing and build

`main.tex` supplies the venue wrapper; `content.tex` selects the shared editorial manuscript. Introduce VST-specific cuts through this entry point so the 10-page SE4AgenticAI draft remains intact. Preserve the primary matrices, diagnostic example, uncertainty, abandonment accounting, and oracle qualifications when shortening.

Run `python3 submissions/build.py vst-2027` from the repository root. This generates `review.pdf` and `review-checks.json`; a successful compile can still exceed the page limit. Venue facts and open items are recorded in [venue.json](venue.json).
