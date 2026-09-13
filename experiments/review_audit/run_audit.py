"""Post hoc statistical review of existing records; no API calls or code execution.

This analysis was specified after inspecting the published draft and is not a
preregistered experiment. It retains original records, computes separate complete
HumanEval base/plus matrices, and resamples whole problems/packages for uncertainty.
Run from any directory: python3 experiments/review_audit/run_audit.py
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = HERE / "results"
SEED = 20260913
BOOTSTRAPS = 20000
INPUTS = {}


def read(path):
    raw = path.read_bytes()
    INPUTS[str(path.relative_to(REPO))] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def mean(xs):
    return sum(xs) / len(xs)


def exact_p(b, c):
    n = b + c
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(b, c) + 1)) / 2**n)


def interval(xs):
    xs = sorted(x for x in xs if x is not None)
    def quantile(q):
        pos = (len(xs) - 1) * q
        low = int(pos)
        high = min(low + 1, len(xs) - 1)
        return xs[low] + (xs[high] - xs[low]) * (pos - low)
    return [quantile(.025), quantile(.975)]


def matrix(rows, oracle):
    out = dict(TA=0, FA=0, FR=0, TR=0)
    for r in rows:
        out[("T" if r["self"] == r[oracle] else "F") + ("A" if r["self"] else "R")] += 1
    out["oracle_pass"] = out["TA"] + out["FR"]
    out["claims"] = out["TA"] + out["FA"]
    out["conditional_fa"] = out["FA"] / out["claims"] if out["claims"] else None
    return out


def single_function(directory, human):
    cells = {}
    for cdir in sorted(directory.iterdir()):
        if not cdir.is_dir() or cdir.name == "scores":
            continue
        rows = []
        for rd in sorted(cdir.glob("run*")):
            fs = sorted(rd.glob("humaneval_tdd_*p_*.json" if human else "lcb_tdd_*p_*.json"))
            if not fs:
                continue
            records = read(fs[-1])["results"]
            key = f"{cdir.name}__{rd.name}"
            sf = directory / "scores" / (f"samples_{key}_eval_results.json" if human else f"{key}_oracle.json")
            scores = read(sf)["eval" if human else "oracle"]
            for r in records:
                pid = r["problem_id" if human else "question_id"]
                v = scores[str(pid)]
                if isinstance(v, list):
                    assert len(v) == 1
                    v = v[0]
                row = dict(problem=str(pid), run=rd.name, self=bool(r["tdd_success"]))
                if human:
                    row.update(base=v["base_status"] == "pass",
                               plus=v["base_status"] == "pass" and v["plus_status"] == "pass")
                else:
                    row["hidden"] = bool(v["oracle_pass"])
                rows.append(row)
        if rows:
            assert len(rows) == 150, (directory, cdir, len(rows))
            cells[cdir.name] = rows
    oracle_names = ("base", "plus") if human else ("hidden",)
    output = {"cells": {}, "contrasts": {}}
    control = "control_rerun" if "control_rerun" in cells else "control"
    for cell, rows in cells.items():
        output["cells"][cell] = {}
        for oracle in oracle_names:
            runs = [matrix([r for r in rows if r["run"] == run], oracle)
                    for run in sorted({r["run"] for r in rows})]
            pooled = matrix(rows, oracle)
            pooled["per_run_mean"] = {k: mean([r[k] for r in runs]) for k in ("TA", "FA", "FR", "TR", "oracle_pass", "claims")}
            pooled["run_spread"] = {k: max(r[k] for r in runs) - min(r[k] for r in runs)
                                    for k in ("FA", "FR", "oracle_pass")}
            pooled["run_spread"]["verdict_error"] = max(r["FA"] + r["FR"] for r in runs) - min(r["FA"] + r["FR"] for r in runs)
            output["cells"][cell][oracle] = pooled
            if cell == control:
                continue
            ctr = cells[control]
            metrics = {
                "FA": lambda r: r["self"] and not r[oracle],
                "FR": lambda r: not r["self"] and r[oracle],
                "verdict_error": lambda r: r["self"] != r[oracle],
                "oracle_pass": lambda r: r[oracle],
            }
            results = {}
            for metric, fn in metrics.items():
                by = []
                b = c = 0
                for pid in sorted({r["problem"] for r in ctr}):
                    a = [fn(r) for r in ctr if r["problem"] == pid]
                    z = [fn(r) for r in rows if r["problem"] == pid]
                    assert len(a) == len(z) == 5
                    ma, mz = sum(a) > 2, sum(z) > 2
                    b += ma and not mz
                    c += mz and not ma
                    by.append(mean(z) - mean(a))
                # Each problem's five outcomes stay together in a sampled cluster.
                rng = random.Random(SEED)
                boots = [sum(rng.choices(by, k=len(by))) for _ in range(BOOTSTRAPS)]
                results[metric] = {"mean_delta_per_30": sum(by), "majority_control_only": b,
                                   "majority_intervention_only": c, "mcnemar_p": exact_p(b, c),
                                   "problem_bootstrap_delta_ci": interval(boots)}
            output["contrasts"].setdefault(cell, {})[oracle] = results
    return output


def rgr_rows(directory):
    return [read(p) for p in sorted(directory.glob("*/run*/result.json"))]


def summary(rows):
    valid = [r for r in rows if r["oracle"]["valid"]]
    rs = [{"self": bool(r["self_verdict"]), "oracle": r["oracle"]["pass_fraction"] == 1} for r in valid]
    out = matrix(rs, "oracle")
    out.update(total=len(rows), valid=len(valid), invalid=len(rows) - len(valid))
    unknown_claims = sum(not r["oracle"]["valid"] and r["self_verdict"] for r in rows)
    out["invalid_claims"] = unknown_claims
    denominator = out["claims"] + unknown_claims
    out["missing_oracle_bounds"] = ([out["FA"] / denominator, (out["FA"] + unknown_claims) / denominator]
                                    if denominator else None)
    return out


def package_vectors(rows, packages):
    by = defaultdict(list)
    for r in rows:
        by[r["package"]].append(r)
    return [summary(by[p]) for p in packages]


def rgr_analysis(control_rows, cell_rows):
    packages = sorted({r["package"] for r in control_rows} | {r["package"] for r in cell_rows})
    va, vb = package_vectors(control_rows, packages), package_vectors(cell_rows, packages)
    rng = random.Random(SEED)
    rates_a, rates_b, deltas, passes, true_accepts = [], [], [], [], []
    # Cluster bootstrap preserves repeated runs and between-cell package pairing.
    for _ in range(BOOTSTRAPS):
        sample = rng.choices(range(len(packages)), k=len(packages))
        sums = [{k: sum(v[i][k] for i in sample) for k in ("FA", "claims", "oracle_pass", "TA", "total")}
                for v in (va, vb)]
        a, b = sums
        ra = a["FA"] / a["claims"] if a["claims"] else None
        rb = b["FA"] / b["claims"] if b["claims"] else None
        rates_a.append(ra)
        rates_b.append(rb)
        deltas.append(rb - ra if ra is not None and rb is not None else None)
        # Design-denominator yield treats missing oracle outcomes as not established passes.
        passes.append(b["oracle_pass"] / b["total"] - a["oracle_pass"] / a["total"])
        true_accepts.append(b["TA"] / b["total"] - a["TA"] / a["total"])
    a, b = summary(control_rows), summary(cell_rows)
    a["package_bootstrap_fa_ci"] = interval(rates_a)
    b["package_bootstrap_fa_ci"] = interval(rates_b)
    matched_a = {(r["package"], r["run"]): r for r in control_rows if r["oracle"]["valid"]}
    matched_b = {(r["package"], r["run"]): r for r in cell_rows if r["oracle"]["valid"]}
    keys = sorted(matched_a.keys() & matched_b.keys())
    matched = {"n_pairs": len(keys), "control": summary([matched_a[k] for k in keys]),
               "intervention": summary([matched_b[k] for k in keys])}
    return {"control": a, "intervention": b, "paired_valid": matched,
            "conditional_fa_delta": b["conditional_fa"] - a["conditional_fa"],
            "package_bootstrap_fa_delta_ci": interval(deltas),
            "oracle_yield_delta": b["oracle_pass"] / b["total"] - a["oracle_pass"] / a["total"],
            "package_bootstrap_oracle_yield_delta_ci": interval(passes),
            "package_bootstrap_true_accept_yield_delta_ci": interval(true_accepts)}


def fmt_ci(v, scale=1):
    return f"[{scale*v[0]:.1f}, {scale*v[1]:.1f}]"


def main():
    exps = REPO / "experiments"
    analyses = {}
    for name, path, human in [
        ("exp006", exps / "exp006_model_asymmetry/results", True),
        ("exp007", exps / "exp007_lcb_asymmetry/results", False),
        *[(f"exp011_{arm}", exps / f"exp011_verifier_generalization/results/{arm}", arm.startswith("he"))
          for arm in ("he_gemini", "he_claude", "lcb_gemini", "lcb_claude")],
    ]:
        analyses[name] = single_function(path, human)
    control = rgr_rows(exps / "exp010_flagship/results/control")
    rgr = {"tau0.70": rgr_analysis(control, rgr_rows(exps / "exp010_flagship/results/strong_judge"))}
    for tau in ("0.40", "0.50", "0.55", "0.85"):
        rgr[f"tau{tau}"] = rgr_analysis(control, rgr_rows(exps / f"exp013_tau_sweep/results/tau{tau}/strong_judge"))
    calibration = read(exps / "exp010_flagship/calibration/calibration.json")
    usable = [r for r in calibration if not r.get("excluded")]
    failures = sum(r["pass_fraction"] < 1 for r in usable)
    assert failures == 0
    adapter = {"usable": len(usable), "excluded": len(calibration) - len(usable), "observed_failures": failures,
               "one_sided_95_binomial_upper": 1 - .05 ** (1 / len(usable)),
               "caveat": "Illustrative binomial bound only; these selected synthetic packages are not a random sample of generated candidates."}
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, check=True,
                           capture_output=True, text=True).stdout.strip()
    report = {"status": "post hoc review; not preregistered", "seed": SEED, "bootstrap_replicates": BOOTSTRAPS,
              "generated_at_utc": datetime.now(timezone.utc).isoformat(), "working_tree_dirty": bool(dirty),
              "source_revision": sha, "python": platform.python_version(), "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "input_sha256": INPUTS, "single_function": analyses, "rgrbench": rgr, "adapter_calibration": adapter}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "audit.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    lines = ["# Post hoc statistical review (generated; do not hand-edit)", "",
             "No new model calls. Original results are preserved. This supplementary analysis is not preregistered.",
             f"Bootstrap: {BOOTSTRAPS:,} replicates, seed {SEED}; whole problems/packages retain all repeated runs.",
             "Intervals characterize resampling of the selected tasks, not representative benchmark sampling.", "",
             "## Complete matrices: per-run means on each oracle", "",
             "| Experiment | Cell | Oracle | Pass | TA | FA | FR | TR | Conditional FA |",
             "|---|---|---|---:|---:|---:|---:|---:|---:|"]
    for exp, analysis in analyses.items():
        for cell, oracles in analysis["cells"].items():
            for oracle, d in oracles.items():
                m = d["per_run_mean"]
                lines.append(f"| {exp} | {cell} | {oracle} | " + " | ".join(f"{m[k]:.1f}" for k in ("oracle_pass", "TA", "FA", "FR", "TR")) + f" | {100*d['conditional_fa']:.1f}% |")
    lines += ["", "## Original majority-outcome tests, completed for all outcomes", "",
              "These p-values are unadjusted. Majority-of-five and mean-per-run changes are different estimands.",
              "The original runners tested only FA and pass, omitting FR and total-error p-values.", "",
              "| Experiment | Cell | Oracle | Outcome | Δ per 30 | McNemar p | Problem bootstrap Δ CI |",
              "|---|---|---|---|---:|---:|---:|"]
    for exp, analysis in analyses.items():
        for cell, oracles in analysis["contrasts"].items():
            for oracle, metrics in oracles.items():
                for key, d in metrics.items():
                    lines.append(f"| {exp} | {cell} | {oracle} | {key} | {d['mean_delta_per_30']:+.1f} | {d['mcnemar_p']:.5f} | {fmt_ci(d['problem_bootstrap_delta_ci'])} |")
    lines += ["", "## RGRBench: package-cluster uncertainty and missing-oracle bounds", "",
              "Δ = strong minus control conditional FA, in percentage points. Each bootstrap samples the same",
              "package IDs for both cells and retains all runs, allowing different accepted sets in each cell.",
              "This is an operating-policy comparison, not a judge discrimination test on fixed candidates.", "",
              "| Strong threshold | Control FA% [cluster CI] | Strong FA% [cluster CI] | Δ FA pp [cluster CI] | Strong missing-oracle bounds |",
              "|---|---:|---:|---:|---:|"]
    for tau, d in rgr.items():
        a, b = d["control"], d["intervention"]
        lines.append(f"| {tau} | {100*a['conditional_fa']:.1f} {fmt_ci(a['package_bootstrap_fa_ci'],100)} | {100*b['conditional_fa']:.1f} {fmt_ci(b['package_bootstrap_fa_ci'],100)} | {100*d['conditional_fa_delta']:+.1f} {fmt_ci(d['package_bootstrap_fa_delta_ci'],100)} | {fmt_ci(b['missing_oracle_bounds'],100)} |")
    lines += ["", f"Control missing-oracle bounds: {fmt_ci(rgr['tau0.70']['control']['missing_oracle_bounds'],100)}%.",
              "Bounds classify all claimed successes with missing oracle verdicts as correct or incorrect;",
              "they do not repair possible oracle/specification disagreement or adapter errors in valid cases.", "",
              "## Adapter calibration", "",
              f"Observed failures: {failures}/{len(usable)} usable cases; {adapter['excluded']} excluded.",
              f"Even under an illustrative IID binomial model, the one-sided 95% upper bound is {100*adapter['one_sided_95_binomial_upper']:.1f}%, not zero.",
              adapter["caveat"], "",
              "## Interpretation limits", "",
              "- Failure to pass a significance/effect-size bar does not demonstrate equivalence or absence of benefit.",
              "- Treat unadjusted p-values as nominal; no familywise correction was preregistered.",
              "- GREEN retry count and difficulty strata are observational subsets; their differences do not establish a causal retry or complexity effect.",
              "- The tau sweep changes RED and GREEN thresholds, and its 0.50 point is an adaptive follow-up.",
              "- New complete HumanEval+ pass/FR matrices correct the original mixture of base pass/FR with plus FA.", ""]
    (OUT / "ANALYSIS.md").write_text("\n".join(lines))
    # Numeric macros are available to the manuscript without manually changing result numbers.
    macros = ["% Generated by experiments/review_audit/run_audit.py; post hoc analysis."]
    labels = {"control_rerun": "Control", "strong_testgen": "Test", "strong_judge": "Judge", "strong_both": "Both"}
    for cell, label in labels.items():
        m = analyses["exp006"]["cells"][cell]["plus"]["per_run_mean"]
        for key, suffix in (("oracle_pass", "Pass"), ("FA", "FA"), ("FR", "FR")):
            macros.append(f"\\newcommand{{\\AuditHE{label}{suffix}}}{{{m[key]:.1f}}}")
    for exp, cell, oracle, name in (("exp006", "control_rerun", "plus", "HEControlGap"),
                                    ("exp007", "control", "hidden", "LCBControlGap"),
                                    ("exp007", "strong_judge", "hidden", "LCBJudgeGap")):
        rate = analyses[exp]["cells"][cell][oracle]["conditional_fa"]
        macros.append(f"\\newcommand{{\\Audit{name}}}{{{100*rate:.1f}}}")
    for tau, label in (("tau0.70", "Shared"), ("tau0.50", "Followup")):
        d = rgr[tau]
        macros.append(f"\\newcommand{{\\AuditRGR{label}Delta}}{{{100*d['conditional_fa_delta']:+.1f}}}")
        macros.append(f"\\newcommand{{\\AuditRGR{label}CI}}{{{fmt_ci(d['package_bootstrap_fa_delta_ci'],100)}}}")
    macro_text = "\n".join(macros) + "\n"
    (OUT / "paper_numbers.tex").write_text(macro_text)
    (REPO / "paper" / "audit_numbers.tex").write_text(macro_text)
    print(f"Generated {OUT / 'audit.json'}, ANALYSIS.md, and paper_numbers.tex")


if __name__ == "__main__":
    main()
