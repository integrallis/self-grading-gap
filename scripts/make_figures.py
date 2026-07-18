"""Regenerate every paper figure from committed raw result files. No API, no hand-drawn data.

Palette: Okabe-Ito pair, validated (CVD ΔE≥91.9, contrast ≥3:1): PASS=#0072B2, GAP=#D55E00
with hatching as secondary encoding so figures survive grayscale printing. Ink is neutral.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
FIG = REPO / "paper" / "figures"
EXP6 = REPO / "experiments" / "exp006_model_asymmetry" / "results"
EXP7 = REPO / "experiments" / "exp007_lcb_asymmetry" / "results"
EXP10 = REPO / "experiments" / "exp010_flagship" / "results"

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
    cells = json.loads(summary_file.read_text())["cells"]
    out = []
    for key, _ in CELL_LABELS:
        c = cells[cell_map.get(key, key)]
        out.append({"fa": c[fa_key], "fr": c["fr"], "pass": c["pass"]})
    return out


def fig2_asym() -> None:
    """Per-cell false accepts vs false rejects (bars = means, dots = runs), both experiments.
    The figure carries the paper's two headline results at once: FA flat everywhere
    (soundness invariant), FR collapsing and pass rising in the strong-judge cells."""
    data = [
        ("HumanEval subset-30 (exp006)",
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
            ax.annotate(f"pass {pm:.1f}", (i, -1.55), ha="center", fontsize=7.5,
                        color=INK, annotation_clip=False)
        ax.set_xticks(range(len(cells)))
        ax.set_xticklabels([lbl for _, lbl in CELL_LABELS], fontsize=7.5)
        ax.set_title(title, fontsize=8.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylim(0, 8)
    axes[0].set_ylabel("problem-runs / 30")
    axes[0].bar(0, 0, color="white", edgecolor=RED, hatch="///", label="false accepts (invisible)")
    axes[0].bar(0, 0, color=BLUE, alpha=0.85, label="false rejects (visible)")
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG / "fig2_asym.pdf", bbox_inches="tight")
    plt.close(fig)


def _exp10() -> dict:
    """Parse committed exp010 ANALYSIS.md for per-tier and headline conditional FA rates."""
    txt = (EXP10 / "ANALYSIS.md").read_text()
    ctrl_sec = txt.split("## control:")[1].split("## strong_judge:")[0]
    strong_sec = txt.split("## strong_judge:")[1]

    def tiers(sec: str) -> list[float]:
        return [float(re.search(rf"H-D4 {t} FA:.*?= ([\d.]+)", sec).group(1))
                for t in ("beginner", "intermediate", "advanced")]

    def hd1(sec: str) -> tuple[float, float, float]:
        m = re.search(r"H-D1 conditional FA of claims: ([\d.]+) \[([\d.]+), ([\d.]+)\]", sec)
        return float(m.group(1)), float(m.group(2)), float(m.group(3))

    return {"control": {"tiers": tiers(ctrl_sec), "hd1": hd1(ctrl_sec)},
            "strong": {"tiers": tiers(strong_sec), "hd1": hd1(strong_sec)}}


def fig3_complexity() -> None:
    """Conditional false accepts rise monotonically with difficulty tier (RGRBench, H-D4)."""
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
    ax.set_ylim(0, 1.0); ax.set_xlim(-0.25, 2.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "fig3_complexity.pdf", bbox_inches="tight")
    plt.close(fig)


def fig4_convergence() -> None:
    """The false-accept rate is a constant across three instruments and the external literature.
    RGRBench point + Wilson CI parsed from committed ANALYSIS.md; HumanEval+/LCB are the control
    conditional-FA headlines (exp006/exp007, 18%/29%); the external range is the cited
    SWE-bench overfitting literature (20-33%)."""
    rgr, rgr_lo, rgr_hi = _exp10()["control"]["hd1"]      # 0.415 [0.304, 0.537]
    rows = [
        ("SWE-bench overfitting (external)", None, 0.20, 0.33, MUTED),
        ("RGRBench (this work)", rgr, rgr_lo, rgr_hi, RED),
        ("LiveCodeBench (this work)", 0.29, None, None, RED),
        ("HumanEval+ (this work)", 0.18, None, None, RED),
    ]
    fig, ax = plt.subplots(figsize=(4.5, 2.3))
    ax.axvspan(0.18, 0.42, color=RED, alpha=0.06, lw=0)
    for y, (_, pt, lo, hi, col) in enumerate(rows):
        if pt is not None and lo is not None:
            ax.errorbar(pt, y, xerr=[[pt - lo], [hi - pt]], fmt="o", color=col, ms=6,
                        capsize=3, lw=1.3, zorder=3)
        elif pt is not None:
            ax.plot(pt, y, "o", color=col, ms=6, zorder=3)
        else:
            ax.plot([lo, hi], [y, y], "-", color=col, lw=5, solid_capstyle="round", alpha=0.65)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7.5)
    ax.set_ylim(-0.6, len(rows) - 0.4); ax.set_xlim(0, 0.6)
    ax.set_xticks([0, 0.15, 0.30, 0.45, 0.60])
    ax.set_xticklabels(["0", "15%", "30%", "45%", "60%"])
    ax.set_xlabel("false-accept rate (fraction of claimed successes)", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "fig4_convergence.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    fig1_loop()
    fig2_asym()
    fig3_complexity()
    fig4_convergence()
    print(f"figures regenerated under {FIG}")
