# Stock Market Analytics Dashboard

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen)](https://stock-market-analytics-ftic57gndb94woiigwukue.streamlit.app/)

![Dashboard Preview](dashboard_preview.png)

---

I built this to understand how Indian and US stocks behave over time —
not just price charts, but volatility, sector trends, and risk vs return.

3 years of data. 25 stocks. One dashboard.

---

## What I found

- NVDA grew 426% in 3 years. TSLA was the most volatile.
- Indian banking stocks were more stable than US tech — but grew slower.
- ITC.NS lost 33% while every other Indian stock gained.
- US Semiconductors was the best performing sector overall.

---

## Pages

- Market Overview — who grew, who didn't
- Stock Deep Dive — price, moving averages, volume
- Sector Analysis — Indian vs US comparison
- Volatility & Risk — which stocks are risky vs stable
- Key Insights — findings pulled straight from the data

---

## Built with

Python · Pandas · SQL · Plotly · Streamlit · yFinance

---

## Run it

git clone https://github.com/saithrishadaggupati/stock-market-analytics
pip install -r requirements.txt
python src/fetch_stock.py
python src/clean_stock.py
streamlit run dashboard/app.py