# Figure and statistical claim map

This document identifies the calculations that can be reproduced from the CSV
inputs. A successful run is a reconstruction of *published summaries*, **not**
a replication using original participant-level observations.

| Companion article location | Input | Produced calculation / figure | What cannot be recovered |
|---|---|---|---|
| §3, Alexander & Fisher (2003) | `alexander_fisher_2003_partner_means.csv` | Means by sex and setting; descriptive differences | Cell-level n and SD, original F test on partner counts, accuracy of histories |
| §4, Fisher (2013), Figure 1 | `fisher_2013_table4_partner_counts.csv`; `published_f_tests.csv` | Four means, approximate *unadjusted* 95% mean CIs, 1.54 difference-in-differences; reported tests checked using F distribution | Original covariate-adjusted ANOVA or its exact confidence interval; any real partner histories |
| §5, Figure 4 | Model parameters in the code (d=.25, two-sided α=.05, equal n) | Noncentral-t power curve, n=25/80/253, minimum integer group size achieving ≥80% | Power of any particular published study's actual factorial design |
| §6, Tourangeau et al. (1997), Figure 2 | `tourangeau_1997_partner_means.csv`; `published_f_tests.csv` | Group differences and ratio; F-tail probability checks | Raw-count/adjusted model regeneration without original observations; precision intervals |
| §7, Strang & Peterson, Figure 3 | `strang_peterson_2020_table3.csv` | Sample proportions, exact 2x2 Fisher test, odds ratios, risk ratios; group comparison graphics | Any treatment effect on unobserved true behavior; precision for other untranscribed measures |
| §8, Ross et al. (2024) | `ross_2024_victimization_prevalence.csv` | Percentage-point differences by sex across survey occasions | Separation of time/order/mode/pipeline effects; individual-level paired tests |

## Assumptions and inference

- **Figure 1 intervals**: a *t* interval of `mean ± t_(0.975,n−1) × SD/√n` for each of the four reported cell means. This is an *unadjusted* descriptive approximation and is not the source paper's adjusted interval. Fisher's Table 4 values were winsorized at 12 partners, and the model included a covariate affected by the manipulation.
- **Fisher difference-in-differences**: `(women pipeline − women non-pipeline) − (men pipeline − men non-pipeline) = 1.54`. It is calculated directly from the rounded published means. It is **not** the same statistic as the paper's covariate-adjusted F test.
- **Figure 2**: the heights are rounded published means. There are no defensible inferential intervals to plot from these figures alone. The adjusted, square-root-transformed tests in the paper are different analyses from mean comparisons of the plotted raw counts.
- **Figure 3**: exact yes/total counts reproduce the percentages rounded to one decimal. The odds ratio from the first two-by-two table is `(22/36)/(3/32)≈6.52`; the corresponding risk ratio `(22/58)/(3/35)≈4.43`. The two-sided Fisher exact p≈.00175, displayed as .002 in the paper. For comparison 2, p≈.125; for comparison 3, p=1.0.
- **Figure 4**: this is a hypothetical conventional equal-variance independent-samples *t* test, not a post-hoc power calculation or estimate of the published factorial model's power. Calculations use the noncentral *t* distribution.
- **Causal scope**: a change in reports is not itself independently validated truthfulness. The studies and this reconstruction cannot distinguish all causes of reporting differences.
- **Numerical precision**: printed means, percentages, and test values are rounded in the source papers. Tiny discrepancies between independently recomputed figures and published numbers are expected.

## Original sources

1. Michele G. Alexander & Terri D. Fisher (2003), *Journal of Sex Research*: https://doi.org/10.1080/00224490309552164
2. Terri D. Fisher (2013), *Sex Roles*, especially Table 4 and the test results on p. 409: https://doi.org/10.1007/s11199-013-0266-3
3. Tourangeau, Smith & Rasinski (1997), *Journal of Applied Social Psychology*: https://doi.org/10.1111/j.1559-1816.1997.tb00629.x
4. Strang & Peterson (2020; online 2016), *Journal of Interpersonal Violence*, especially Table 3: https://doi.org/10.1177/0886260516681157
5. Ross, Machette & Gonzalez (2024; online 2022), *Journal of Sexual Aggression*: https://doi.org/10.1080/13552600.2022.2100933
6. The Date Psychology article being critiqued: https://datepsychology.com/did-a-fake-polygraph-catch-women-lying-about-their-sexual-partner-count/

The article's complete reference list provides the additional background literature.
No study PDFs or original participant records are redistributed here.
