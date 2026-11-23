# Oil-market volatility and U.S. financial-market volatility

**Course:** Financial Econometrics, HEC Lausanne (semester project, group 3, graded 5.0/6).
Also published separately: [UNI-PROJECT-oil-vix-volatility](https://github.com/MUGIWARA95D/UNI-PROJECT-oil-vix-volatility).

**Question:** does oil-market volatility (CBOE OVX) predict U.S. equity-market volatility (VIX) through instantaneous comovement?

## Contents
- `Financial_Econ_groupe_3.pdf`: the written paper.
- `oil_vix_volatility.py`: the full analysis.

## Method
Daily FRED data from 2010 onward. The script builds a panel of about 30 series (oil, volatility, credit spreads, term structure, macro controls, FX, liquidity, uncertainty), then runs:

1. Simple OLS (OVX on VIX);
2. OLS with macro controls;
3. HAC (Newey-West) standard errors for heteroskedasticity and autocorrelation;
4. Control selection through a correlation matrix (collinear regressors dropped);
5. Interaction terms (OVX × stress, dollar, 3-month yield, uncertainty);
6. A quadratic-term test;
7. A PE test selecting a log-linear specification.

**Main finding:** a 1% rise in oil-price volatility is associated with a rise of about 0.69% in market volatility (log-linear, HAC-robust).

## Run
```bash
pip install fredapi pandas statsmodels matplotlib seaborn numpy
export FRED_API_KEY=your_free_key   # https://fred.stlouisfed.org/docs/api/api_key.html
python oil_vix_volatility.py
```
The FRED API key is read from the environment: there are no secrets in the code.
