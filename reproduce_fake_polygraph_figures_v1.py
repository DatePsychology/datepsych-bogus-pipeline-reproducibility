#!/usr/bin/env python3
"""Reproduce published-summary reconstructions and four companion figures.

This is not an individual-level replication of the studies. CSVs contain
transcribed published, rounded summary statistics. The statistical tests
requiring participant-level data or original adjustment variables CANNOT
be independently refitted from these summaries.

Usage:
    python reproduce_fake_polygraph_figures_v1.py --check
    python reproduce_fake_polygraph_figures_v1.py --output-dir output
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from scipy.stats import f as f_dist, fisher_exact, norm, t as t_dist
from statsmodels.stats.power import TTestIndPower

HERE = Path(__file__).resolve().parent
IVORY = "#f7f4f0"
INK = "#1b2b36"
NAVY = "#162c3c"
TEAL = "#43858e"
TEAL_DARK = "#4a7982"
OCHRE = "#ac8266"
MUTED = "#506372"
GRID = "#d5dddf"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11.5,
    "axes.edgecolor": "#bfcbd0",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.titlesize": 16,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "savefig.facecolor": IVORY,
})


def records(name: str) -> list[dict]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def chart_base(title: str, subtitle: str, *, legend: bool = False):
    """Reserve a non-data area for title/subtitle/legend and a footer."""
    fig, ax = plt.subplots(figsize=(12.6, 6.7), dpi=150)
    fig.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.set_position([0.095, 0.19, 0.855, 0.565 if legend else 0.61])
    fig.text(0.095, 0.935, title, ha="left", va="top", fontsize=18, fontweight="bold", color=INK)
    fig.text(0.095, 0.858, subtitle, ha="left", va="top", fontsize=11.4, color=MUTED)
    ax.grid(axis="y", color=GRID, linewidth=0.9)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_color("#bfccd0")
    ax.tick_params(axis="both", length=0, pad=8)
    return fig, ax


def legend_at_top(fig, handles, labels):
    # Figure-level legend is *outside* the plotting axes, so no gridline can
    # pass through the legend. Do not use a nontransparent masking background.
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.095, 0.813),
               frameon=False, ncol=len(labels), borderaxespad=0,
               handlelength=2.0, columnspacing=1.5, fontsize=11.4)


def save(fig, path: Path):
    fig.savefig(path, dpi=150, facecolor=IVORY)
    plt.close(fig)


def calculate():
    fisher = records("fisher_2013_table4_partner_counts.csv")
    old = records("alexander_fisher_2003_partner_means.csv")
    tour = records("tourangeau_1997_partner_means.csv")
    strang = records("strang_peterson_2020_table3.csv")
    ftests = records("published_f_tests.csv")
    ross = records("ross_2024_victimization_prevalence.csv")
    assert len(fisher) == 4 and len(old) == 6 and len(tour) == 3
    assert len(strang) == 3 and len(ftests) == 5 and len(ross) == 4

    fish = {}
    for row in fisher:
        n = int(row["n"])
        mean = float(row["mean_lifetime_partners"])
        sd = float(row["sd_lifetime_partners"])
        margin = t_dist.ppf(0.975, n - 1) * sd / np.sqrt(n)
        fish[(row["sex"], row["condition"])] = (n, mean, sd, margin)
    mf0 = fish[("Men", "Non-pipeline")][1]
    mf1 = fish[("Men", "Bogus pipeline")][1]
    wf0 = fish[("Women", "Non-pipeline")][1]
    wf1 = fish[("Women", "Bogus pipeline")][1]
    did = (wf1-wf0) - (mf1-mf0)
    did_se = np.sqrt(sum((row[2] ** 2 / row[0]) for row in fish.values()))
    did_p_unadjusted_normal = 2 * norm.sf(abs(did / did_se))

    three_conditions = {(r["sex"], r["condition"]): float(r["mean_reported_partners"]) for r in old}
    early = []
    for r in tour:
        control = float(r["control_mean"])
        pipe = float(r["bogus_pipeline_mean"])
        early.append((r["reference_period"], control, pipe,
                      pipe - control, 100 * (pipe / control - 1)))

    st = []
    for row in strang:
        yes0, n0 = int(row["standard_yes"]), int(row["standard_total"])
        yes1, n1 = int(row["pipeline_yes"]), int(row["pipeline_total"])
        _, exact_p = fisher_exact([[yes0, n0-yes0], [yes1, n1-yes1]], alternative="two-sided")
        # Use the conventional effect direction: odds under pipeline / odds under standard.
        odds_ratio = (yes1 * (n0-yes0)) / ((n1-yes1) * yes0)
        risk_ratio = (yes1 / n1) / (yes0 / n0)
        st.append((row["measure"], 100*yes0/n0, 100*yes1/n1, odds_ratio, risk_ratio, exact_p))

    checks = [(r["study"], r["contrast"], float(r["F"]),
               f_dist.sf(float(r["F"]), int(r["df1"]), int(r["df2"])),
               r["published_p_display"]) for r in ftests]

    powmodel = TTestIndPower()
    power = {n: float(powmodel.power(effect_size=0.25, nobs1=n, alpha=0.05,
                                     ratio=1, alternative="two-sided")) for n in (25, 80, 253)}
    needed = float(powmodel.solve_power(effect_size=0.25, alpha=0.05,
                                        power=0.80, ratio=1, alternative="two-sided"))

    # These assertions check the formulas and transcribed numbers most relevant
    # to the critique; they are NOT evidence of source-data independence.
    assert abs(did - 1.54) < 1e-10
    assert abs(st[0][3] - 6.5185185185) < 1e-8
    assert abs(st[0][4] - 4.4252873563) < 0.01
    assert 0.13 < power[25] < 0.15
    assert 0.34 < power[80] < 0.36
    assert power[253] >= 0.80 and powmodel.power(0.25, 252, alpha=.05) < .80
    assert 252 < needed < 253
    assert abs(checks[1][3] - .03339) < .0001
    assert abs(checks[2][3] - .00889) < .0001
    return dict(fish=fish, did=did, did_se=did_se, did_unadjusted_p=did_p_unadjusted_normal,
                old=three_conditions, early=early, strang=st, ftests=checks,
                power=power, min_n=needed, ross=ross)


def plot_fisher(data, out):
    fig, ax = chart_base("Opposite changes under the bogus pipeline",
                         "Fisher (2013): mean lifetime partners; whiskers show approximate unadjusted 95% CIs",
                         legend=True)
    x = np.array([0, 1])
    offset = dict(Men=-.008, Women=.008)
    for sex, color in (("Men", NAVY), ("Women", TEAL)):
        vals = [data["fish"][(sex, cond)] for cond in ("Non-pipeline", "Bogus pipeline")]
        y = [v[1] for v in vals]
        er = [v[3] for v in vals]
        xx = x + offset[sex]
        ax.errorbar(xx, y, yerr=er, fmt="o-", capsize=5, capthick=1.7,
                    elinewidth=1.6, lw=2.4, markersize=8, color=color, zorder=5)
        if sex == "Men":
            label_xy = [(-28, 16), (14, -2)]
        else:
            label_xy = [(14, -20), (14, 4)]
        for xc, yc, off in zip(xx, y, label_xy):
            ax.annotate(f"{yc:.2f}", (xc, yc), xytext=off, textcoords="offset points",
                        ha="left", va="center", color=color, weight="bold", fontsize=11,
                        annotation_clip=False)
    ax.set_xlim(-.25, 1.28)
    ax.set_ylim(0, 5.35)
    ax.set_xticks(x, ["Non-pipeline", "Bogus pipeline"])
    ax.set_ylabel("Reported partners")
    legend_at_top(fig, [plt.Line2D([0],[0],color=NAVY,marker="o",lw=2),
                        plt.Line2D([0],[0],color=TEAL,marker="o",lw=2)], ["Men", "Women"])
    fig.text(.50,.07,"Sex × condition interaction: F(1, 284) = 4.57, p = .033 (published adjusted model)",
             ha="center", color=MUTED, fontsize=10.7)
    save(fig, out / "figure_01_fisher_2013.png")


def plot_tourangeau(data, out):
    fig, ax = chart_base("An earlier bogus-pipeline partner-count experiment",
                         "Tourangeau, Smith & Rasinski (1997): unadjusted group means; no individual-level data",
                         legend=True)
    vals = data["early"]
    centers = np.arange(3)
    width=.29
    for j,(key,color,label) in enumerate(((1,NAVY,"Control"),(2,TEAL,"Bogus pipeline"))):
        ys = [r[key] for r in vals]
        bars = ax.bar(centers + (j-.5)*width, ys, width=width, color=color, zorder=3)
        for bar,v in zip(bars,ys):
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+.13,f"{v:.2f}",
                    ha="center",va="bottom",fontsize=11,weight="bold")
    ax.set_ylim(0,16)
    ax.set_xticks(centers,["Past year","Past five years","Lifetime"])
    ax.set_ylabel("Mean reported partners")
    legend_at_top(fig,[Patch(facecolor=NAVY),Patch(facecolor=TEAL)],["Control","Bogus pipeline"])
    fig.text(.50,.07,"Significance depended on transformation and adjustment; no established sex-specific interaction.",
             ha="center",color=MUTED,fontsize=10.4)
    save(fig, out / "figure_02_tourangeau_1997.png")


def plot_strang(data, out):
    fig, ax = chart_base("A strong effect on one measure—not every measure",
                         "Strang & Peterson (2020), n = 93 men: percentages endorsing specified tactics",
                         legend=True)
    labels=["SES-LFP\nassault tactics","SSS\nassault tactics","SSS\nverbal coercion"]
    centers=np.arange(3)
    width=.29
    for j,(idx,color) in enumerate(((1,NAVY),(2,TEAL))):
        vals = [r[idx] for r in data["strang"]]
        bars = ax.bar(centers+(j-.5)*width,vals,width=width,color=color,zorder=3)
        for bar,v in zip(bars,vals):
            ax.text(bar.get_x()+bar.get_width()/2, v+.9,f"{v:.1f}%",
                    ha="center",va="bottom",fontsize=10.2,weight="bold")
    ax.set_xticks(centers,labels)
    ax.set_ylim(0,78)
    ax.set_ylabel("Participants endorsing each tactic (%)")
    ax.set_yticks([0,20,40,60], ["0%","20%","40%","60%"])
    for x,(_,_,_,_,_,p) in zip(centers,data["strang"]):
        ax.text(x,73,"p = " + ("1.00" if p > .999 else f"{p:.3f}".lstrip("0")),
                ha="center",va="center",fontsize=10.5,color=MUTED)
    legend_at_top(fig,[Patch(facecolor=NAVY),Patch(facecolor=TEAL)],
                  ["Standard, n = 35","Pipeline, n = 58"])
    fig.text(.5,.055,"The reported ≈6.5× refers to odds for SES-LFP assault tactics, not a risk ratio.",
             ha="center",color=MUTED,fontsize=10.3)
    save(fig, out / "figure_03_strang_peterson_2020.png")


def plot_power(data, out):
    fig, ax=chart_base("Why a null result can be inconclusive",
                        "Illustrative two-sided independent-groups t-test; d = 0.25, α = .05, equal group sizes")
    model=TTestIndPower()
    xx=np.arange(15,291)
    yy=np.array([model.power(effect_size=.25,nobs1=float(n),alpha=.05,ratio=1,
                             alternative="two-sided")*100 for n in xx])
    ax.plot(xx,yy,color=NAVY,lw=3.2,zorder=2)
    ax.axhline(80,ls="--",lw=1.8,color=TEAL_DARK,alpha=.88,zorder=1)
    ax.set_xlim(0,300)
    ax.set_ylim(0,105)
    ax.set_yticks([0,20,40,60,80,100],["0%","20%","40%","60%","80%","100%"])
    ax.set_xlabel("Participants per group (illustrative model)")
    ax.set_ylabel("Probability of detecting this effect")
    # Text is wholly in empty space.  Thin leader lines terminate before the
    # labels; neither the curve nor the dashed reference is hidden or masked.
    for n in (25,80,253):
        y=data["power"][n]*100
        ax.scatter(n,y,s=100,zorder=5,color=OCHRE)
        if n==25: text_y=28; align="bottom"
        elif n==80: text_y=48; align="bottom"
        else: text_y=64; align="top"
        ax.annotate(f"n = {n}\n{y:.0f}% power",xy=(n,y),xytext=(n,text_y),
                    textcoords="data",ha="center",va=align,color=NAVY,
                    fontsize=10.4,fontweight="bold",
                    arrowprops=dict(arrowstyle="-",lw=1.1,color=OCHRE,
                                    shrinkA=6,shrinkB=6,connectionstyle="arc3,rad=0"))
    ax.text(262,88.7,"80% target",color=TEAL_DARK,fontsize=11.2,ha="left",va="bottom")
    save(fig,out / "figure_04_illustrative_power.png")


def format_results(d):
    lines = [
        "BOGUS-PIPELINE RECONSTRUCTION CHECKS — v1",
        "Based on rounded published summaries; not on participant-level data.",
        "",
        "ALEXANDER & FISHER (2003): PUBLISHED PARTNER-COUNT MEANS",
    ]
    for sex in ("Men","Women"):
        lines.append(f"  {sex}: exposure threat={d['old'][(sex,'Exposure threat')]:.1f}; "
                     f"anonymous={d['old'][(sex,'Anonymous')]:.1f}; "
                     f"pipeline={d['old'][(sex,'Bogus pipeline')]:.1f}")
    lines += ["  The paper's partner-count F<1 null result cannot be re-fitted from means alone.","",
              "FISHER (2013): TABLE 4 MEANS AND APPROXIMATE *UNADJUSTED* t INTERVALS"]
    for sex in ("Men","Women"):
        for c in ("Non-pipeline","Bogus pipeline"):
            n,m,sd,e=d["fish"][(sex,c)]
            lines.append(f"  {sex:5s} {c:14s} n={n:2d} mean={m:.2f} SD={sd:.2f} "
                         f"approx. 95% CI=[{m-e:.3f}, {m+e:.3f}]")
    lines += [f"  Women change: +0.65; men change: -0.89; difference-in-differences: {d['did']:.2f}",
              f"  Heuristic unadjusted independence/normal test of DID: SE={d['did_se']:.3f}, "
              f"approx. two-sided p={d['did_unadjusted_p']:.4f} (NOT the paper's adjusted model)","",
              "CHECKS OF THE PUBLISHED F STATISTICS (distribution tails only)"]
    for study,label,val,p,pub in d["ftests"]:
        lines.append(f"  {study} | {label} | F={val:.2f} | recomputed p={p:.6f} | reported {pub}")
    lines += ["  The underlying adjusted ANOVAs cannot be re-fitted without original records.","",
              "TOURANGEAU ET AL. (1997): PUBLISHED RAW PARTNER-COUNT MEANS"]
    for label,c,p,diff,pct in d["early"]:
        lines.append(f"  {label:16s} control={c:.2f}, pipeline={p:.2f}, "
                     f"difference=+{diff:.2f}, ratio increase=+{pct:.1f}%")
    lines += ["  Published transformed/adjusted results are different from tests on raw plotted means.","",
              "STRANG & PETERSON: RECONSTRUCTED 2 x 2 COMPARISONS"]
    for label,p0,p1,orr,rr,p in d["strang"]:
        lines.append(f"  {label}: standard={p0:.1f}%, pipeline={p1:.1f}%, "
                     f"odds ratio={orr:.4f}, risk ratio={rr:.4f}, "
                     f"two-sided Fisher exact p={p:.6f}")
    lines += ["", "ROSS ET AL. (2024): DESCRIPTIVE REPORTED PREVALENCE CHANGES"]
    for sex in ("Men","Women"):
        group=[r for r in d["ross"] if r["sex"]==sex]
        values=[int(r["prevalence_percent"]) for r in group]
        lines.append(f"  {sex}: T1={values[0]}%, T2={values[1]}%, change={values[1]-values[0]:+d} pp")
    lines += ["  The time, laboratory, mode and pipeline conditions were confounded.","",
              "HYPOTHETICAL POWER CURVE — TWO-SIDED INDEPENDENT-GROUPS t TEST",
              "  d=0.25, alpha=0.05, equal group sizes; NOT the power of a published factorial model."]
    for n,p in d["power"].items():
        lines.append(f"  n per group={n:3d}: power={100*p:.2f}%")
    lines += [f"  Minimum group n for 80%: ceil({d['min_n']:.4f}) = {int(np.ceil(d['min_n']))}",
              "", "Data provenance and limits: see README.md and FIGURE_AND_CLAIM_MAP.md."]
    return "\n".join(lines) + "\n"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=HERE,
                        help="Directory for generated PNGs and result TXT (default: repository root)")
    parser.add_argument("--check",action="store_true",help="Validate core summaries and thresholds")
    args=parser.parse_args()
    d=calculate()  # includes core assertions on every run
    args.output_dir.mkdir(parents=True,exist_ok=True)
    plot_fisher(d,args.output_dir)
    plot_tourangeau(d,args.output_dir)
    plot_strang(d,args.output_dir)
    plot_power(d,args.output_dir)
    report=format_results(d)
    (args.output_dir/"reconstruction_results_v1.txt").write_text(report,encoding="utf-8")
    print(report)
    if args.check:
        print("PASS: input checks, statistical assertions and output generation completed.")


if __name__ == "__main__":
    main()
