# Corrigendum draft: flat10MIP (GMD 18, 5699–5724, 2025)

Draft as of 2026-10-28, not yet circulated to co-authors or sent to GMD. Section numbers follow the published article.
`docx_build/` applies exactly these changes to a Word version of the paper.

## Corrigendum text

**Corrigendum to "flat10MIP: an emissions-driven experiment to diagnose the climate response to positive, zero and
negative CO2 emissions" published in Geosci. Model Dev., 18, 5699–5724, 2025**

Benjamin M. Sanderson and co-authors as in the original article

After publication, we identified an error in the calculation of the Earth system model (ESM) values of ZEC50, ZEC90,
ZEC100 and TR0 in Table 2. T100yr was computed relative to a pre-industrial baseline extrapolated from the first
30 years of esm-flat10, but the esm-flat10-zec and esm-flat10-cdr time series were referenced to the esm-flat10
temperature in a single year (year 1). The two offsets do not cancel, so the published values contained a term
reflecting single-year internal variability of up to 0.22 K. In the corrected values, all temperatures share the
baseline used for T100yr. ZECn is therefore the difference between the 20-year mean warming in esm-flat10-zec
centred n years after emissions cease and the 20-year mean warming in esm-flat10 centred on year 100.

In addition, the time of peak warming (tPW) was taken from an 11-year running mean without accounting for the offset
of the averaging window, which placed it 5 years early for every ESM. Table 2 also contained sign errors for three
entries and an incorrect T100yr for UVic-ESCM-2-10.

The corrections strengthen the main conclusions on the Zero Emissions Commitment: ESM ZEC magnitudes in
esm-flat10-zec are about 40 % smaller than in the ZECMIP protocol, rather than 30 %. The statement that most ESMs reach
peak warming before net zero no longer holds; four of the ten ESMs peak before net zero and six after. Because tPW is
estimated from a single ensemble member, individual values are sensitive to the choice of smoothing window. Corrected
code and metrics are available at https://doi.org/10.5281/zenodo.23736830 (Sanderson, 2026).

## Corrected Table 2 (ESM rows)

Published values are in parentheses where they differ. T1000PgC, the ZECMIP columns, TNZ, TR1000 and all SCM rows are
unchanged, and T100yr changes only for UVic-ESCM-2-10.

| Model | T100yr (K) | ZEC50 (K) | ZEC90 (K) | ZEC100 (K) | t-PW (years) | TR0 (K) |
| --- | --- | --- | --- | --- | --- | --- |
| ACCESS-ESM1-5 | 1.75 | 0.19 (0.21) | 0.13 (0.15) | 0.12 (0.13) | 12 (7) | 0.18 (0.17) |
| CESM2 | 1.95 | −0.11 (−0.27) | 0.02 (−0.14) | 0.03 (−0.13) | −5 (−10) | 0.49ᵈ (0.42) |
| GFDL-ESM4 | 1.45 | −0.06 (−0.21) | 0.02 (−0.13) | 0.04 (0.11) | −24 (−29) | −0.04 (−0.11) |
| GISS | 1.62 | 0.03 (0.19) | 0.07 (−0.15) | −0.02 (−0.24) | 1 (−4) | −0.42ᵈ (−0.56) |
| NorESM2-LM | 1.18 | −0.13 (−0.23) | −0.12 (−0.21) | −0.22 (−0.31) | −28 (−33) | −0.22 (−0.31) |
| MPI-ESM1-2-LR | 1.50 | −0.14 | −0.16 (−0.17) | −0.24 | 6 (1) | −0.33 (−0.29) |
| CNRM-ESM2-1 | 1.72 | −0.01 | 0.06 (0.067) | 0.09 (0.11) | −5 (−10) | 0.31 (0.38) |
| UKESM1.2 | 2.50 | 0.26 (0.27) | 0.18 (0.19) | 0.20 | 4 (−1) | 0.31ᵈ (–) |
| UVic-ESCM-2-10 | 1.86 (1.80) | 0.07 (0.01) | 0.12 (−0.11) | 0.13 (0.12) | 8 (3) | 0.26 (0.25) |
| HadCM3LC-Bris | 1.53 | −0.03 (−0.02) | −0.05 (−0.04) | −0.03 (−0.02) | 11 (6) | −0.18 (0.15) |

New footnote d: "TR0 approximated from years 291–300 because the esm-flat10-cdr simulation ends in year 300: the mean
temperature over those years minus the warming expected from the 45 PgC of cumulative emissions remaining on average
(0.045 × T100yr)." On the seven full-length simulations this approximation reproduces TR0 with no mean bias and an RMSE
of 0.07 K.

Table 2 caption: replace "measured as the warming in esm-flat10-zec between years 100 and years 150/190/200,
respectively" with "measured as the difference between the 20-year mean warming in esm-flat10-zec centred on years
150/190/200 and the 20-year mean warming in esm-flat10 centred on year 100, respectively".

## Text corrections

Four correct statements that the revised Table 2 makes wrong; two correct method descriptions that would lead a reader
reproducing TNZ or tPW to different values (by up to 0.16 K and 6 years).

