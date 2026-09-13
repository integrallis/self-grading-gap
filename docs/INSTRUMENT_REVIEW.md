# Instrument and reproducibility review

Review date: 2026-09-13. Scope: the public manuscript, pipeline source, experiment runners,
registration/deviation records, and released artifacts. No new model calls or oracle runs
were made for this review. Statistical reanalysis is documented separately in
`experiments/review_audit/`. References below describe the historical instrument; changing
it now would define a new experiment, not repair its old measurements.

## Findings requiring changes to interpretation

### 1. The recorded self-verdict includes judge rejection and abandonment

**Priority: high.** `run_flagship.py:134` records `bool(result.get("success"))`, as do the
single-function runners through `tdd_success`. The graph can terminate unsuccessfully at
the RED or GREEN judge gate without executing a final test suite
(`src/vgap/pipeline/subgraph.py:467`, `:483`, `:505`, `:521`). Success requires a passing
VERIFY execution; failure does not imply that an execution rejected the implementation.
The general definition already allows internal quality gates, but prose describing every
self-verdict as an executed final-test outcome, or every false reject as bad tests
rejecting correct code, overstates what was measured.

**Repair:** define the endpoint as pipeline acceptance, including all gates. State that
positive verdicts require successful execution and negative verdicts include judge
rejection, exhausted retries, and failure to produce an implementation. Separate
abandonment, true accepts, and oracle passes when discussing completeness. Do not
retroactively replace the stored endpoint with an unrecorded final pytest result.

### 2. The null concerns a particular judge contract

**Priority: high.** The GREEN judge receives a task title, generated tests, and generated
code, but not the full specification
(`src/vgap/pipeline/templates/judge/code_against_tests.j2`). Its system prompt explicitly
restricts the rating to predicted test outcomes (`coordinator.py:142`). Even hardcoding is
flagged without changing the outcome-based rating. The RED reviewer does see the full
specification, but its rubric permits one wrong assertion or invented constraint at the
default acceptance threshold: the specified deduction leaves a score at that threshold
(`templates/judge/test_quality.j2`, scoring section).

**Repair:** scope generalization to this instrument and these role prompts. A separate
final reviewer that checks implementation against the original specification is an
unmeasured comparison. The experiment supports a warning about this test-centered loop;
it cannot establish that every stronger verifier, prompt, or independent verification
strategy fails to reduce false accepts.

### 3. Adapter calibration is a limited stress test, not a zero error bound

**Priority: high.** The calibration chooses the first alphabetically sorted packages in
each tier (`calibrate_adapter.py:113`), merges reference source, and renames public
top-level symbols. It excludes packages for which its deterministic adaptation fails
before evaluating the model adapter (`:152`). The surviving fixtures keep reference
behavior and much of their internal API structure; they do not reproduce arbitrary
generated implementations with incompatible constructors, data representations, omitted
methods, or differing exception contracts.

`experiments/exp010_flagship/calibration/calibration.json` contains the complete fixture
outcomes, including exclusions. Zero observed errors among eligible fixtures is not an
upper bound of zero. Moreover, the runner's `adapter_error` is one minus the fraction of
tests passed (`:187`), while the study's false-accept endpoint is whether any oracle test
fails. These quantities cannot simply be subtracted from one another as the calibration
docstring proposes.

**Repair:** report zero observed errors in the eligible calibration fixtures, disclose the
selection/exclusions, and retain adapter mismatch as a construct limitation. Distinguish
mutation kill rate from a statistical error rate of the oracle: mutation adequacy does not
measure the probability that a benchmark requirement or expected output is wrong. A
future validation would manually adjudicate representative generated-candidate failures
under a frozen, blinded protocol and estimate error on the same binary endpoint.

### 4. Reconstructed history does not independently establish preregistration

**Priority: high.** `PROVENANCE.md` states that historical run SHAs identify a private
working history and that release history was linearized. The exp006/007 plan's recorded
SHA, `f0411e0bced918e1f329798187261dfdcc03b8f1`, is not present in this public checkout
(`git cat-file -t` cannot resolve it). The public introduction of exp010's README and
results is the same commit (`c4627ac2`), rather than a publicly inspectable registration
commit before collection. These facts are consistent with private prior registration;
they do not establish its timing to an independent reader.

**Repair:** describe registrations as the authors' retained design records, identify
which original history is unavailable publicly, and avoid claiming that the public Git
graph proves the original ordering. Publish the original relevant commits or an
independently timestamped registration archive if available. Do not reconstruct or
backdate new evidence to fill this gap.

### 5. Cross-provider collection used outcome-dependent run replacement

**Priority: high.** `experiments/exp011_verifier_generalization/DEVIATIONS.md` documents
deleted and repeated partial runs, an initially stricter nonempty-implementation
threshold, and a later relaxed threshold. The original registration instead says
terminal API errors count as failed problem-runs. Nonempty implementation count can
reflect a scientific outcome, including RED-gate abandonment, as well as an outage.
Calling all of these changes operational and asserting that scientific selection was
unchanged is too strong without the discarded records.

**Repair:** disclose the selection change and missing attempts in the manuscript. If
recoverable, release every replaced attempt plus provider-error classifications, frozen
inclusion decisions, and token costs; then run an inclusion sensitivity analysis. Until
then, scope inference to retained runs and state that the effect of replacement cannot
be fully audited. Do not infer from this concern that the retained outcomes are invented.

## Implementation details that should be reported accurately

### 6. Same-model escalation changes sampling temperature in single-function runs

