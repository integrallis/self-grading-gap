"""Regenerate paper figures from recorded outcomes and the post hoc statistical audit.

No API calls. Schematics describe the instrument; numeric plots read recorded data.
The Okabe-Ito palette and secondary marker/hatch encoding aid grayscale reading.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

# Use the bundled DejaVu fonts requested below, avoiding host-specific font scans.
os.environ.setdefault("MPL_IGNORE_SYSTEM_FONTS", "1")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
FIG = REPO / "paper" / "figures"
EXP6 = REPO / "experiments" / "exp006_model_asymmetry" / "results"
EXP7 = REPO / "experiments" / "exp007_lcb_asymmetry" / "results"
EXP10 = REPO / "experiments" / "exp010_flagship" / "results"
EXP = REPO / "experiments"
AUDIT = EXP / "review_audit" / "results" / "audit.json"

BLUE = "#0072B2"   # pass / false rejects (visible failure)
RED = "#D55E00"    # false accepts (invisible failure; always hatched for grayscale)
INK = "#333333"
MUTED = "#777777"

plt.rcParams.update({
    "font.size": 9, "font.family": "DejaVu Sans", "axes.edgecolor": MUTED,
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": MUTED,
    "ytick.color": MUTED, "figure.dpi": 150,
})


def fig1_loop() -> None:
    """Schematic: the self-verification loop with the oracle outside it."""
    fig, ax = plt.subplots(figsize=(6.0, 2.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.6); ax.axis("off")

    def box(x, y, w, h, label, fc="white", ec=INK, style="round,pad=0.06"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=1.0))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=8)

    def arrow(x1, y1, x2, y2, **kw):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=9, lw=1.0, color=kw.get("color", INK),
                                     linestyle=kw.get("ls", "-")))

    # pipeline boundary
    ax.add_patch(FancyBboxPatch((0.25, 0.7), 8.2, 3.5, boxstyle="round,pad=0.1",
                                fc="none", ec=MUTED, lw=0.8, linestyle=(0, (4, 3))))
    ax.text(0.45, 4.05, "pipeline (grades itself)", fontsize=7.5, color=MUTED)

    box(0.6, 2.6, 1.5, 0.9, "spec")
    box(2.7, 2.6, 1.7, 0.9, "RED\nwrite tests $T$")
    box(5.0, 2.6, 1.7, 0.9, "GREEN\nwrite code $y$")
    box(5.0, 1.0, 1.7, 0.9, "judges +\nexec gate")
    box(7.1, 2.6, 1.2, 0.9, "run $T(y)$")
    arrow(2.1, 3.05, 2.7, 3.05)
    arrow(4.4, 3.05, 5.0, 3.05)
    arrow(6.7, 3.05, 7.1, 3.05)
    arrow(5.85, 2.6, 5.85, 1.9)            # green <-> gates
    arrow(5.0, 1.45, 3.55, 2.6)            # retry feedback to RED/GREEN
    ax.text(3.9, 1.5, "retries /\nfeedback", fontsize=7, color=MUTED, ha="center")

    box(8.9, 2.6, 1.6, 0.9, "self-verdict\n$s_i$", ec=BLUE)
    arrow(8.3, 3.05, 8.9, 3.05)

    box(8.9, 0.6, 1.6, 0.9, "oracle\n$o_i$", ec=RED)
    arrow(6.7, 2.75, 8.9, 1.1, ls=(0, (2, 2)), color=MUTED)
    ax.text(8.15, 2.15, "$y$ (never $T$)", fontsize=7, color=MUTED, ha="center")

    ax.annotate("verification gap:  $s_i{=}1 \\wedge o_i{=}0$",
                xy=(10.5, 0.1), fontsize=8.5, color=RED, ha="right")
    fig.savefig(FIG / "fig1_loop.pdf", bbox_inches="tight")
    plt.close(fig)


CELL_LABELS = [("control", "control\n(W everywhere)"), ("strong_testgen", "S authors\ntests"),
               ("strong_judge", "S judges"), ("strong_both", "S authors\n+ judges")]


def _cells(summary_file: Path, fa_key: str, cell_map: dict[str, str]) -> list[dict]:
    """Use complete HumanEval+ matrices; original summaries mix base and plus."""
    human = fa_key == "fa_plus"
    directory = summary_file.parent
    audit = json.loads(AUDIT.read_text())["single_function"]["exp006" if human else "exp007"]
    out = []
    for key, _ in CELL_LABELS:
        cell = cell_map.get(key, key)
        arrays = {"fa": [], "fr": [], "pass": []}
        for rd in sorted((directory / cell).glob("run*")):
            pattern = "humaneval_tdd_*p_*.json" if human else "lcb_tdd_*p_*.json"
            files = sorted(rd.glob(pattern))
            if not files:
                continue
            records = json.loads(files[-1].read_text())["results"]
            score_name = (f"samples_{cell}__{rd.name}_eval_results.json" if human
                          else f"{cell}__{rd.name}_oracle.json")
            scores = json.loads((directory / "scores" / score_name).read_text())["eval" if human else "oracle"]
            fas = frs = passes = 0
            for r in records:
                pid = r["problem_id" if human else "question_id"]
                v = scores[str(pid)]
                if human:
                    v = v[0] if isinstance(v, list) else v
                    oracle = v["base_status"] == "pass" and v["plus_status"] == "pass"
                else:
                    oracle = bool(v["oracle_pass"])
                fas += r["tdd_success"] and not oracle
                frs += not r["tdd_success"] and oracle
                passes += oracle
            arrays["fa"].append(fas)
            arrays["fr"].append(frs)
            arrays["pass"].append(passes)
        expected = audit["cells"][cell]["plus" if human else "hidden"]["per_run_mean"]
        for key, canonical in (("fa", "FA"), ("fr", "FR"), ("pass", "oracle_pass")):
            assert sum(arrays[key]) / len(arrays[key]) == expected[canonical]
        out.append(arrays)
    return out


def fig2_asym() -> None:
    """Per-cell oracle-relative errors: bars are means; dots are individual runs."""
    data = [
        ("HumanEval+ subset-30 (exp006)",
         _cells(EXP6 / "asym_summary.json", "fa_plus", {"control": "control_rerun"})),
        ("LiveCodeBench lcb30, post-cutoff (exp007)",
         _cells(EXP7 / "asym_summary.json", "fa", {})),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 2.9), sharey=True)
    w = 0.34
    for ax, (title, cells) in zip(axes, data):
        for i, c in enumerate(cells):
            fam = sum(c["fa"]) / len(c["fa"])
            frm = sum(c["fr"]) / len(c["fr"])
            ax.bar(i - w / 2, fam, w, color="white", edgecolor=RED, hatch="///", lw=1.2)
            ax.bar(i + w / 2, frm, w, color=BLUE, alpha=0.85)
            ax.scatter([i - w / 2] * len(c["fa"]), c["fa"], s=8, color=RED, zorder=3)
            ax.scatter([i + w / 2] * len(c["fr"]), c["fr"], s=8, color=BLUE, zorder=3,
                       edgecolor="white", lw=0.4)
            pm = sum(c["pass"]) / len(c["pass"])
            ax.annotate(f"pass {pm:.1f}", (i, -2.0), ha="center", fontsize=7.5,
                        color=INK, annotation_clip=False)
        ax.set_xticks(range(len(cells)))
        ax.set_xticklabels([lbl for _, lbl in CELL_LABELS], fontsize=7.5)
        ax.set_title(title, fontsize=8.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylim(0, 8)
    axes[0].set_ylabel("problem-runs / 30")
    axes[0].bar(0, 0, color="white", edgecolor=RED, hatch="///", label="false accepts")
    axes[0].bar(0, 0, color=BLUE, alpha=0.85, label="false rejects")
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_asym.pdf", bbox_inches="tight")
    plt.close(fig)


def _exp10() -> dict:
    """Read exact tier numerators and denominators from raw package-run records."""
    result = {}
    for label, cell in (("control", "control"), ("strong", "strong_judge")):
        rows = [json.loads(p.read_text()) for p in sorted((EXP10 / cell).glob("*/run*/result.json"))]
        claims = [r for r in rows if r["oracle"]["valid"] and r["self_verdict"]]
        counts = []
        for tier in ("beginner", "intermediate", "advanced"):
            subset = [r for r in claims if r["tier"] == tier]
            counts.append((sum(r["oracle"]["pass_fraction"] < 1 for r in subset), len(subset)))
        result[label] = {"counts": counts, "tiers": [k / n for k, n in counts]}
    return result


def fig3_complexity() -> None:
    """Descriptive tier associations with claim counts, including sparse strata."""
    d = _exp10()
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = [0, 1, 2]
    ax.plot(x, d["control"]["tiers"], "-o", color=RED, lw=1.8, ms=6,
            label="control (weak everywhere)")
    ax.plot(x, d["strong"]["tiers"], "--s", color=INK, lw=1.3, ms=5, mfc="white",
            label="strong judge")
    ax.set_xticks(x); ax.set_xticklabels(["beginner", "intermediate", "advanced"], fontsize=8)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
    ax.set_ylabel("false accepts / claimed successes", fontsize=8)
    for label, offset, color in (("control", 9, RED), ("strong", -15, INK)):
        for i, ((k, n), value) in enumerate(zip(d[label]["counts"], d[label]["tiers"])):
            dy = (-15 if label == "control" else 9) if i == 0 else offset
            ax.annotate(f"{k}/{n}", (i, value), xytext=(0, dy),
                        textcoords="offset points", ha="center", fontsize=7, color=color)
    ax.set_ylim(0, 1.05); ax.set_xlim(-0.25, 2.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_complexity.pdf", bbox_inches="tight")
    plt.close(fig)


def fig4_convergence() -> None:
    """Show study-specific claim-error rates; do not pool incompatible external endpoints."""
    audit = json.loads(AUDIT.read_text())
    rgr = audit["rgrbench"]["tau0.70"]["control"]
    he = audit["single_function"]["exp006"]["cells"]["control_rerun"]["plus"]
    lcb = audit["single_function"]["exp007"]["cells"]["control"]["hidden"]
    rows = [
        (f"RGRBench ({rgr['FA']}/{rgr['claims']})", rgr["conditional_fa"], *rgr["package_bootstrap_fa_ci"], RED),
        (f"LiveCodeBench ({lcb['FA']}/{lcb['claims']})", lcb["conditional_fa"], None, None, RED),
        (f"HumanEval+ ({he['FA']}/{he['claims']})", he["conditional_fa"], None, None, RED),
    ]
    fig, ax = plt.subplots(figsize=(4.8, 2.1))
    for y, (_, pt, lo, hi, col) in enumerate(rows):
        if pt is not None and lo is not None:
            ax.errorbar(pt, y, xerr=[[pt - lo], [hi - pt]], fmt="o", color=col, ms=6,
                        capsize=3, lw=1.3, zorder=3)
        elif pt is not None:
            ax.plot(pt, y, "o", color=col, ms=6, zorder=3)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5)
    ax.set_ylim(-0.6, len(rows) - 0.4); ax.set_xlim(0, 0.6)
    ax.set_xticks([0, 0.15, 0.30, 0.45, 0.60])
    ax.set_xticklabels(["0", "15%", "30%", "45%", "60%"])
    ax.set_xlabel("false-accept rate (fraction of claimed successes)", fontsize=8)
    ax.set_title("All-weak controls on different selected task sets", fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_convergence.pdf", bbox_inches="tight")
    plt.close(fig)


# Read all verifier outcomes from the complete-oracle post hoc audit.
VERIFIER_ARMS = [
    ("HumanEval+", "GPT-5.6 Terra", "exp006", "plus"),
    ("HumanEval+", "Gemini-2.5-Pro", "exp011_he_gemini", "plus"),
    ("HumanEval+", "Claude-4.5-Sonnet", "exp011_he_claude", "plus"),
    ("LiveCodeBench", "GPT-5.6 Terra", "exp007", "hidden"),
    ("LiveCodeBench", "Gemini-2.5-Pro", "exp011_lcb_gemini", "hidden"),
    ("LiveCodeBench", "Claude-4.5-Sonnet", "exp011_lcb_claude", "hidden"),
]


def fig5_verifiers() -> None:
    """Plot observed FA means without equating nonsignificance with a flat response."""
    cells = ["control", "strong_testgen", "strong_judge", "strong_both"]
    xlabels = ["control", "S tests", "S judge", "S both"]
    benches = ["HumanEval+", "LiveCodeBench"]
    style = {"GPT-5.6 Terra": (MUTED, "o", MUTED),
             "Gemini-2.5-Pro": (BLUE, "s", "white"),
             "Claude-4.5-Sonnet": (RED, "^", "white")}
    data: dict = {}
    audit = json.loads(AUDIT.read_text())["single_function"]
    for bench, ver, experiment, oracle in VERIFIER_ARMS:
        data.setdefault(bench, {})[ver] = {
            cell.replace("control_rerun", "control"): v[oracle]["per_run_mean"]["FA"]
            for cell, v in audit[experiment]["cells"].items()}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7), sharey=True)
    for ax, bench in zip(axes, benches):
        for ver, (col, mk, mfc) in style.items():
            ys = [data[bench][ver][c] for c in cells]
            ax.plot(range(4), ys, marker=mk, color=col, lw=1.3, ms=5, mfc=mfc, label=ver)
        ax.set_xticks(range(4))
        ax.set_xticklabels(xlabels, fontsize=8)
        ax.set_title(bench, fontsize=9)
        ax.set_ylim(0, 6)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("false accepts / 30-problem run", fontsize=8)
    axes[1].legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG / "fig5_verifiers.pdf", bbox_inches="tight")
    plt.close(fig)


def fig6_misalignment() -> None:
    """An oracle-relative false accept caused by an unspecified exception contract."""
    run = EXP10 / "strong_judge" / "numbers_to_words" / "run1"
    record = json.loads((run / "result.json").read_text())
    code = (run / "candidate" / "__init__.py").read_text()
    tests = (run / "self_tests.py").read_text()
    assert 'raise Exception("must be in 0..9999")' in code
    assert "pytest.raises(Exception," in tests
    assert record["self_verdict"] and record["oracle"]["valid"]
    oracle = record["oracle"]
    assert oracle["tests_passed"] < oracle["tests_total"]

    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.5)
    ax.axis("off")
    ax.text(.1, 4.25, "A requirements–oracle mismatch: numbers_to_words", fontsize=11,
            weight="bold", va="center")

    for x, title, edge in ((.1, "Supplied requirement", INK),
                            (4.05, "Self-testing pipeline", BLUE),
                            (8.0, "Held-out oracle", RED)):
        ax.add_patch(FancyBboxPatch((x, 1.05), 3.65, 2.75, boxstyle="round,pad=0.05",
                                   facecolor="white", edgecolor=edge, linewidth=1.2))
        ax.text(x + .15, 3.52, title, fontsize=9, weight="bold", color=edge)

    ax.text(.25, 3.12, "Reject out-of-range numbers.", fontsize=9)
    ax.text(.25, 2.72, "Error message includes:", fontsize=9)
    ax.text(.25, 2.34, '"must be in 0..9999"', fontsize=8.6, family="monospace")
    ax.text(.25, 1.68, "Exception type unspecified.", fontsize=9, weight="bold")

    ax.text(4.2, 3.12, "Self-authored test:", fontsize=9)
    ax.text(4.2, 2.77, "pytest.raises(Exception)", fontsize=8.6, family="monospace")
    ax.text(4.2, 2.36, "Generated code:", fontsize=9)
    ax.text(4.2, 2.01, "raise Exception(...)", fontsize=8.6, family="monospace")
    ax.text(4.2, 1.43, "Self-verdict: accept", fontsize=9, weight="bold", color=BLUE)

    ax.text(8.15, 3.12, "Oracle range test:", fontsize=9)
    ax.text(8.15, 2.77, "pytest.raises(ValueError)", fontsize=8.6, family="monospace")
    ax.text(8.15, 2.17, "Adds a specific exception type.", fontsize=9)
    ax.text(8.15, 1.64, f"{oracle['tests_passed']} / {oracle['tests_total']} oracle tests pass",
            fontsize=9, weight="bold", color=RED)
    ax.text(8.15, 1.27, "Oracle-relative false accept", fontsize=8.7, color=RED)

    for start, end in ((3.8, 4.0), (7.75, 7.95)):
        ax.add_patch(FancyArrowPatch((start, 2.8), (end, 2.8), arrowstyle="-|>",
                                     mutation_scale=10, linewidth=1.1, color=MUTED))
    ax.text(.1, .55,
            "The recorded disagreement does not establish that the code violates the supplied requirement.",
            fontsize=9, color=INK)
    fig.savefig(FIG / "fig6_misalignment.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    fig1_loop()
    fig2_asym()
    fig3_complexity()
    fig4_convergence()
    fig5_verifiers()
    fig6_misalignment()
    print(f"figures regenerated under {FIG}")
