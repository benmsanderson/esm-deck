# Word versions of the paper

`build.sh` regenerates two Word files from the GMD article XML (`gmd-18-5699-2025.xml`, CC BY 4.0):

* `out/flat10MIP_GMD2025_published.docx`: a straight conversion of the published article (single column, A4,
  Table 2 on a landscape page).
* `out/flat10MIP_GMD2025_corrigendum_tracked.docx`: the same document with the corrigendum applied as Word tracked
  changes (author "flat10MIP corrigendum"). The changes are the six text edits, the Table 2 values, caption and
  footnote, and the replacement of Figs. 7, 8 and 13. Accept all changes to get a clean corrected copy.

How it works:

| File | Role |
|---|---|
| `prep.py` | Prepares the XML for pandoc: local figure paths, OASIS tables converted to JATS tables, front matter, appendix, references, and visible section, figure and table numbers |
| `post.py` | A4 pages, compact full-width tables, Table 2 on a landscape page |
| `track.py` | Helpers that turn a text replacement into a phrase-level tracked change, leaving equations untouched |
| `apply_corrigendum.py` | The corrigendum itself: the text edits, Table 2 cells (from `esm_metrics_flat10_corrected.csv`) and figure swaps |

Notes:

* The published figures come from the article PDF, which `build.sh` downloads; the replacement figures come from
  `images/` in this repository.
* Equations are native Word equations. They display in Word, but LibreOffice without its maths module shows them blank.
* Each edit in `apply_corrigendum.py` quotes the converted text exactly; `track.py` raises an error if a quoted
  passage is not found once, or if an edit would delete an equation.
