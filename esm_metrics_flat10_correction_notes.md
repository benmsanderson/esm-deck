# flat10MIP ESM metrics: corrigendum notes (Sanderson et al., 2025, GMD 18, 5699, Table 2)

`flat10_esm_metrics.py` recomputes the ESM rows of Table 2 from `ESM_data/` in two ways:

* **legacy**: the method behind the published table (`flat10_figures.ipynb`, Aug 2024). It reproduces the
  published values apart from the transcription errors listed below.
* **corrected**: the values written to `esm_metrics_flat10_corrected.csv` and used by `flat10_figures_paper.ipynb`.

This branch implements the *light* corrigendum: only errors that change a published number, statement or visible
figure are corrected. A fuller version is kept on the `flat10-corrigendum-full` branch. It also moves all
temperatures to a regression-estimated pre-industrial baseline and tidies further method wording.

## Errors

1. **ZEC50/90/100 and TR0 baselines.** T100yr is referenced to the pre-industrial state extrapolated from esm-flat10
   years 0–29, `cn0 = 2·mean(yrs 0–19) − mean(yrs 10–29)`. The esm-flat10-zec and esm-flat10-cdr series were instead
   referenced to the esm-flat10 temperature in year 1 alone. The two offsets do not cancel, so the published ZEC and
   TR0 values contain single-year variability of up to 0.22 K. T100yr, TNZ and TR1000 are unaffected.
2. **tPW.** It was located in an 11-year `np.convolve(..., 'valid')` running mean without adding back the 5-year window
   offset, so every value is 5 years early.
3. **Transcription errors in Table 2.**
   * The signs of GISS ZEC50, GFDL ZEC100 and UVic ZEC90 are reversed.
   * UVic T100yr (1.80, should be 1.86) and ZEC50 are incorrect.
   * The HadCM3LC-Bris row mixes two calculation methods.
4. **Figures.**
   * The Fig. 7a multi-model mean used ZEC100 where the individual models used ZEC90.
   * Fig. 10 plotted TCRE·Iem + ZEC100 although its caption says ZEC90.

## Corrected method

All temperatures are referenced to cn0, the published T100yr baseline (indices 0-based from the start of esm-flat10;
zec and cdr runs branch at year 100):

| Metric | Definition |
|---|---|
| T100yr | flat10 years 90–109 minus cn0 (unchanged) |
| ZEC50 / ZEC90 / ZEC100 | flat10-zec years 140–159 / 180–199 / 190–209 minus flat10 years 90–109 |
| tPW | centre year of the peak 11-year running mean of flat10-cdr, minus 150 |
| TR0 | flat10-cdr years 300–319 minus cn0. CESM2, GISS and UKESM runs end in year 299: years 290–299 minus cn0 minus 0.045 × T100yr (warming from the 45 PgC of cumulative emissions remaining on average). On the seven full-length runs this approximation has 0.00 K bias and 0.07 K RMSE. |

## Corrected values (ESM rows; published in parentheses where different)

| Model | T100yr | ZEC50 | ZEC90 | ZEC100 | tPW | TR0 |
|---|---|---|---|---|---|---|
| ACCESS-ESM1-5 | 1.75 | 0.19 (0.21) | 0.13 (0.15) | 0.12 (0.13) | 12 (7) | 0.18 (0.17) |
| CESM2 | 1.95 | −0.11 (−0.27) | 0.02 (−0.14) | 0.03 (−0.13) | −5 (−10) | 0.49* (0.42) |
| GFDL-ESM4 | 1.45 | −0.06 (−0.21) | 0.02 (−0.13) | 0.04 (0.11) | −24 (−29) | −0.04 (−0.11) |
| GISS | 1.62 | 0.03 (0.19) | 0.07 (−0.15) | −0.02 (−0.24) | 1 (−4) | −0.42* (−0.56) |
| NorESM2-LM | 1.18 | −0.13 (−0.23) | −0.12 (−0.21) | −0.22 (−0.31) | −28 (−33) | −0.22 (−0.31) |
| MPI-ESM1-2-LR | 1.50 | −0.14 | −0.16 (−0.17) | −0.24 | 6 (1) | −0.33 (−0.29) |
| CNRM-ESM2-1 | 1.72 | −0.01 | 0.06 (0.067) | 0.09 (0.11) | −5 (−10) | 0.31 (0.38) |
| UKESM1.2 | 2.50 | 0.26 (0.27) | 0.18 (0.19) | 0.20 | 4 (−1) | 0.31* (–) |
| UVic-ESCM-2-10 | 1.86 (1.80) | 0.07 (0.01) | 0.12 (−0.11) | 0.13 (0.12) | 8 (3) | 0.26 (0.25) |
| HadCM3LC-Bris | 1.53 | −0.03 (−0.02) | −0.05 (−0.04) | −0.03 (−0.02) | 11 (6) | −0.18 (0.15) |

\* approximated from years 290–299 (see above). TNZ and TR1000 are unchanged.

## Corrigendum contents

* **Table 2:** the values above, a new footnote for the approximated TR0, and a caption that defines ZEC as a
  difference of 20-year means.
* **Text:**
  * Abstract: ZEC50 reduction of about 40 % instead of 30 %.
  * Sect. 2.1.4: TNZ definition (flat10 at 1250 PgC, not 1.25 × TCRE), and tPW smoothing "20-year" → "11-year".
  * Sect. 3.1: 4 of 10 ESMs peak before net zero, not "most"; UKESM added to the warmer and HadCM3 to the cooler models at year 300.
  * Sect. 3.2.2: ∼ 40 % (not ∼ 25 %) smaller ESM ZEC; T + ZEC90 difference of 0.01 K (not 0.05 K).
  * Sect. 3.2.3: year-300 range −0.4 to +0.5 K; GISS and UKESM no longer described as peaking before net zero.
* **Figures:** 7, 8, 10 and 13 are replaced.

Not corrected in the light version (no result changes):

* Fig. 4 peak markers (fixed in the code: they are now at the centre year of the window).
* The SCM ZEC90/ZEC100 mix in Fig. 7b.
* "21-year" window wording.
* The "Table 1" cross-reference slip.

## Notebook

`flat10_figures_paper.ipynb` was re-executed end to end with numpy 1.26, pandas 2.1, xarray 2024.3 and matplotlib 3.9.
Its printed metrics match `esm_metrics_flat10_corrected.csv`. Other changes:

* The MAGICC timeseries filename case is fixed (`flat10_MAGICC.nc`).
* Figs. 6, 7, 9 and 13, previously only displayed, are now saved:
  * Fig. 6: `images/flat10_1pct_comparison.*`
  * Fig. 7: `images/flat10_zec_tcre_comparison.*`
  * Fig. 9: `images/flat10_zecmip_timeseries.*`
  * Fig. 13: `images/flat10_metric_pairplot.*`
* Figures whose content does not change keep their committed image files.
