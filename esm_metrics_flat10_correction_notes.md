# flat10MIP ESM metrics: correction notes (Sanderson et al., 2025, GMD 18, 5699, Table 2)

`flat10_esm_metrics.py` recomputes the ESM rows of Table 2 from `ESM_data/` using two methods:

* **legacy**: the method that produced the published table (`flat10_figures.ipynb`, Aug 2024).
* **corrected**: the values written to `esm_metrics_flat10_corrected.csv`.

## What was wrong

1. **Inconsistent baselines in ZEC and TR0.** T100yr is referenced to
   `cn0 = 2·mean(yrs 0–19) − mean(yrs 10–29)` of esm-flat10, but the flat10-zec and
   flat10-cdr series were referenced to the esm-flat10 tas of a single year (year 1).
   These offsets do not cancel, so published ZEC50/90/100 and TR0 contain the term
   `cn0 − T(yr 1)`. That is single-year variability, up to ~0.2 K, the same size as ZEC itself.
   T100yr, TNZ and TR1000 are unaffected.
   The April 2025 revision (`flat10_figures_paper.ipynb`) swapped the year-1 offset
   for a 30-year regression intercept. That reduces the term but does not remove it.
2. **tPW is 5 years early.** The peak was located in an 11-year `np.convolve(..., 'valid')`
   moving average without adding back the 5-year offset of the valid window.
3. **Transcription errors in Table 2:** the signs of GISS ZEC50 (+0.19, should be −0.19 under the
   legacy method), GFDL ZEC100 (+0.11 → −0.11) and UVic ZEC90 (−0.11 → +0.11).
   UVic T100yr (1.80) and ZEC50 (0.01) are not reproducible: the legacy method gives 1.86 and 0.06.
   The HadCM3LC-Bris row partly comes from the April 2025 regression baseline (TR0 0.15 is not
   reproducible from current data).
4. CESM2 and GISS flat10-cdr runs end at year 299, so their TR0 is a 10-year mean (years 290–299).

## Published vs legacy recomputation vs corrected

| Model | ZEC50 pub / legacy / **corr** | ZEC90 pub / legacy / **corr** | ZEC100 pub / legacy / **corr** | tPW pub / **corr** | TR0 pub / legacy / **corr** |
|---|---|---|---|---|---|
| ACCESS-ESM1-5 | 0.21 / 0.21 / **0.19** | 0.15 / 0.15 / **0.13** | 0.13 / 0.13 / **0.12** | 7 / **12** | 0.17 / 0.17 / **0.16** |
| CESM2 | −0.27 / −0.26 / **−0.11** | −0.14 / −0.14 / **0.02** | −0.13 / −0.13 / **0.03** | −10 / **−5** | 0.42 / 0.42 / **0.57** |
| GFDL-ESM4 | −0.21 / −0.21 / **−0.06** | −0.13 / −0.13 / **0.02** | 0.11 / −0.11 / **0.04** | −29 / **−24** | −0.11 / −0.11 / **0.04** |
| GISS | 0.19 / −0.19 / **0.03** | −0.15 / −0.15 / **0.07** | −0.24 / −0.24 / **−0.02** | −4 / **1** | −0.56 / −0.56 / **−0.35** |
| NorESM2-LM | −0.23 / −0.23 / **−0.13** | −0.21 / −0.21 / **−0.12** | −0.31 / −0.31 / **−0.22** | −33 / **−28** | −0.31 / −0.31 / **−0.22** |
| MPI-ESM1-2-LR | −0.14 / −0.14 / **−0.14** | −0.17 / −0.17 / **−0.16** | −0.24 / −0.24 / **−0.24** | 1 / **6** | −0.29 / −0.29 / **−0.29** |
| CNRM-ESM2-1 | −0.01 / 0.00 / **−0.01** | 0.067 / 0.07 / **0.06** | 0.11 / 0.11 / **0.09** | −10 / **−5** | 0.38 / 0.38 / **0.36** |
| UKESM1.2 | 0.27 / 0.27 / **0.26** | 0.19 / 0.19 / **0.18** | 0.20 / 0.21 / **0.20** | −1 / **4** | – / 0.43 / **0.42** |
| UVic-ESCM-2-10 | 0.01 / 0.06 / **0.07** | −0.11 / 0.11 / **0.12** | 0.12 / 0.12 / **0.13** | 3 / **8** | 0.25 / 0.25 / **0.26** |
| HadCM3LC-Bris | −0.02 / 0.02 / **−0.03** | −0.04 / 0.00 / **−0.05** | −0.02 / 0.02 / **−0.03** | 6 / **11** | 0.15 / 0.01 / **−0.04** |