| # | Location | Published text | Corrected text |
| --- | --- | --- | --- |
| 1 | Abstract | "the magnitude of ZEC50 in ESMs is, on average, reduced by 30 % compared with 1pctCO2 branch experiments" | "… reduced by about 40 % compared with 1pctCO2 branch experiments" |
| 2 | Sect. 2.1.4, TNZ | "TNZ is calculated as a 21-year average around year 150 in esm-flat10-cdr (i.e., 50 years after branching from esm-flat10) minus the expected temperature at net zero using cumulative emissions proportionality (Tref, which is 1.25 times the esm-flat10-derived TCRE; see Fig. 2)." | "TNZ is calculated as the 20-year mean temperature in esm-flat10-cdr centred on year 150 (years 140–159, i.e., 50 years after branching from esm-flat10) minus the expected temperature at net zero using cumulative emissions proportionality (Tref, the 20-year mean temperature in esm-flat10 centred on year 125, years 115–134, when cumulative emissions in esm-flat10 also reach 1250 PgC; see Fig. 2)." |
| 3 | Sect. 2.1.4, tPW | "the peak value of 20-year smoothed global mean temperatures" | "the peak value of 11-year smoothed global mean temperatures" |
| 4 | Sect. 3.1 | "peak warming can occur either before or after net zero (but most models peak before)" | "… (four of the ten ESMs peak before net zero and six after)" |
| 5 | Sect. 3.2.2 | "ESMs are also consistent with the relationship of ∼ 25 % smaller absolute magnitudes in ZEC50 and ZEC90, albeit with larger scatter." | "ESMs show a larger reduction, with ∼ 40 % smaller absolute magnitudes in ZEC50 and ZEC90 (best-fit slopes of 0.59 and 0.57; Fig. 8c, d), albeit with larger scatter." |
| 6 | Sect. 3.2.3 | "a number of ESMs (CNRM, GISS, CESM, UKESM) lie outside of the SCM distributions such that we see peak warming significantly before net zero with greater warming than one would expect from cumulative emissions proportionality" | Delete "such that we see peak warming significantly before net zero". |

The 40 % is the reduction in mean |ZEC50| for the five models with same-version ZECMIP simulations (ACCESS, CESM2,
NorESM, MPI-ESM, CNRM-ESM2): 41 %.

## Replacement figures

Captions are unchanged.

* **Fig. 7**: panel a uses the corrected ESM ZEC50 and ZEC90, and the multi-model-mean point uses ZEC90 like the
  individual models. Panel b is as published. File: `images/flat10_zec_tcre_comparison.pdf`.
* **Fig. 8**: ESM ZEC50 and ZEC90 points and best-fit lines use the corrected values (ESM fits y = 0.05 + 0.59x and
  y = 0.03 + 0.57x). File: `images/flat10_SCM_ESM_metric_correlations.pdf`.
* **Fig. 13**: ESM points use the corrected ZEC50, ZEC90, ZEC100, tPW and TR0. File: `images/flat10_metric_pairplot.pdf`.

## Left out of the corrigendum

The test for inclusion was whether a reader quoting, citing or reproducing the paper would otherwise take away
something wrong. These items are fixed in the code but not in the corrigendum:

| Item | Why it is left out |
| --- | --- |
| Fig. 10 | Only the dotted TCRE · Iem + ZEC reference lines move (by up to 0.2 K), and the conclusion drawn from them holds |
| Year-300 warmer/cooler model lists (Sect. 3.1) | Every listed model remains correctly placed; UKESM and HadCM3 are simply not listed |
| "0.05 K" T + ZEC90 difference (Sect. 3.2.2) | Corrected to about 0.01 K, which strengthens the path-independence statement |
| Year-300 range of −0.7 to +0.5 K (Sect. 3.2.3) | Describes annual values in Fig. 4c rather than the 20-year TR0 of Table 2 |
| Fig. 4 peak markers 5 years early | Visually minor on a 300-year axis; Table 2 carries the corrected tPW |
| SCM ZEC90 vs ZEC100 in Fig. 7b and the "∼ 0.1 K" sentence (Sect. 3.2.2) | Using ZEC100 on both sides moves the SCM means by 0.00–0.03 K |
| "21-year" window wording (Sects. 2.1.2, 2.1.4), Fig. 4 caption smoothing | Wording only |
| "see Table 1" for Table 2 (Sect. 3.2.1) | Cross-reference slip |
| A common regression-estimated pre-industrial baseline | A methodological choice, not an error; implemented on the `flat10-corrigendum-full` branch |

## Code and data availability (proposed addition)

"The corrected analysis code (flat10_figures_paper.ipynb), a stand-alone script that reproduces both the published and
corrected ESM metrics from the global-mean output (flat10_esm_metrics.py), and the corrected metrics
(esm_metrics_flat10_corrected.csv) are archived at https://doi.org/10.5281/zenodo.23736830."

## Reference (to add to the corrigendum)

Sanderson, B. M.: benmsanderson/esm-deck: Corrected ZEC values for corrigendum (corrigendum), Zenodo [code],
https://doi.org/10.5281/zenodo.23736830, 2026.
