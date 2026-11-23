# Does appreciation of the Swiss franc affect Swiss gold exports?

**Course:** Empirical Research in Management and Economics, HEC Lausanne (group project of six, June 2026, graded 5.5/6).

## Contents
- `paper_chf_gold_exports.pdf`: the 26-page paper.
- `chf_gold_exports.py`: the full pipeline, exported from the original Google Colab notebook (data build, panel models, robustness checks, figures).

## Data and method
- **Data:** monthly bilateral Swiss gold exports (Swiss Impex) for 13 partner countries, 2012-2025, combined with Swiss National Bank exchange rates, the gold price and the VIX.
- **Model:** country-month fixed-effects panel regressions (`linearmodels.PanelOLS`), with stress-period interactions and macroeconomic controls.

## Findings
- **Exchange-rate elasticity of β = +0.55 (p < 0.01):** a 1% appreciation of the Swiss franc is associated with a 0.55% *increase* in bilateral gold exports. This is consistent with a safe-haven co-movement rather than the price-competitiveness channel.
- **Stress episodes:** the effect more than doubles during COVID-19 and the Russia-Ukraine war (β = +1.16, against +0.48 in normal periods).
- **Limits:** with country-level macroeconomic controls the coefficient becomes insignificant, which limits a causal reading.

## Run
The script was written for Google Colab and reads data from Google Drive (`/content/drive/MyDrive/recherche_empirique/data`).
To run it locally, replace the Colab `drive.mount` cell and point `BASE` to a local data folder.
```bash
pip install pandas numpy linearmodels yfinance matplotlib seaborn openpyxl
```
