# Fake Lie Detectors and Sexual-Partner Counts — Reproducibility Materials

**Code, transcribed published summary statistics, statistical checks, and four figures** accompanying a methodological review of Date Psychology's article [“Did a fake polygraph catch women lying about their sexual partner count?”](https://datepsychology.com/did-a-fake-polygraph-catch-women-lying-about-their-sexual-partner-count/).

The [companion methodological review](https://datepsych.substack.com/p/can-a-fake-lie-detector-reveal-the/) examines what the bogus-pipeline experiments do—and do not—establish about sexual-history reporting. **This is a reproducibility package for the review's published-summary reconstructions, not a replication of the original studies using individual participant records.** Original microdata, analysis scripts, and verified partner histories were not available. Calculations from reported rounded figures cannot reproduce the source authors' full adjusted models.

> **Name clarification:** “Date Psychology” refers to the author/website being reviewed. **Michele G. Alexander** is a different person: she coauthored the 2003 experiment with Terri D. Fisher.

## Contents

| File | Purpose |
|---|---|
| `reproduce_fake_polygraph_figures_v1.py` | Standalone Python script that reads all six CSV inputs, reconstructs the numerical checks, and regenerates the four figures and results file. |
| `alexander_fisher_2003_partner_means.csv` | Published partner-count means for men and women under exposure threat, anonymous, and bogus-pipeline conditions. |
| `fisher_2013_table4_partner_counts.csv` | Fisher (2013), Table 4: cell sizes, means, and SDs for lifetime partner counts. |
| `tourangeau_1997_partner_means.csv` | Partner-count group means for the past year, past five years, and lifetime. |
| `strang_peterson_2020_table3.csv` | Endorsement numerators and denominators for three sexual-aggression measures; allows exact 2×2 checks. |
| `published_f_tests.csv` | Five F statistics, degrees of freedom, and published p values for Fisher (2013) and Tourangeau et al. (1997). |
| `ross_2024_victimization_prevalence.csv` | Descriptive Time 1 / Time 2 victimization prevalence reported for men and women. |
| `reconstruction_results_v1.txt` | Reference console output of the published-summary calculations. |
| `figure_01_fisher_2013.png` | Four group means with approximate *unadjusted* 95% intervals and the *reported adjusted* interaction test. |
| `figure_02_tourangeau_1997.png` | Three sets of published control/pipeline mean counts. |
| `figure_03_strang_peterson_2020.png` | Contrasting endorsement results across three measures. |
| `figure_04_illustrative_power.png` | Explicitly hypothetical two-sample power curve for *d*=0.25. |
| `FIGURE_AND_CLAIM_MAP.md` | Exact figure-to-source map, calculation formulas, inferential limitations, and original-source links. |
| `requirements.txt` | Python dependency requirements. |
| `LICENSE` | MIT license for original code and generated chart artwork; not a license for third-party research papers. |

## Reproduce everything

Use **Python 3.10+** in a working copy of this repository:

```bash
python -m pip install -r requirements.txt
python reproduce_fake_polygraph_figures_v1.py --check
```

The script reads the CSV files from its own directory, prints the reconstructions, and recreates **four `figure_*.png` files** and **`reconstruction_results_v1.txt`** beside the script. The files of those names are overwritten when you rerun it.

For an isolated output directory instead:

```bash
python reproduce_fake_polygraph_figures_v1.py --check --output-dir output
```

The `--check` flag runs consistency assertions, including the Fisher (2013) difference-in-differences, Strang–Peterson odds and risk ratios, published F-test tail probabilities, and the power threshold. It does **not** validate any original participant records, which are unavailable here.

Tested environment when preparing this package: Python 3; numpy 2.3.5, scipy 1.17.0, matplotlib 3.10.8, statsmodels 0.14.6. The dependency file permits a supported range rather than pinning these exact versions. Small antialiasing/font differences across platforms are possible; the statistical content is deterministic.

## Key reproduced results

- **Fisher (2013):** men's means 2.85 (non-pipeline) and 1.96 (pipeline); women's means 2.70 and 3.35. Difference-in-differences from rounded means = **1.54** partners. Fisher's reported **sex × condition interaction** is *F*(1,284)=4.57, *p*=.033. The separate **sex contrast within the pipeline** is *F*(1,284)=6.94, *p*=.009. Computing F-distribution tail probabilities checks the reported p values, **not** the underlying adjusted ANOVA. The script also prints a clearly labeled heuristic *unadjusted* difference-in-differences check; it is **not** substituted for the source paper's inferential model.
- **Tourangeau et al. (1997):** lifetime group means 7.23 (control) versus 13.43 (pipeline), a descriptive increase of 6.20 (≈85.8%). The published significant tests applied square-root transformations and adjustments; they cannot be recreated solely from these raw group means.
- **Strang & Peterson (2020):** for SES-LFP assault tactics, 3/35 (8.6%) versus 22/58 (37.9%) give an odds ratio ≈**6.52**, a risk ratio ≈**4.43**, and a two-sided Fisher exact *p*≈.00175. Other measures have different effects; see Figure 3.
- **Illustrative power calculation:** for a two-sided equal-variance independent-groups *t* test, *d*=0.25, α=.05, and equal n, power is approximately **13.9%** at 25 per group, **34.9%** at 80, and **80.1%** at 253. This is **not** the computed power of either original experiment.

## What this package does not claim

1. It does not establish any participant's true number of partners or whether responses were intentionally false.
2. It does not possess or reconstruct original survey microdata, trial records, study code, original randomization, adjustment variables, or full factorial data.
3. The group-mean confidence intervals in Figure 1 use the published *N*, means, and SDs with a conventional independent-group *t* formula. They are **unadjusted approximations**; Fisher's original reported interaction was covariate-adjusted. The paper also winsorized partner counts at 12.
4. The 1997 and 2024 between-condition or between-time differences do not necessarily isolate a specific causal effect on truthfulness. In particular, Ross's time and mode changes are confounded with the pipeline procedure.
5. This does not systematically reproduce every qualitative claim in the companion article. It covers the reported numerical reconstructions, plotted figures, and selected test-statistic checks. For a detailed inventory, see [`FIGURE_AND_CLAIM_MAP.md`](FIGURE_AND_CLAIM_MAP.md).
6. Chart geometry is generated anew from the transcribed summary statistics, so it may not be **pixel-identical** to images already embedded in a published Substack draft. Numerical inputs, substantive graphic content, and statistical descriptions are matched.

## Principal sources

- Date Psychology, [“Did a fake polygraph catch women lying about their sexual partner count?”](https://datepsychology.com/did-a-fake-polygraph-catch-women-lying-about-their-sexual-partner-count/).
- Michele G. Alexander & Terri D. Fisher (2003), [“Truth and consequences: Using the bogus pipeline to examine sex differences in self-reported sexuality”](https://doi.org/10.1080/00224490309552164).
- Terri D. Fisher (2013), [“Gender roles and pressure to be truthful: The bogus pipeline modifies gender differences in sexual but not non-sexual behavior”](https://doi.org/10.1007/s11199-013-0266-3).
- Tourangeau, Smith & Rasinski (1997), [“Motivation to report sensitive behaviors on surveys: Evidence from a bogus pipeline experiment”](https://doi.org/10.1111/j.1559-1816.1997.tb00629.x).
- Strang & Peterson (2020; online 2016), [“Use of a bogus pipeline to detect men's underreporting of sexually aggressive behavior”](https://doi.org/10.1177/0886260516681157).
- Ross, Machette & Gonzalez (2024; online 2022), [“Testing the reliability of sexual aggression self-reports”](https://doi.org/10.1080/13552600.2022.2100933).

The full bibliography and interpretive discussion are in the companion article. **No copyrighted study PDFs or third-party webpages are redistributed.**


