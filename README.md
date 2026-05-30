# Stock Market Analytics — BI Dashboard

[

![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen)

](https://stock-market-analytics-ftic57gndb94woiigwukue.streamlit.app/)


![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=flat&logo=powerbi&logoColor=black)




![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)




![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)





![Dashboard Preview](dashboard_preview.png)



---

I got tired of seeing stock charts that just show prices going up and down
without actually telling you anything useful.

So I built this — a proper BI pipeline that pulls 3 years of data
across 25 Indian and US stocks, models it into a star schema,
and answers the questions a portfolio manager actually cares about.

Which stocks are too risky? Which sectors quietly outperformed?
Is Indian banking really safer than US tech?

Now I know. And so can you.

---

## What I found

- TSLA and AMD are the riskiest — 57% and 55% annual volatility
- AMZN and NVDA move almost identically — 0.94 correlation
- Holding META is basically holding AMZN (0.91 correlation)
- ICICI Bank is the most stable stock across all 25
- Indian banking stocks are 4x more stable than US tech
- NVDA grew 426% but carries 47% annual volatility — high risk, high reward

---

## How it works

yFinance API → Python ETL → PostgreSQL (Star Schema) → Power BI

**Data Model:**
- `fact_stock_prices` — 18,000+ rows of daily OHLCV data
- `dim_stock` — company master (sector, country)
- `dim_date` — time intelligence (day, month, quarter, year)

**SQL KPI Views:**
- Daily % price change
- 7-day & 30-day moving averages
- 52-week high/low
- Top gainers & losers
- Sector performance

**DAX Measures:**
- % Price Change
- Price Range
- Volume Intensity

**Analysis:**
- Annual volatility per stock
- Cross-stock correlation matrix
- Risk vs return comparison
- Data quality validation

---

## Power BI Dashboard

### Market Overview


![Market Overview](powerbi_market_overview.png)



### Stock Deep Dive


![Stock Deep Dive](powerbi_stock_deepdive.png)



### Sector Analysis


![Sector Analysis](powerbi_sector_analysis.png)



---

## Built with

Python · Pandas · yFinance · PostgreSQL · SQLAlchemy · Power BI · DAX · Star Schema · Streamlit · Plotly

---

## Run it

```bash
git clone https://github.com/saithrishadaggupati/stock-market-analytics
pip install -r requirements.txt
python src/fetch_stock.py
python src/star_schema.py
python src/kpi_queries.py
python src/data_quality.py
python src/statistics_analysis.py
streamlit run dashboard/app.py
# Open stock_market_bi.pbix in Power BI Desktop