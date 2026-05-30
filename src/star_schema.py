# ============================================
# STAR SCHEMA — STOCK MARKET DATA WAREHOUSE
# Dimensions built from the data itself —
# no hardcoding, no maintenance headaches.
# ============================================
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres123@localhost:5432/stock_db")

# ============================================
# DIM STOCK — pulled from data, not hardcoded
# ============================================
print("Building dim_stock from existing data...")
raw = pd.read_sql('SELECT DISTINCT "Stock", "Sector" FROM stock_prices', engine)

dim_stock = pd.DataFrame({
    "ticker":  raw["Stock"],
    "sector":  raw["Sector"],
    "country": raw["Stock"].apply(lambda x: "India" if ".NS" in x else "US")
})

dim_stock = dim_stock.reset_index(drop=True)
dim_stock.to_sql("dim_stock", engine, if_exists="replace", index=True, index_label="stock_id")
print(f"✅ dim_stock created — {len(dim_stock)} stocks loaded from data!")

# ============================================
# DIM DATE
# ============================================
print("Building dim_date...")
dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="D")
dim_date = pd.DataFrame({
    "date":       dates,
    "day":        dates.day,
    "month":      dates.month,
    "month_name": dates.strftime("%B"),
    "quarter":    dates.quarter,
    "year":       dates.year,
    "week":       dates.isocalendar().week.values,
    "day_name":   dates.strftime("%A"),
    "is_weekend": dates.weekday >= 5
})
dim_date.to_sql("dim_date", engine, if_exists="replace", index=True, index_label="date_id")
print("✅ dim_date created!")

# ============================================
# FACT TABLE
# ============================================

# Drop views first so fact table can be replaced
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text("DROP VIEW IF EXISTS vw_daily_change CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS vw_moving_averages CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS vw_52week_highlow CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS vw_gainers_losers CASCADE"))
    conn.execute(text("DROP VIEW IF EXISTS vw_sector_performance CASCADE"))
    conn.commit()
print("✅ Old views dropped!")

print("Building fact_stock_prices...")



print("Building fact_stock_prices...")
df = pd.read_sql("SELECT * FROM stock_prices", engine)
df["Date"] = pd.to_datetime(df["Date"])
df["country"] = df["Stock"].apply(lambda x: "India" if ".NS" in x else "US")

fact = df[["Date","Stock","Sector","Open","High","Low","Close","Volume","country"]]
fact.columns = ["date","ticker","sector","open","high","low","close","volume","country"]
fact.to_sql("fact_stock_prices", engine, if_exists="replace", index=True, index_label="fact_id")
print(f"✅ fact_stock_prices created — {len(fact)} rows!")

print("\n🎉 Star Schema complete — built from data, not from hardcoding!")