**Priority: medium.** HumanEval and LiveCodeBench construct a separate escalation client
at temperature 1.0 (`humaneval_runner.py:229`, `lcb_runner_local.py:166`). Pinning its model
name to the generator disables a model upgrade, but is not an identity operation: the
normal generator uses temperature 0.7. The subgraph switches clients at the escalation
attempt threshold or after repeated execution-gate failures (`subgraph.py:195`). In
contrast, the RGRBench runners pass the original generator object as the escalation
client, retaining temperature 0.7.

**Repair:** disclose this historical retry schedule and distinguish it from a model
upgrade. A future correction should be versioned and preregistered; silently changing the
historical instrument would hide the configuration that produced the data. Usage logs
record model names, but not enough request parameters to independently verify temperature
on each historical call.

### 7. Shared configuration and timeout descriptions hide harness differences

**Priority: medium.** The self-test executor uses a 30-second subprocess timeout
(`pytest_runner.py`). The HumanEval in-run diagnostic uses 120 seconds, but final paper
scoring goes through EvalPlus, whose settings are separate. The LiveCodeBench scorer
explicitly passes `timeout=6` to `codegen_metrics`
(`experiments/exp007_lcb_asymmetry/score_lcb.py:44`). RGRBench adapter authoring sets
`max_tokens=4096` (`run_flagship.py:212`), even though pipeline-generation calls leave it
unset. A single universal oracle-timeout or token-limit statement is inaccurate.

**Repair:** name the applicable harness and stage for each setting. Do not interpret
the in-run `humaneval_passed` flag as the independent final score: failed pipeline runs
are assigned false in that diagnostic, whereas the separate EvalPlus stage scores their
retained implementations too (`humaneval_runner.py:166`; `run_asym.py:151`).

### 8. Artifact coverage supports reanalysis more strongly than exact replay

**Priority: medium.** HumanEval/LCB summary provenance stores the Git SHA and Python
version, but not all dependency versions, input hashes, or resolved provider snapshots
(`humaneval_runner.py:307`, `lcb_runner_local.py:230`). The usage logger stores the request
model alias rather than a complete provider response and request configuration
(`instrumentation.py:46`). RGRBench result rows retain the package's source-provenance
label, verdicts, attempts, and oracle summary, but not per-run source hashes, timestamps,
prompt transcripts, judge feedback, or final pytest output (`run_flagship.py:233`). Its
plan references the dataset and instrument commits globally. The runner does not set a
per-problem `MAESTRO_PROMPT_LOG_DIR`, unlike the single-function runners.

The LiveCodeBench scorer loads a named release, not a committed dataset snapshot or
pinned harness revision. Its output records the input path but not an input-content hash.
The lockfile supports an installable released environment; it cannot establish that each
historical run used those exact dependency versions. `PRE_REGISTRATION.md` for exp011
mentions VCR, but this public repository has no VCR implementation or cassette archive.

**Repair:** distinguish released raw outcome reanalysis, stored-score reanalysis, new
oracle execution, and fresh model replication. Publish available historical manifests,
traces, provider snapshots, and dataset/harness revisions. Mark unavailable fields as
unknown rather than inventing them. Future runners should persist these fields at run
time, before interpreting results.

### 9. Cost telemetry has limits beyond successful retained calls

**Priority: medium.** `UsageLogger` logs successful completions only; it does not record
failed attempts or provider billing evidence. The budget readers treat unpriced calls as
zero and check the cap between complete problem-runs, not before every potentially
billable call. Thus a strict total-spend hard cap is not guaranteed. RGRBench also uses
the strong model for offline adapter grading in both cells, with the same tag as pipeline
calls, so its logged study spend is not purely deployable pipeline cost.

**Repair:** label costs as retained successful-call estimates and explain whether offline
grading is included. Do not claim invoice-complete cost or a strict per-call cap. The
released main-study usage logs inspected in this review did have numeric prices, so the
unpriced-call branch is a future-run robustness issue rather than evidence of missing
prices in these retained data.

## Reproduction repair made during this review

The original `reproduce.sh` regenerated only exp006 and exp007, although the manuscript
also used exp010, exp011, and exp013. Its final line asserted analyses matched the
committed files without making that comparison, and pipelines into `tail` could hide
upstream failures.

The updated script uses the frozen lockfile, propagates pipeline errors, runs the
instrument and existing asymmetry-analysis tests, regenerates the later analyses and
review audit, then regenerates figures. README now distinguishes these offline stages
from fresh paid generation or independent oracle replay. The copied exp013 analyzer is
repaired separately to report thresholds individually instead of pooling all threshold
directories. Raw experimental outcomes are retained unchanged.

Remaining empirical gaps above require additional evidence or newly designed experiments;
documentation and reanalysis alone cannot close them.

## Verification record

`uv sync --frozen` installed the released dependency lock successfully. The instrument
tests and existing exp006 helper tests passed (`38 passed`); `bash -n reproduce.sh` and
`git diff --check` also passed. Every exp006, exp007, exp010, exp011, and exp013 analysis
stage completed without model access using that environment. The statistical review and
figure generation were verified separately by the corresponding review tasks.

Regeneration preserved outcome counts and historical contrasts. It corrected stale cost
headers: exp010's archived zero-spend header was replaced by the total from its retained
usage logs, and the earlier exp011 analyses now show the final global exp011 spend rather
than totals from intermediate collection dates. Asymmetry analyses also update their
generation timestamps and current-checkout SHAs. The corrected exp013 analysis reproduced
without further drift. These are generated-report changes, not edits to raw outcomes.

An attempt to execute the complete shell script in the restricted sandbox stopped at uv's
external cache permissions; its requested escalation was interrupted. Accordingly, this
review records separate successful stage checks, not a completed end-to-end shell run in
that sandbox.
