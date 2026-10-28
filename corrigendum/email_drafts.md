# Email drafts

Status unknown at handoff (2026-10-28): it is not recorded whether either draft has been sent. Check with Ben before reusing.

## To co-authors (revised to the current corrigendum scope)

**Subject:** flat10MIP (GMD 2025): errors in ESM ZEC/TR0/tPW and proposed corrigendum

Dear all,

While helping Roland Séférian reproduce our ZEC numbers, I found errors in some of the ESM metrics in Table 2 of the
flat10MIP paper. I've traced them, corrected the code and drafted a short corrigendum for GMD. Before contacting the
editorial office, I'd like you all to look it over, and modelling groups to check their own rows.

**What went wrong**

1. **ZEC and TR0 baselines.** T100yr was referenced to a pre-industrial baseline extrapolated from the first decades
   of esm-flat10, while the zec and cdr runs were referenced to the temperature of a single year (year 1). The offsets
   don't cancel, so the published ESM ZEC50/90/100 and TR0 values contain single-year internal variability of up to
   0.22 K. The corrected ZEC is the plain difference of 20-year means. T100yr is unchanged.
2. **tPW** was reported 5 years too early for every model (uncentred moving average).
3. **Table 2 typos:** three sign errors and a wrong UVic T100yr.

**What it means**

* The finding that ZEC is smaller under flat10 than under ZECMIP gets stronger: about 40 % smaller, not 30 %.
* "Most models peak before net zero" no longer holds (four of ten before, six after); "before or after" stands.
* The multi-model mean ZEC stays near zero; the spread across models narrows by about a quarter, because noise has
  been removed.
* TCRE, TNZ, TR1000, the carbon-cycle results and all SCM results are unaffected.

The corrigendum covers only what readers would otherwise quote or reproduce wrongly:

* Table 2 values, caption and a footnote;
* six text edits;
* replacements for Figs. 7, 8 and 13.

[link to corrigendum draft and the tracked-changes Word version]

**What I need from you**

* **Modelling groups:** please check your model's row in the corrected Table 2, especially CESM2, GFDL-ESM4, GISS
  and NorESM2-LM, whose ZEC values change most, and UVic-ESCM-2-10 and HadCM3LC-Bris. For CESM2, GISS and UKESM1.2,
  TR0 is approximated because the esm-flat10-cdr runs end in year 299.
* **Everyone:** comments by [date].

Code and corrected metrics are in benmsanderson/esm-deck, PR #15. `flat10_esm_metrics.py` reproduces both the
published and corrected values from the global-mean output.

I'm sorry about this, and thanks to Roland for persisting with his questions.

Best,
Ben

## To Roland Séférian (reply to his question on the ZEC calculation)

> Hi Roland,
>
> You've found a real problem, so thank you for persisting. I went back to the exact code version that produced
> Table 2. The ZEC values were computed as
>
> ZEC50 = mean(flat10-zec, yrs 140–159) − [mean(flat10, yrs 90–109) − cn0] − T_flat10(yr 1),
> cn0 = 2·mean(flat10 yrs 0–19) − mean(flat10 yrs 10–29),
>
> (ZEC90/100: zec years 180–199 / 190–209; annual means; zec years indexed from the start of flat10). The baselines
> don't cancel between the two terms, so the published ESM ZEC values contain a residual of single-year variability of
> up to ~0.2 K (CESM2, GFDL, GISS). The clean estimate is simply mean(zec yrs 140–159) − mean(flat10 yrs 90–109),
> which I think is what you've computed. There are also sign typos for GISS ZEC50 and GFDL ZEC100. Corrected values
> are in `esm_metrics_flat10_corrected.csv` in the esm-deck repository, and `flat10_esm_metrics.py` reproduces both.
>
> Cheers,
> -b
