"""Published vs corrected ESM metrics (Table 2 of Sanderson et al., 2025): ensemble statistics and figure.

Usage: python corrigendum/distribution_shifts.py   (from the repository root)
Writes corrigendum/distribution_shifts.png and prints the statistics quoted in distribution_shifts.md.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = ['ACCESS-ESM1-5', 'CESM2', 'GFDL-ESM4', 'GISS', 'NorESM2-LM', 'MPI-ESM1-2-LR', 'CNRM-ESM2-1', 'UKESM',
          'UVic-ESCM-2-10', 'HadCM3LC-Bris']
LABELS = ['ACCESS', 'CESM2', 'GFDL', 'GISS', 'NorESM2', 'MPI-ESM', 'CNRM', 'UKESM', 'UVic', 'HadCM3LC']
# published Table 2 (ESM rows)
PUB = pd.DataFrame({
    'T100yr': [1.75, 1.95, 1.45, 1.62, 1.18, 1.50, 1.72, 2.50, 1.80, 1.53],
    'ZEC50': [0.21, -0.27, -0.21, 0.19, -0.23, -0.14, -0.01, 0.27, 0.01, -0.02],
    'ZEC90': [0.15, -0.14, -0.13, -0.15, -0.21, -0.17, 0.067, 0.19, -0.11, -0.04],
    'ZEC100': [0.13, -0.13, 0.11, -0.24, -0.31, -0.24, 0.11, 0.20, 0.12, -0.02],
    'tPW': [7, -10, -29, -4, -33, 1, -10, -1, 3, 6],
    'TR0': [0.17, 0.42, -0.11, -0.56, -0.31, -0.29, 0.38, np.nan, 0.25, 0.15]}, index=MODELS)
# ZECMIP (esm-1pct-brch-1000PgC) values from Table 2
ZECMIP = pd.DataFrame({'ZEC50': [0.01, -0.31, np.nan, -0.11, -0.33, -0.27, 0.06, 0.28, 0.04, np.nan],
                       'ZEC90': [-0.03, -0.17, np.nan, -0.06, -0.32, -0.37, 0.25, 0.33, 0.02, np.nan]}, index=MODELS)
SAME_VERSION = ['ACCESS-ESM1-5', 'CESM2', 'NorESM2-LM', 'MPI-ESM1-2-LR', 'CNRM-ESM2-1']


def main():
    cor = pd.read_csv(os.path.join(HERE, '..', 'esm_metrics_flat10_corrected.csv'), index_col=0)[PUB.columns]
    rows = []
    for k in PUB.columns:
        a = PUB[k].dropna(); b = cor.loc[a.index, k]; c = cor[k]
        rows.append(dict(metric=k, pub_mean=a.mean(), cor_mean=c.mean(), pub_median=a.median(), cor_median=c.median(),
                         pub_sd=a.std(), cor_sd=c.std(), pub_min=a.min(), pub_max=a.max(), cor_min=c.min(),
                         cor_max=c.max(), pub_npos=int((a > 0).sum()), cor_npos=int((c > 0).sum()),
                         mean_abs_shift=(b - a).abs().mean(), max_abs_shift=(b - a).abs().max(),
                         sign_changes=int((np.sign(a) != np.sign(b)).sum()), r=np.corrcoef(a, b)[0, 1]))
    pd.set_option('display.width', 200)
    print(pd.DataFrame(rows).set_index('metric').round(3).T.to_string())
    for label, subset in [('5 same-version models', SAME_VERSION), ('all 8 with ZECMIP', list(ZECMIP.dropna().index))]:
        for z in ['ZEC50', 'ZEC90']:
            zm = ZECMIP.loc[subset, z].abs().mean()
            print(f'{label} {z}: mean|ZECMIP| {zm:.3f}, flat10/ZECMIP published {PUB.loc[subset, z].abs().mean() / zm:.2f}'
                  f' -> corrected {cor.loc[subset, z].abs().mean() / zm:.2f}')
    plot(cor, os.path.join(HERE, 'distribution_shifts.png'))


def plot(cor, out):
    blue, grey, muted, ink = '#2a78d6', '#52514e', '#b9b8b3', '#0b0b0b'
    plt.rcParams.update({'font.size': 9, 'axes.edgecolor': muted, 'xtick.color': grey, 'ytick.color': ink})
    metrics = ['ZEC50', 'ZEC90', 'ZEC100', 'tPW', 'TR0']
    units = {'tPW': 'years'}
    fig, axs = plt.subplots(1, 5, figsize=(13, 4.6), sharey=True)
    y = np.arange(len(MODELS))[::-1] + 2
    for ax, k in zip(axs, metrics):
        ax.axvline(0, color=muted, lw=1, zorder=0)
        for yi, m in zip(y, MODELS):
            a, b = PUB.loc[m, k], cor.loc[m, k]
            if not np.isnan(a):
                ax.annotate('', xy=(b, yi), xytext=(a, yi), zorder=1, arrowprops=dict(
                    arrowstyle='-|>', color=muted, lw=1.2, shrinkA=4, shrinkB=4, mutation_scale=8))
                ax.plot(a, yi, 'o', mfc='white', mec=grey, ms=7, mew=1.4, zorder=2)
            ax.plot(b, yi, 'o', color=blue, ms=7, mec='white', mew=1, zorder=3)
        for dy, s, col, mfc in [(0.18, PUB[k], grey, 'white'), (-0.18, cor[k], blue, blue)]:
            ax.errorbar(s.mean(), 0.4 + dy, xerr=s.std(), fmt='s', color=col, mfc=mfc, mec=col, ms=6, capsize=3, lw=1.4)
        ax.axhline(1.2, color=muted, lw=0.6)
        ax.set_title(f'{k} ({units.get(k, "K")})', fontsize=10, loc='left')
        ax.grid(axis='x', color='#ecebe8', lw=0.6); ax.set_axisbelow(True)
        for sp in ['top', 'right']:
            ax.spines[sp].set_visible(False)
    axs[0].set_yticks(list(y) + [0.4]); axs[0].set_yticklabels(LABELS + ['Mean ± 1 s.d.'])
    fig.legend(handles=[Line2D([], [], marker='o', ls='', mfc='white', mec=grey, ms=7, mew=1.4, label='Published'),
                        Line2D([], [], marker='o', ls='', color=blue, ms=7, label='Corrected')],
               loc='upper right', ncol=2, frameon=False, bbox_to_anchor=(0.99, 1.02))
    fig.text(0.01, 0.985, 'ESM metrics in Table 2: published vs corrected', fontsize=11, weight='bold', va='top')
    fig.text(0.01, 0.935, 'Arrows show each model’s shift; squares show the ensemble mean ± 1 s.d. '
             'TR0: UKESM had no published value.', fontsize=8.5, color=grey, va='top')
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(out, dpi=200, facecolor='white')
    print('wrote', out)


if __name__ == '__main__':
    main()
