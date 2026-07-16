# Defect register

The pipeline under study is a reviewed recreation of a 2025 system from earlier, informal
experiments. The recreation was performed line-by-line, and every defect found is recorded
here with a stable identifier. The paper's appendix summarizes this register; identifiers
are referenced from the paper and must stay stable.

- **Class H (harness)** — defects outside the studied mechanism (result accounting, crashes,
  logging, environment coupling).
- **Class B (behavioral)** — defects inside the studied mechanism (prompt rendering, judge
  scoring/parsing, retry logic, code extraction).
- **Disposition** — how the study instrument treats the finding. All are resolved in the
  instrument that produced the paper's results; none is merely documented.
- B-9 was never assigned; IDs are kept stable.

## Findings

| ID | Class | Finding (in the 2025 original) | Disposition in the study instrument |
|----|-------|-------------------------------|-------------------------------------|
| H-1 | H | Invoked bare `pytest` from PATH — which pytest ran depended on the caller's environment and was never recorded. | Pinned to `sys.executable -m pytest`; interpreter+pytest versions recorded in run provenance. |
| H-2 | H | Module-level `from git import Repo` forced GitPython into every import though only the git-enabled path uses it. | Lazy import inside the function. |
| H-3 | H | Import-time side effect: truncated and appended a FileHandler to a /tmp debug log. | Removed. |
| H-4 | H | Every GREEN generation dumped prompt+response to /tmp/rag_analysis. | Removed (per-run instrumented logging replaces it). |
| H-5 | H | Prompt config mapped ~40 agents; only the TDD path's are live. | Config trimmed to the live path. |
| H-6 | H | `evaluate_functional_correctness` imported but never used; scoring was a bare in-process `exec`. | Dead import removed; see H-12 for the oracle. |
| H-7 | H | Problems loaded via `human_eval.data.read_problems`. | Loaded via EvalPlus's mirror of the identical original dataset (one fewer dependency). |
| H-8 | H | Live network GET to toptal.com for `.gitignore` on every bootstrap (5 s timeout, static fallback). | Static placeholder; the pipeline never touches the network. |
| H-9 | H | GREEN responses were never logged (RED's were) — original artifacts lack GREEN outputs. | GREEN responses logged. |
| H-10 | H | Per-attempt JSON dumps to /tmp/prompt_logs. | Removed. |
| H-11 | H | Bootstrap Jinja-rendered a docker-compose.yml (execution-inert in the workspace). | Static placeholder, execution-inert. |
| H-12 | H | The in-run oracle ran untrusted solution code with a bare in-process `exec` and no timeout — a pathological solution hung the whole run. | Oracle runs in a subprocess with a 120 s timeout; identical pass/fail semantics for anything that terminates. |
| H-13 | H | No per-call cost or provenance instrumentation. | Per-call usage/cost logging with problem/cell/run tags; per-run machine-readable summaries with provenance fields. |
| H-14 | H | Every `.content` read assumed `str`; providers that return content as a block list crashed the run. | `content_to_text` normalization at all read sites (identity for `str`). |
| H-15 | H | (Found in this study's own instrumentation.) Registering a usage logger per run stacked callbacks; later runs' rows landed in the first run's log. | Registration retargets a per-process singleton; rows carry per-call tags. |
| B-1 | B | A template render exception silently became a `None` prompt upstream. | A render failure raises RuntimeError — a broken template is an instrument error, not an empty prompt. |
| B-2 | B | The 30 s pytest timeout raised `TimeoutExpired` uncaught — a hanging generated test aborted the whole problem run. | A timeout scores as a failed test run (TIMEOUT marker in the output). |
| B-3 | B | Judge pass/fail verdicts via substring scans of the whole response ("fail" present and "pass" absent anywhere) — mostly dead branch in practice. | Verdicts derive from the parsed score against the configured threshold. |
| B-4 | B | First-match score regex; `>1.0 → ÷10 → clamp` normalization mapped "Score: 85" to a perfect 1.0; unparseable → 0.0. | Last occurrence of the highest-priority pattern; (1,10] read as 0–10, (10,100] as 0–100; unparseable stays fail-closed 0.0. |
| B-5 | B | GREEN judge verdict threshold hardcoded at 0.7, ignoring configuration. | Verdict uses the configured judge threshold. |
| B-6 | B | Two result classes with different validation semantics across judges. | Single `EvaluationResult` class everywhere. |
| B-7 | B | Latent `NameError` in the RED retry fallback (referenced an undefined name; unreachable in practice). | Fallback uses the content the response dict carries. |
| B-8 | B | GREEN's execution gate ran only the current test file while VERIFY ran the whole suite. | The gate runs the whole suite, matching VERIFY. |
| B-10 | B | The failure-analysis judge was asked for corrected implementation code that was never written to disk — it traveled only as prompt text. | Mechanism removed: the failure analyst produces analysis and fix directives only, never code; the generator writes all code. |
| E-1 | — | (Extension, not a defect.) RED called the generator agent directly, leaving no seam for a separate test-author model. | RED routes through a test agent: identity when no test model is configured; the model-asymmetry knob when one is. |

## Excluded couplings

The recreation excludes machinery that is inert on the studied path, verified by closure
trace: the legacy coordinator monolith the subgraph replaces, multi-task state, pattern
analyzer, complexity router, LibCST manipulation, VCR/Redis caching, requirements agents,
MCP tooling, and RAG wiring. Nothing on the RED-GREEN-VERIFY path consults any of them.
