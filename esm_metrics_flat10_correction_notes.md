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

## Notebook changes and regenerated figures

Changes to `flat10_figures_paper.ipynb` (re-executed end to end; numpy 1.26, pandas 2.1, xarray 2024.3, matplotlib 3.9):

* **Metrics (cell 38):** ZEC50/90/100 and TR0 are referenced to cn0, the same baseline as T100yr. tPW adds `window//2` to the
  peak index. The printed metrics now match `esm_metrics_flat10_corrected.csv` exactly.
* **Fig. 4 (cell 19):** peak markers in the cdr column (GMST, CO2, land, ocean) are moved to the centre year of the moving
  average (+5 years). The text statements on carbon-cycle peak timing still hold. Peak years, corrected, with net zero = 150:
  CO2 125–138 (all before net zero); ocean sink 175–186 (all after); land sink 139–146 for ACCESS, UVic and HadCM3 (before)
  and 160–174 for the others (after).
* **Fig. 7a (cell 41):** the flat10 multi-model-mean point used ZEC100 while the individual models used ZEC90. Both now use ZEC90.
* **Fig. 10 (cell 46):** dotted line changed from + ZEC100 to + ZEC90, matching the caption and text (resolves B5).
* `SCM_data/timeseries/flat10_magicc.nc` → `flat10_MAGICC.nc` (the notebook only ran on case-insensitive file systems).
* Figs. 7, 9 and 13 were previously displayed but not saved. Save calls were added.

| Paper figure | File | Changed? |
|---|---|---|
| Fig. 4 | `images/flat10_ESM_results_panel.{pdf,jpg}` | yes: peak markers |
| Fig. 7 | `images/flat10_zec_tcre_comparison.{pdf,jpg}` (new) | yes: ESM ZEC, mean point |
| Fig. 8 | `images/flat10_SCM_ESM_metric_correlations.{pdf,jpg}` | yes: ESM ZEC points and fits (ESM ZEC50 slope 0.59, ZEC90 slope 0.57) |
| Fig. 9 | `images/flat10_zecmip_timeseries.{pdf,jpg}` (new) | no: saved for completeness |
| Fig. 10 | `images/temp_vs_cumulative_emissions_panel.png` | yes: dotted ZEC90 lines |
| Fig. 13 | `images/flat10_metric_pairplot.{pdf,jpg}` (new) | yes: ESM ZEC, tPW, TR0 |

Figs. 3, 5, 6 and the schematic figures were not changed, so their committed image files were left as they were.

## Follow-up decisions (2026-10-15)

* **Abstract:** "about 40 %", based on the five same-version models (41 %).
* **TNZ:** keep the calculation and correct the text.
* **TR0:** keep the text's concept (years 301–320 relative to esm-piControl). esm-piControl is estimated as the
  intercept of a linear fit to esm-flat10 years 0–29. Corrected TR0: ACCESS 0.17, GFDL −0.06, NorESM −0.24, MPI −0.32,
  CNRM 0.31, UVic 0.25, HadCM3 −0.17 K. The CESM2, GISS and UKESM esm-flat10-cdr runs end in year 299. For these,
  TR0 is approximated from years 290–299 minus T100yr × 45 PgC (the mean cumulative emissions still present in that
  window). Validated on the seven full-length runs: bias 0.00 K, RMSE 0.07 K, max error 0.13 K. Values: CESM2 0.43,
  GISS −0.42, UKESM 0.31 K (flagged as approximate in Table 2). No new simulations are requested.
* **SCM ZEC90 vs ZEC100:** the SCM esm-1pct-brch-1000PgC metrics provide ZEC50 and ZEC100 only. Fig. 7b now
  compares T + ZEC100 on both sides. The 1pct minus flat10 differences are FaIR +0.01 K, MAGICC +0.08 K,
  CICERO-SCM +0.21 K. Fig. 8b,d SCM points were already ZEC100 on both axes; only their labels need correcting.
* **Fig. 13:** in the tPW–TNZ plane, CNRM, GISS, CESM2 and UKESM lie outside the highest-density region holding 99 % of
  each SCM ensemble (KDE). The "99th percentile" statement holds.
* **Figs. 11 and 12** do not use ESM ZEC, tPW or TR0 (confirmed by B. Sanderson).

* **Common baseline (decided 2026-10-15):** T100yr now uses the same regression-estimated esm-piControl baseline as TR0,
  replacing cn0 everywhere in the notebook. T100yr changes by at most 0.06 K: ACCESS 1.74, CESM2 1.89, GFDL 1.44,
  GISS 1.62, NorESM 1.16, MPI 1.51, CNRM 1.73, UKESM 2.51, UVic 1.86, HadCM3 1.53 K. ZEC, TNZ, TR1000 and tPW do not
  depend on the baseline. Text numbers affected: the ESM T100yr range becomes 1.2–2.5 K; the mean T1000PgC − T100yr
  offset becomes 0.11 K (five same-version models; published 0.12 K); the T + ZEC90 difference becomes < 0.01 K.
  Figures that plot ESM temperatures on this baseline also shift slightly: Fig. 3a, Fig. 6d (now saved as
  `images/flat10_1pct_comparison.*`), Fig. 9, Fig. 10 and the TCRE-normalised plume figure (`images/T_vs_CE_plumes_flatcdr.png`).
