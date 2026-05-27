# Stock Market Analytics Dashboard

I wanted a project that combined SQL, Python, and a live 
dashboard — so I built this to track Indian and US stock 
performance in one place.
<img width="1731" height="752" alt="image" src="https://github.com/user-attachments/assets/9898ad01-10fc-4347-99fb-8fdb62c0588a" />

You pick a stock, and it shows you the price history, 
7-day and 30-day moving averages, trading volume, and 
a few KPI cards that give you a quick read on recent 
performance.

## Live App
👉 [Open Dashboard](https://stock-market-analytics-ftic57gndb94woiigwukue.streamlit.app/)

## How it works

**1. Data Collection**
Uses yFinance to pull historical price data for 
Indian and US stocks.

**2. Processing**
Cleans and structures the data with Pandas, then 
loads it into a local SQLite database for 
SQL-based analysis.

**3. Dashboard**
Built with Streamlit and Plotly — pick a stock, 
adjust the date range, and the charts update 
instantly.

## Tech used
Python · Pandas · SQL (SQLite) · Plotly · Streamlit · yFinance

## Run it yourself
git clone https://github.com/saithrishadaggupati/stock-market-analytics
pip install -r requirements.txt
streamlit run dashboard/app.py

## Project structure
stock-market-analytics/
├── dashboard/      # Streamlit app
├── data/           # CSV and cleaned data files
├── src/            # Fetch, clean, analyze, visualize
├── stock_market.db # SQLite database
└── requirements.txt
