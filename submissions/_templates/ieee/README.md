# IEEE conference template and verified venue requirements

Verified September 23, 2026. The venue wrappers and manuscript content live
outside this directory.

## Template provenance

`IEEEtran.cls` (v1.8b, August 26, 2015), `IEEEtran.bst`, and `bare_conf.tex` are
unchanged upstream files extracted from the
[CTAN IEEEtran distribution](https://mirrors.ctan.org/macros/latex/contrib/IEEEtran.zip).
The [package record](https://www.ctan.org/pkg/ieeetran) and
[maintainer's website](https://www.michaelshell.org/tex/ieeetran/) identify 1.8b as
the current reference release. The original class and bibliography README files
are retained, including their credits; the source headers retain the LPPL notices.
`provenance.json` records the download URL, archive hash, upstream member names,
and hashes of all five retained upstream files.

Both venues link the [IEEE conference template page](https://www.ieee.org/conferences/publishing/templates).
The [IEEE CAI template page](https://cai.ieee.org/2025/manuscript-templates-for-conference-proceedings/)
links both IEEE's conference ZIP and CTAN documentation. The IEEE-hosted ZIP
returned an empty response in this environment, so the upstream CTAN release was
used. This is not a claim that its bytes match the IEEE-hosted 2024 ZIP.

The intended wrapper declaration is:

```tex
\documentclass[10pt,conference]{IEEEtran}
```

Use the standard numeric `IEEEtran` bibliography style. Do not modify the vendored
class to fit the page limit. `bare_conf.tex` is upstream reference material, not a
venue submission manuscript.

## SE4AgenticAI 2026

| Requirement | Verified value |
| --- | --- |
| Regular paper | 8–10 pages, references included |
| Short paper | 3–4 pages, references included |
| Format | IEEE conference, two columns |
| Submission | October 10, 2026, 11:59 p.m. Anywhere on Earth |
| Notification | October 31, 2026 |
| Camera-ready | November 14, 2026 |
| Conference/workshop window | December 14–17, 2026; specific workshop date not posted |
| Portal | CyberChair, Workshop 59 / `S59` |

Sources: [workshop CFP](https://cs.uwaterloo.ca/~palencar/se4agenticai/) and
[Workshop 59 submission instructions](https://wi-lab.com/cyberchair/2026/bigdata26/scripts/submit.php?subarea=S59&undisplay_detail=1&wh=/cyberchair/2026/bigdata26/scripts/ws_submit.php).
The portal supplies the deadline timezone omitted by the CFP.

The workshop CFP and portal do not explicitly specify anonymity. The
[Big Data main-track CFP](https://bigdataieee.org/BigData2026/calls/papers/) states
single-blind review and disallows appendices, but neither rule is explicitly
repeated for this workshop. Do not report their workshop applicability as
confirmed. The workshop's page cap includes references and provides no separate
extra-page allowance for appendices.

## VST 2027

| Requirement | Verified value |
| --- | --- |
| Full paper | At most 8 pages, including text, references, appendices, and figures |
| Position/tool paper | 2–4 pages |
| Format | IEEE proceedings; 24pt title, 10pt text; `[10pt,conference]{IEEEtran}`; no `compsoc` or `compsocconf` |
| Mandatory abstract | October 19, 2026, AoE |
| Paper | October 23, 2026, AoE |
| Notification | December 8, 2026, AoE |
| Camera-ready | January 8, 2027, AoE |
| Workshop | March 9, 2027, Richmond, Virginia, with SANER |
| Submission | English PDF through [VST's dedicated EasyChair portal](https://easychair.org/conferences/?conf=vst2027) |

Source: [VST 2027 CFP and instructions](https://vstworkshop.github.io/vst2027/).
The page requires original work not already accepted or concurrently under
review elsewhere; it references IEEE authorship and conference GenAI policies.
It does not explicitly specify an anonymity rule. The
[text CFP](https://vstworkshop.github.io/vst2027/vst2027-cfp.txt) also requires an
author to attend and present an accepted paper, and states that papers enter
SANER's companion proceedings.

The linked EasyChair sign-in page reported new submissions closed when checked,
despite the future CFP deadline. Recheck portal availability before submission;
the text CFP still lists the submission link as TBD, while the HTML page links
the dedicated portal.

## Scheduling consequence

SE4AgenticAI's October 31 notification follows VST's October 23 paper deadline.
The two variants are preparation alternatives: the dates do not support a normal
SE4AgenticAI decision followed by a VST submission in this cycle, and VST explicitly
prohibits concurrent review elsewhere.
