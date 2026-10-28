#!/usr/bin/env bash
# Rebuild the Word versions of Sanderson et al. (2025, GMD 18, 5699) from the publisher's JATS XML:
#   out/flat10MIP_GMD2025_published.docx            straight conversion of the published article
#   out/flat10MIP_GMD2025_corrigendum_tracked.docx  the same with the corrigendum as tracked changes
# Needs: pandoc (>= 3.1), poppler-utils (pdfimages, pdftoppm), python3 with python-docx and lxml, curl.
# Run from this directory. Accept all changes in Word (or LibreOffice) to get a clean corrected copy.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p work/figs work/newfigs out
PDF=work/gmd-18-5699-2025.pdf
[ -f "$PDF" ] || curl -sSL -o "$PDF" https://gmd.copernicus.org/articles/18/5699/2025/gmd-18-5699-2025.pdf
# published figures: the PDF holds the GMD logo, then Figs. 1-13 as raster images in order
pdfimages -png "$PDF" work/img
for i in $(seq 1 13); do cp "work/img-$(printf %03d "$i").png" "work/figs/fig$(printf %02d "$i").png"; done
# replacement figures (from the corrected notebook output in ../../images)
pdftoppm -png -r 250 -singlefile ../../images/flat10_zec_tcre_comparison.pdf work/newfigs/fig07
pdftoppm -png -r 250 -singlefile ../../images/flat10_SCM_ESM_metric_correlations.pdf work/newfigs/fig08
pdftoppm -png -r 250 -singlefile ../../images/flat10_metric_pairplot.pdf work/newfigs/fig13
python3 prep.py gmd-18-5699-2025.xml work/prepped.xml
(cd work && pandoc -f jats -t docx prepped.xml -o raw.docx)
python3 post.py work/raw.docx out/flat10MIP_GMD2025_published.docx
python3 apply_corrigendum.py out/flat10MIP_GMD2025_published.docx out/flat10MIP_GMD2025_corrigendum_tracked.docx \
    ../../esm_metrics_flat10_corrected.csv work/newfigs
echo "Done: see out/"
