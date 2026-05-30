import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:postgres123@localhost:5432/stock_db")

# ============================================
# KPI 1 — DAILY % PRICE CHANGE
# ============================================
kpi1 = """
CREATE OR REPLACE VIEW vw_daily_change AS
SELECT
    date, ticker, sector, country,
    close,
    LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS prev_close,
    ROUND(
        ((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date))
        / LAG(close) OVER (PARTITION BY ticker ORDER BY date) * 100)::numeric, 2
    ) AS pct_change
FROM fact_stock_prices
ORDER BY ticker, date;
"""

# ============================================
# KPI 2 — 7 & 30 DAY MOVING AVERAGE
# ============================================
kpi2 = """
CREATE OR REPLACE VIEW vw_moving_averages AS
SELECT
    date, ticker, sector, country, close,
    ROUND(AVG(close) OVER (
        PARTITION BY ticker ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ma_7day,
    ROUND(AVG(close) OVER (
        PARTITION BY ticker ORDER BY date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    )::numeric, 2) AS ma_30day
FROM fact_stock_prices
ORDER BY ticker, date;
"""

# ============================================
# KPI 3 — 52 WEEK HIGH/LOW
# ============================================
kpi3 = """
CREATE OR REPLACE VIEW vw_52week_highlow AS
SELECT
    ticker, sector, country,
    ROUND(MAX(high)::numeric, 2) AS week52_high,
    ROUND(MIN(low)::numeric, 2)  AS week52_low,
    ROUND(AVG(volume)::numeric, 0) AS avg_volume
FROM fact_stock_prices
WHERE date >= CURRENT_DATE - INTERVAL '52 weeks'
GROUP BY ticker, sector, country
ORDER BY ticker;
"""

# ============================================
# KPI 4 — TOP GAINERS & LOSERS (LAST 30 DAYS)
# ============================================
kpi4 = """
CREATE OR REPLACE VIEW vw_gainers_losers AS
WITH latest AS (
    SELECT ticker, sector, country, close,
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) AS rn
    FROM fact_stock_prices
),
month_ago AS (
    SELECT ticker, close,
           ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY date DESC) AS rn
    FROM fact_stock_prices
    WHERE date <= CURRENT_DATE - INTERVAL '30 days'
)
SELECT
    l.ticker, l.sector, l.country,
    ROUND(l.close::numeric, 2) AS current_price,
    ROUND(m.close::numeric, 2) AS price_30d_ago,
    ROUND(((l.close - m.close) / m.close * 100)::numeric, 2) AS pct_change_30d
FROM latest l
JOIN month_ago m ON l.ticker = m.ticker AND m.rn = 1
WHERE l.rn = 1
ORDER BY pct_change_30d DESC;
"""

# ============================================
# KPI 5 — SECTOR PERFORMANCE
# ============================================
kpi5 = """
CREATE OR REPLACE VIEW vw_sector_performance AS
SELECT
    sector, country,
    ROUND(AVG(close)::numeric, 2)   AS avg_price,
    ROUND(MAX(high)::numeric, 2)    AS sector_high,
    ROUND(MIN(low)::numeric, 2)     AS sector_low,
    ROUND(AVG(volume)::numeric, 0)  AS avg_volume
FROM fact_stock_prices
GROUP BY sector, country
ORDER BY sector;
"""

# RUN ALL
with engine.connect() as conn:
    conn.execute(text(kpi1))
    print("✅ KPI 1: Daily % Change view created!")
    conn.execute(text(kpi2))
    print("✅ KPI 2: Moving Averages view created!")
    conn.execute(text(kpi3))
    print("✅ KPI 3: 52 Week High/Low view created!")
    conn.execute(text(kpi4))
    print("✅ KPI 4: Gainers & Losers view created!")
    conn.execute(text(kpi5))
    print("✅ KPI 5: Sector Performance view created!")
    conn.commit()

print("\n🎉 All KPI views created in PostgreSQL!")