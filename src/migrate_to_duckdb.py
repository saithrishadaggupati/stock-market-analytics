import duckdb
import sqlite3
import pandas as pd

print('Reading from SQLite...')
sqlite_conn = sqlite3.connect('stock_market.db')
df = pd.read_sql('SELECT * FROM stock_prices', sqlite_conn)
sqlite_conn.close()
print(f'Loaded {len(df)} rows from SQLite')

sector_map = {
    'RELIANCE.NS': 'Energy', 'TCS.NS': 'IT', 'INFY.NS': 'IT',
    'HDFCBANK.NS': 'Banking', 'ICICIBANK.NS': 'Banking',
    'SBIN.NS': 'Banking', 'WIPRO.NS': 'IT', 'HCLTECH.NS': 'IT',
    'AAPL': 'Tech', 'MSFT': 'Tech', 'GOOGL': 'Tech',
    'AMZN': 'Tech', 'META': 'Tech', 'NVDA': 'Tech',
    'TSLA': 'EV', 'AMD': 'Tech', 'NFLX': 'Media'
}
df['Sector'] = df['Stock'].map(sector_map).fillna('Other')
df['Country'] = df['Stock'].apply(lambda x: 'India' if '.NS' in x else 'US')
df['Date'] = pd.to_datetime(df['Date'])

print('Creating DuckDB database...')
duck = duckdb.connect('stock_market_duckdb.db')

duck.execute('DROP TABLE IF EXISTS fact_stock_prices')
duck.execute('''
    CREATE TABLE fact_stock_prices AS
    SELECT ROW_NUMBER() OVER () AS fact_id,
        Date AS date, Stock AS ticker, Sector AS sector,
        Country AS country, Open AS open, High AS high,
        Low AS low, Close AS close, Volume AS volume
    FROM df
''')
print(f'fact_stock_prices: {duck.execute("SELECT COUNT(*) FROM fact_stock_prices").fetchone()[0]} rows')

duck.execute('DROP TABLE IF EXISTS dim_stock')
duck.execute('''
    CREATE TABLE dim_stock AS
    SELECT ROW_NUMBER() OVER () AS stock_id, ticker, sector, country
    FROM (SELECT DISTINCT ticker, sector, country FROM fact_stock_prices)
''')
print(f'dim_stock: {duck.execute("SELECT COUNT(*) FROM dim_stock").fetchone()[0]} stocks')

duck.execute('DROP TABLE IF EXISTS dim_date')
duck.execute('''
    CREATE TABLE dim_date AS
    SELECT ROW_NUMBER() OVER () AS date_id, date,
        EXTRACT(DAY FROM date) AS day,
        EXTRACT(MONTH FROM date) AS month,
        EXTRACT(QUARTER FROM date) AS quarter,
        EXTRACT(YEAR FROM date) AS year,
        DAYNAME(date) AS day_name,
        MONTHNAME(date) AS month_name
    FROM (SELECT DISTINCT date FROM fact_stock_prices ORDER BY date)
''')
print(f'dim_date: {duck.execute("SELECT COUNT(*) FROM dim_date").fetchone()[0]} dates')

duck.execute('DROP VIEW IF EXISTS vw_moving_averages')
duck.execute('''
    CREATE VIEW vw_moving_averages AS
    SELECT date, ticker, close,
        ROUND(AVG(close) OVER (PARTITION BY ticker ORDER BY date ROWS 6 PRECEDING), 2) AS ma_7,
        ROUND(AVG(close) OVER (PARTITION BY ticker ORDER BY date ROWS 29 PRECEDING), 2) AS ma_30
    FROM fact_stock_prices
''')

duck.execute('DROP VIEW IF EXISTS vw_sector_performance')
duck.execute('''
    CREATE VIEW vw_sector_performance AS
    SELECT sector,
        ROUND(AVG(close), 2) AS avg_price,
        ROUND(STDDEV(close), 2) AS volatility,
        COUNT(DISTINCT ticker) AS num_stocks
    FROM fact_stock_prices
    GROUP BY sector
''')

duck.execute('DROP VIEW IF EXISTS vw_volume_spikes')
duck.execute('''
    CREATE VIEW vw_volume_spikes AS
    SELECT date, ticker, volume,
        ROUND(AVG(volume) OVER (PARTITION BY ticker), 0) AS avg_volume,
        ROUND(volume / AVG(volume) OVER (PARTITION BY ticker), 2) AS volume_ratio
    FROM fact_stock_prices
    WHERE volume > 0
    ORDER BY volume_ratio DESC
''')

print('All views created!')
duck.close()
print('DuckDB migration complete!')