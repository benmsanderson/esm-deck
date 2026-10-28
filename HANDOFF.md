# Handoff: flat10MIP GMD corrigendum (as of 2026-10-28)

This project is moving to a new account. Everything needed to continue is in this repository; documents created in
the previous account's Claude workspace are not accessible from the new one, and their content is copied into
`corrigendum/`.

## Background

Roland Séférian could not reproduce the ZEC50/ZEC100 values in Table 2 of Sanderson et al. (2025), *flat10MIP*,
GMD 18, 5699–5724, https://doi.org/10.5194/gmd-18-5699-2025. Tracing the code showed the following:

* **Baseline error:** the published ESM ZEC50/90/100 and TR0 mix two baselines. T100yr uses the pre-industrial state
  extrapolated from esm-flat10 years 0–29 (`cn0`), while the zec/cdr series were referenced to the esm-flat10 year-1
  temperature. This leaves single-year variability of up to 0.22 K in those metrics.
* **tPW:** 5 years early for every model (uncentred running mean).
* **Table 2 transcription errors:** three sign errors, a wrong UVic row, and a mixed-method HadCM3 row.

Details, corrected values and the method are in `esm_metrics_flat10_correction_notes.md`.

## Where things stand

| Item | Status |
| --- | --- |
| Corrected code, metrics, figures | Done; [PR #15](https://github.com/benmsanderson/esm-deck/pull/15) merged into `main` on 2026-10-28 |
| Corrigendum text | Drafted: `corrigendum/corrigendum_text.md` (Table 2, six text edits, Figs. 7, 8, 13) |
| Word version of the paper with the corrigendum as tracked changes | Reproducible with `corrigendum/docx_build/build.sh` |
| Ensemble-distribution analysis for co-authors (e.g. Charlie Koven, for IPCC) | `corrigendum/distribution_shifts.md` + `.png` + `.py` |
| Email to co-authors | Circulated; no further comments as of 2026-10-28 |
| Reply to Roland | Drafted in `corrigendum/email_drafts.md`; not known to be sent |
| GMD submission | Not started. Corrigenda must reach Copernicus within 3 years of publication (by Sept 2028); only one corrigendum per article in that window, so bundle everything. Email the GMD editorial office / handling editor first. |
| Zenodo archive of the corrected code | Done: GitHub release `corrigendum` (commit `ea557e2`), https://doi.org/10.5281/zenodo.23736830; cited in the corrigendum text |

## Decisions taken (by Ben)

* **Scope:** a narrow corrigendum. It corrects only what a reader quoting, citing or reproducing the paper would
  otherwise get wrong: Table 2, six text edits, and Figs. 7, 8 and 13. Everything else is fixed in code only;
  `corrigendum/corrigendum_text.md` lists what was left out and why.
* **Baseline:** keep the published T100yr baseline (cn0), so T100yr is unchanged. ZEC becomes the plain difference of
  20-year means.
* **tPW:** keep 11-year smoothing; fix the text from "20-year" to "11-year" rather than recomputing.
* **TR0:** years 301–320 relative to the baseline. The three runs ending in year 299 (CESM2, GISS, UKESM) are
  approximated from years 291–300 minus 0.045 × T100yr (validated RMSE 0.07 K). No new simulations are requested.
* **TNZ:** correct the text to match the calculation (flat10 at 1250 PgC, not 1.25 × TCRE).
* **SCM comparisons:** the SCM ensembles have no 1pctCO2 ZEC90 (only ZEC50 and ZEC100). This is left as published
  in the narrow corrigendum.

## Branches and PRs

| Branch | Content |
| --- | --- |
| `main` | **Current.** Contains the corrected code (PR #15) and the `corrigendum` release |
| `flat10-corrigendum-light` | Branch of PR #15 (merged); reused for follow-up changes |
| `flat10-corrigendum-full` | Fuller alternative: all temperatures on a regression-estimated pre-industrial baseline and every wording fix. Kept for reference. |
| `flat10-corrigendum-esm-metrics` | PR #14, superseded by #15; can be closed |
| `claude/laughing-cray-2vabfq` | Stale original working branch; can be deleted |

## How to reproduce

* **Metrics:** `python flat10_esm_metrics.py` prints the legacy (published) and corrected tables and writes
  `esm_metrics_flat10_corrected.csv`. It needs numpy, pandas, xarray and netCDF4.
* **Figures:** run `flat10_figures_paper.ipynb` end to end. It was last run with Python 3.11, numpy 1.26, pandas 2.1.4,
  xarray 2024.3.0, matplotlib 3.9.2, scipy < 1.14 and seaborn; newer pandas/numpy break it, as do older matplotlib
  versions (`violinplot(side=...)`). Figures in the corrigendum:
  * Fig. 7: `images/flat10_zec_tcre_comparison.*`
  * Fig. 8: `images/flat10_SCM_ESM_metric_correlations.*`
  * Fig. 13: `images/flat10_metric_pairplot.*`
* **Word files:** `corrigendum/docx_build/build.sh`. See the README there.
* **Distribution analysis:** `python corrigendum/distribution_shifts.py` (needs matplotlib).

## Open items

1. Co-authors have seen the corrigendum; no further comments as of 2026-10-28.
2. Send the reply to Roland, if not already done.
3. Email the GMD editorial office, then submit the corrigendum.
4. Close PR #14 and delete the stale `claude/laughing-cray-2vabfq` branch.

## Known caveats

* tPW from a single member is sensitive to smoothing: 20-year instead of 11-year smoothing moves individual values by
  up to 6 years. The corrigendum text mentions this.
* `output/temperatures_flat10.csv` in the repository is stale relative to the current code and was deliberately left
  unchanged.
* Earlier messages and the superseded full-version materials refer to "all 7 models with ZECMIP values"; it is
  8 (including UVic). The corrigendum uses the five same-version models (41 %) and is unaffected.
