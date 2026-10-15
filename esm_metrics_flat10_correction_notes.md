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
