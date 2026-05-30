# Stock Market Analytics — BI Dashboard



![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=flat&logo=powerbi&logoColor=black)




![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)




![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)





![Dashboard Preview](dashboard_preview.png)



---

Wanted to understand how Indian and US markets really compare —
so I built a proper BI pipeline to find out.

Modeled 25 stocks across 3 years into a star schema,
wrote SQL KPI views, and built a 3-page Power BI dashboard
that answers real business questions — not just pretty charts.

---

## Business Questions Answered

- Which sectors delivered the best returns over 3 years?
- How do Indian banking stocks compare to US Tech in stability?
- Which stocks are top gainers/losers in the last 30 days?
- What does the 52-week high/low tell us about market risk?

---

## Architecture

yFinance API → Python ETL → PostgreSQL (Star Schema) → Power BI

**Data Model:**
- `fact_stock_prices` — 18,000+ rows of daily OHLCV data
- `dim_stock` — company master (sector, country)
- `dim_date` — time intelligence (day, month, quarter, year)

**KPI Views (SQL):**
- Daily % price change
- 7-day & 30-day moving averages
- 52-week high/low
- Top gainers & losers
- Sector performance

---

## Dashboard Pages

- **Market Overview** — KPI cards, price trends, top gainers/losers
- **Stock Deep Dive** — per-stock analysis with moving averages and volume
- **Sector Analysis** — India vs US sector comparison

---

## Key Findings

- NVDA grew 426% in 3 years — best performer overall
- Indian Banking was more stable than US Tech but grew slower
- US Semiconductors was the top performing sector
- TSLA had the highest volatility across all 25 stocks

---

## Tech Stack

Python · Pandas · yFinance · PostgreSQL · SQLAlchemy · Power BI · DAX Measures · Star Schema
---

## Run it

```bash
git clone https://github.com/saithrishadaggupati/stock-market-analytics
pip install -r requirements.txt
python src/fetch_stock.py
python src/star_schema.py
python src/kpi_queries.py
# Open stock_market_bi.pbix in Power BI Desktop