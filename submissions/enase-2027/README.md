# ENASE 2027 preparation

Official requirements checked **2026-09-23**. This folder contains the original template and venue requirements. Eligibility of the existing public arXiv/GitHub version remains **unresolved**; a locally prepared variant is not yet a cleared submission.

The recommended route is a **Regular Paper**, with Area 3 (Systems and Software Quality) as the closest fit: the call explicitly includes software testing and AI for coding/testing. This is our assessment of fit. The conference is **20–22 April 2027 in Rome, Italy**. [Official call](https://enase.scitevents.org/CallforPapers.aspx)

## Dates

| Route | Submission | Notification | Camera-ready and registration |
| --- | --- | --- | --- |
| Regular Paper, first stage | 2026-11-17 | 2027-01-15 | 2027-01-27 |
| Regular / Position Paper, second stage | 2026-12-21 | 2027-02-15 | 2027-03-01 |

All dates use **Anywhere on Earth (AoE)**. The first stage provides an earlier decision. Recheck dates when choosing the submission round. [Official dates](https://enase.scitevents.org/ImportantDates.aspx)

## Submission and final-paper requirements

| Item | Confirmed requirement |
| --- | --- |
| Review file | English PDF; double-blind; at most 9 authors |
| Regular Paper length at submission | 10,000–50,000 non-whitespace characters |
| Position Paper length at submission | 8,000–40,000 non-whitespace characters |
| Counting scope | References, tables, graphs and appendices included |
| Final Regular Paper accepted as Full | 12 pages |
| Final Regular Paper accepted as Short / Position Paper | 8 pages |
| Final overlength allowance | Up to 4 extra pages, with a fee per page |

The character limits govern review submissions; the page limits govern correctly formatted final papers. [Guidelines](https://enase.scitevents.org/Guidelines.aspx), [FAQ §§4.1–4.2](https://enase.scitevents.org/FAQ.aspx)

Remove identifying information from the review PDF, including metadata, acknowledgments and identifying repository links. Cite relevant related work accurately without self-identifying prose. Do not submit substantially overlapping work concurrently to another archival venue. Submission uses PRIMORIS. [Call: Paper Submission](https://enase.scitevents.org/CallforPapers.aspx), [FAQ §3.4](https://enase.scitevents.org/FAQ.aspx)

The official template is recommended for review and mandatory for camera-ready preparation. [Templates](https://enase.scitevents.org/Templates.aspx) Accepted papers require presentation, registration/payment and the camera-ready/copyright materials by the applicable deadline. [Important information](https://enase.scitevents.org/ImportantInformation.aspx)

## Public-preprint eligibility: unresolved

ENASE prohibits public posting of the submitted paper **during review**, from initial submission through announcement of final selection results. Its wording does not explicitly settle an **already-public** arXiv/GitHub version. [Guidelines](https://enase.scitevents.org/Guidelines.aspx)

The FAQ allows some prior non-archival dissemination, while the technical-report exception in the ethical norms describes material with limited availability and no ISBN. Neither explicitly authorizes the existing widely accessible preprint. [FAQ §3.8](https://enase.scitevents.org/FAQ.aspx), [Ethical norms](https://enase.scitevents.org/NormsPlagiarism.aspx), [INSTICC plagiarism policy](https://portal.insticc.org/plagiarism-policy)

Before submitting here, obtain an event-specific ruling on whether the existing public version is eligible, whether it can remain accessible, and what anonymization is expected for the manuscript and artifacts. This is an outstanding policy check, not an instruction to delete or withdraw the public version. No organizer has been contacted as part of this preparation.

## AI-use disclosure

Disclose AI-assisted content with the tool, affected parts and purpose. AI-generated illustrations additionally require the tool and prompt in their captions and clear identification as illustrations. Authors remain responsible for accuracy. [AI policy](https://enase.scitevents.org/AiTools.aspx)

The Guidelines require acknowledgments-based disclosure and citations in sections containing generated text, but also removal of acknowledgments for anonymous review. The AI policy additionally mentions an appropriate paper section. **Placement of an anonymized review-stage disclosure needs clarification**; preserve an accurate disclosure in the working materials meanwhile. [Guidelines](https://enase.scitevents.org/Guidelines.aspx), [AI policy](https://enase.scitevents.org/AiTools.aspx)

## Original template

- [Downloaded ZIP](template/SCITEPRESS_Conference_Latex.zip), retrieved from the [official SCITEPRESS archive](https://www.scitepress.org/documents/SCITEPRESS_Conference_Latex.zip) linked by ENASE.
- [Unmodified example source](template/original/Example.tex) and [upstream example PDF](template/original/Example.pdf).
- [Machine-readable requirements and provenance](venue.json).

Archive SHA-256:

```text
ec6cfaa11962e08d5c6a402124f21c3bca3591397521406ab6d1889398a3807a
```

All 10 extracted files match their ZIP bytes. `Example.tex` uses the bundled `article.cls`, `SCITEPRESS.sty` and `apalike` styles. Preserve filename case: the actual files are `Example.tex` and `SCITEPRESS.sty`, although parts of the upstream instructions use lowercase spellings. The example specifies A4, a two-column body, 10-point body text and a 70–200-word abstract. Keep vendor files unchanged and adapt a separate manuscript copy. The example is camera-ready material and contains sample authors; it is not an anonymized submission wrapper.

For a future variant, load additional packages before `SCITEPRESS`, preserve its dimensions and use its bibliography style. Count the complete rendered document against the submission character limit; PDF text extraction is only an estimate when figures/equations contain non-extractable text. The venue does not specify a counting tool in the pages reviewed. A manuscript build and length check are separate from the integrity checks performed on this template.

## Remaining preparation

1. Resolve prior-preprint eligibility and anonymous AI-disclosure placement.
2. Adapt the reviewed study into the original layout, preserving definitions, uncertainty, oracle limitations and reproducibility details during shortening.
3. Check character count, final-layout page budget, bibliography, figure legibility and anonymous PDF metadata/links.
4. Select one archival submission route and recheck its current rules and deadlines before upload.

This folder preparation did not upload or submit a paper, contact organizers, or alter the canonical manuscript.