T100yr, TNZ and TR1000 are unchanged. The only exception is UVic T100yr, which should read 1.86.
Still to check for a GMD correction: any figures and text that use the ESM ZEC, TR0 or tPW values,
including the ESM-vs-1pctCO2 ZEC comparison and the T100yr+ZEC panels.

## Affected passages in the published paper

Effects are judged with the corrected values in `esm_metrics_flat10_corrected.csv`.
"Pub." is the published value and "legacy" is the published method recomputed.

### Claims that change

| # | Location | Published text | Corrected |
|---|---|---|---|
| A1 | Abstract | "the magnitude of ZEC50 in ESMs is, on average, reduced by 30 % compared with 1pctCO2" | 33 % (all 7 models with ZECMIP values) or 41 % (the 5-model same-version subset). The published 30 % cannot be reproduced from Table 2 with either subset under the legacy method (4 % / 15 %), so first confirm how it was derived (regression slope in Fig. 8?). The direction holds and gets stronger. |
| A2 | Abstract; Sect. 3.4 ("peak warming can occur either before or after net zero (but most models peak before)") | 6 of 10 ESMs peak before net zero | 4 of 10 peak before (CESM2, GFDL, NorESM, CNRM) and 6 after. "Most models peak before" is no longer true. "Before or after" still holds. |
| A3 | Sect. 3.4 ("some models remain warmer ... (CESM, CNRM, ACCESS, UVic), while some are cooler (GISS, MPI, NorESM, GFDL)") | GFDL TR0 = −0.11 | GFDL TR0 = +0.04, i.e. ≈0 / slightly warmer. UKESM (+0.42) is also warmer but not listed. HadCM3 −0.04. |
| A4 | Sect. 3.7 ("The temperature response at year 300 ... range of −0.7 to +0.5 K") | | Table-based TR0 range is −0.35 to +0.57 K (corrected) and −0.56 to +0.43 K (legacy). Check against Fig. 4c / TR0 definition (see B3). |
| A5 | Sect. 3.6 ("ESMs are also consistent with the relationship of ∼ 25 % smaller absolute magnitudes in ZEC50 and ZEC90, albeit with larger scatter") | | ESM reductions are now 33–41 % (ZEC50) and 45–57 % (ZEC90), larger than the SCMs' ~25 %. Reword as "at least as large as". |
| A6 | Sect. 3.6 ("the multi-model mean T1000PgC + ZEC90 is 0.05 K greater for esm-1pct-brch-1000PgC than T100yr + ZEC90") | 0.05 K (legacy recomputation gives 0.03 K) | −0.01 K. This strengthens the path-independence statement in the same paragraph. |
| A7 | Sect. 3.7, Fig. 13 discussion ("a number of ESMs (CNRM, GISS, CESM, UKESM) ... peak warming significantly before net zero with greater warming than one would expect") | tPW: CNRM −10, GISS −4, CESM −10, UKESM −1 | CNRM −5, GISS +1, CESM −5, UKESM +4. GISS and UKESM now peak after net zero. The "outside the 99th percentile of SCM tPW–TNZ" statement needs re-checking against Fig. 13. |
| A8 | Sect. 3.7 ("tPW and ZEC50, with two ESMs showing peak warming occurring particularly early") | GFDL −29, NorESM −33 | GFDL −24, NorESM −28. Still the two earliest, so the statement holds but Fig. 13 moves. |
| A9 | Sect. 3.7 ("greater correlation ... (ZEC50, TR1000) than ... TR0"; "high correlation (e.g., between ZEC50 and TR1000 and between ZEC100 and TR1000)") | ESM r(ZEC50,TR1000) = 0.82, r(ZEC100,TR1000) = 0.80, r(ZEC50,TR0) = 0.54 | 0.91, 0.81, 0.37. The statement holds and gets stronger. |
| A10 | Sect. 3.7 ("With the exception of TCRE, all metrics show a positive correlation") | | ESM correlations with tPW weaken (e.g. r(ZEC90,tPW) 0.60 → 0.34, r(TR0,tPW) 0.27 → 0.13) but stay positive. The statement is unchanged; the qualifier "particularly for SCMs" still fits. |
| A11 | Conclusions ("values of ZEC estimated with 1pctCO2 tend to be greater than for esm-flat10-zec") | | Holds and gets stronger (see A1, A5). |

