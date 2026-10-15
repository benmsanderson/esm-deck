"""
Stand-alone recomputation of the flat10MIP ESM summary metrics
(Sanderson et al., 2025, GMD 18, 5699, Table 2) from the annual-mean tas
files in ESM_data/.

Two versions of each metric are computed:

  legacy     - the method that produced the published Table 2 (flat10_figures.ipynb,
               Aug 2024). All series are offset by the flat10 tas of a single year
               (year 1), while T100yr is referenced to a separate 20/10-year baseline
               (cn0). The two offsets do not cancel in ZEC50/90/100 or TR0, leaving a
               term of single-year variability (up to ~0.2 K) in those metrics.
  corrected  - ZEC = mean(flat10-zec window) - mean(flat10 years 90-109) exactly (no
               baseline term). TR0 is years 300-319 of flat10-cdr relative to esm-piControl,
               estimated as the intercept of a linear fit to flat10 years 0-29.
               tPW uses the centred-window index (the legacy value is 5 years early
               because the 'valid' moving average was not re-centred).

Indexing: years are 0-based from the start of esm-flat10. esm-flat10-zec and
esm-flat10-cdr branch at year 100 and are appended to flat10 years 0-99, so
'years 140-159' means 40-59 years after emissions cease.

Metrics (20-year means unless stated):
  T100yr  flat10 years 90-109 minus cn0, cn0 = 2*mean(yrs 0-19) - mean(yrs 10-29)
  ZEC50   flat10-zec years 140-159 minus flat10 years 90-109
  ZEC90   flat10-zec years 180-199 minus flat10 years 90-109
  ZEC100  flat10-zec years 190-209 minus flat10 years 90-109
  tPW     year of peak 11-yr running-mean tas in flat10-cdr minus 150
  TNZ     flat10-cdr years 140-159 minus flat10 years 115-134
  TR1000  flat10-cdr years 190-209 minus flat10 years 90-109
  TR0     legacy: flat10-cdr years 290-309 minus T(yr 1)
          corrected: flat10-cdr years 300-319 minus the regression intercept. Runs that end
          in year 299 use years 290-299 minus T100yr x 45 PgC, the mean cumulative emissions
          remaining in that window (tested on the 7 full-length runs: bias 0.00 K, RMSE 0.07 K)

Usage:  python flat10_esm_metrics.py [path/to/esm-deck]
Writes esm_metrics_flat10_corrected.csv next to ESM_data/ and prints both tables.
Requires numpy, pandas, scipy, xarray, netCDF4.
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd
import xarray as xr
from scipy.stats import linregress

warnings.filterwarnings("ignore")

MODELS = ['ACCESS-ESM1-5', 'CESM2', 'GFDL-ESM4', 'GISS', 'NorESM2-LM', 'MPI-ESM1-2-LR',
          'CNRM-ESM2-1', 'UKESM', 'UVic-ESCM-2-10', 'HadCM3LC-Bris']
RENAME = {'TAS_GLOB': 'tas', 'temp_mm_1_5m': 'tas', '__xarray_dataarray_variable__': 'tas'}
WINDOW = 11
# mean cumulative emissions (PgC) at the end of esm-flat10-cdr years 290-299: 90, 80, ..., 0
CUM_290_299 = 45.0


def _open(path):
    ds = xr.open_dataset(path)
    for k, v in RENAME.items():
        if k in ds:
            ds = ds.rename_vars({k: v})
    for t in ['TIME', 't']:
        if t in ds.coords:
            ds = ds.swap_dims({t: 'time'}).rename_vars({t: 'time'})
    tas = ds['tas'].isel(time=slice(0, 4800))
    # monthly files are averaged to annual means; annual files pass through
    if tas.sizes['time'] >= 1000:
        tas = tas.coarsen(time=12, boundary='trim').mean()
    tas = tas.squeeze(drop=True)
    while tas.ndim > 1:
        d = [x for x in tas.dims if x != 'time'][0]
        tas = tas.isel({d: 0}, drop=True)
    return np.asarray(tas.values, dtype=float)


def load(root, model):
    """Annual tas for flat10, and flat10-zec / flat10-cdr appended to flat10 years 0-99."""
    p = os.path.join(root, 'ESM_data', model)
    f10 = _open(f'{p}/flat10_tas_{model}.nc')
    out = {'flat10': f10}
    for e in ['flat10-zec', 'flat10-cdr']:
        fn = f'{p}/{e}_tas_{model}.nc'
        out[e] = np.concatenate([f10[:100], _open(fn)]) if os.path.exists(fn) else None
    return out


def wmean(x, a, b):
    # windows truncated by a short run are kept if at least 10 years remain
    # (legacy TR0 for CESM2, GISS and UKESM, whose flat10-cdr runs end at year 299)
    if x is None or len(x) < a + 10:
        return np.nan
    return x[a:b].mean()


def metrics(ts, legacy):
    f, z, c = ts['flat10'], ts['flat10-zec'], ts['flat10-cdr']
    cn0 = 2 * f[:20].mean() - f[10:30].mean()
    # legacy: zec/cdr series referenced to flat10 year 1; corrected: to cn0
    ref = f[1] if legacy else cn0
    t100 = wmean(f, 90, 110) - cn0
    m = {'T100yr': t100}
    for name, (a, b) in {'ZEC50': (140, 160), 'ZEC90': (180, 200), 'ZEC100': (190, 210)}.items():
        m[name] = wmean(z, a, b) - ref - t100
    if c is not None:
        ma = np.convolve(c, np.ones(WINDOW), 'valid') / WINDOW
        m['tPW'] = int(np.argmax(ma)) + (0 if legacy else WINDOW // 2) - 150
    else:
        m['tPW'] = np.nan
    m['TNZ'] = wmean(c, 140, 160) - wmean(f, 115, 135)
    m['TR1000'] = wmean(c, 190, 210) - wmean(f, 90, 110)
    if legacy:
        m['TR0'] = wmean(c, 290, 310) - ref
    else:
        pi = linregress(np.arange(30), f[:30]).intercept
        if c is None or len(c) < 300:
            m['TR0'] = np.nan
        elif len(c) >= 320:
            m['TR0'] = c[300:320].mean() - pi
        else:
            m['TR0'] = c[290:300].mean() - pi - t100 * CUM_290_299 / 1000
    return m


def main(root='.'):
    ts = {m: load(root, m) for m in MODELS}
    legacy = pd.DataFrame({m: metrics(ts[m], True) for m in MODELS}).T
    corrected = pd.DataFrame({m: metrics(ts[m], False) for m in MODELS}).T
    pd.set_option('display.width', 200)
    print('Legacy method (as published in Table 2):')
    print(legacy.round(2).to_string())
    print('\nCorrected (common baseline):')
    print(corrected.round(2).to_string())
    corrected.index.name = 'model'
    corrected.to_csv(os.path.join(root, 'esm_metrics_flat10_corrected.csv'), float_format='%.3f')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