### Method descriptions that do not match the code

| # | Location | Text | Code |
|---|---|---|---|
| B1 | Sect. 2.2 (esm-flat10-zec) | ZEC50 "relative to that when emissions cease, averaged over a 21-year period ... (i.e., years 140–160)" | 20-year means (years 140–159 vs flat10 years 90–109). The corrected method matches the wording; the legacy method did not (single-year baseline term). |
| B2 | Sect. 2.4 (TNZ) | cdr years ~150 minus Tref = 1.25 × T100yr | cdr years 140–159 minus flat10 years 115–134, i.e. the actual flat10 temperature at 1250 PgC, not 1.25 × TCRE. |
| B3 | Sect. 2.4 (TR0) | "average of years 301–320 in esm-flat10-cdr minus mean global temperatures in esm-piControl" | cdr years 290–309 (290–299 for CESM2 and GISS, whose runs end at year 299), relative to the extrapolated esm-flat10 start (cn0), not esm-piControl. |
| B4 | Sect. 2.4 (tPW) | "peak value of 20-year smoothed global mean temperatures" | 11-year running mean, with the peak index not re-centred (5 years early; fixed in the corrected values). |
| B5 | Fig. 10 caption and Sect. 3.7 | dotted lines are "TCRE ⋅ Iem + ZEC90" | the code (`flat10_figures_paper.ipynb`, temp_vs_cumulative_emissions_panel) plots + ZEC100. |
| B6 | Fig. 7b, Table 2 SCM header, Sect. 3.6 ("for MAGICC and CICERO-SCM ... T1000PgC + ZEC90 is ∼ 0.1 K greater") | SCM 1pctCO2 ZEC90 | the violins labelled "T1000PgC + ZEC90" use the SCM `zec100` from esm-1pct-brch-1000PgC, and the Table 2 SCM header says ZEC100. The SCM 1pct comparison mixes ZEC90 and ZEC100. |
| B7 | Table 2 caption | ZEC "measured as the warming in esm-flat10-zec between years 100 and years 150/190/200" | ESM values use 20-year windows. SCM flat10 values use single years (T[150] − T[100]). Harmless for SCMs (no internal variability) but inconsistent with the ESM definition. |
| B8 | Sect. 3.2 ("0.12 K greater in 1pctCO2 relative to esm-flat10 (see Table 1, Fig. 7)") | | should be Table 2. Value unaffected. |

### Figures

| Figure | Status |
|---|---|
| Fig. 3 (SCM/ESM results panel) | ESM curves are plotted relative to flat10 years 90–109, i.e. the corrected definition, so **unaffected**. The published Table 2 disagrees with this figure. |
| Fig. 4c (ESM results, cdr column) | circles marking peak warming are plotted 5 years early (uncentred index). Regenerate. |
| Fig. 7a (T100yr + ZEC50/90 bars) | uses Table 2 ESM ZEC. Regenerate. Panel b: see B6. |
| Fig. 8 (flat10 vs 1pctCO2 scatter) | ESM ZEC50/ZEC90 points move (e.g. CESM2 ZEC50 −0.26 → −0.11). Regenerate, and refit the ESM best-fit line. |
| Fig. 9 (ESM ZEC time series) | curves use a consistent baseline, so **unaffected**. |
| Fig. 10 (T vs cumulative emissions) | curves unaffected. Dotted TCRE·Iem + ZEC lines shift (GFDL by +0.15 K, CESM2 +0.16 K, GISS +0.22 K). Re-check the statement that "GFDL, UKESM show a larger hysteresis than predicted by ZEC90". |
| Fig. 13 (metric correlation matrix) | ESM points move in the ZEC50/90/100, tPW and TR0 rows and columns. Regenerate. |
| Table 2 | ESM ZEC50/90/100, tPW and TR0 columns, the three sign typos, UVic T100yr, and the mixed-method HadCM3 row. |

Unaffected: T100yr/TCRE values and the TCRE comparison (Sect. 3.2, Fig. 6), TNZ, TR1000, all carbon-cycle results
(Figs. 4d–l, 5), and all SCM values.
