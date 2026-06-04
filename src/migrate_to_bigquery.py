import duckdb
import pandas as pd

# ── instructions ───────────────────────────────────────────────────────────────
# To run this migration:
#   1. pip install google-cloud-bigquery pandas-gbq
#   2. Create a GCP project and enable the BigQuery API
#   3. Create a dataset named "stock_analytics" in BigQuery
#   4. Run: gcloud auth application-default login
#   5. Set PROJECT_ID below and run this script

PROJECT_ID = "your-gcp-project-id"   # ← replace before running
DATASET    = "stock_analytics"

# ── read from DuckDB ───────────────────────────────────────────────────────────
print("Reading from DuckDB...")
conn = duckdb.connect("stock_market_duckdb.db", read_only=True)

fact_df = conn.execute("""
    SELECT
        fact_id,
        CAST(date AS DATE)  AS date,
        ticker,
        sector,
        country,
        open,
        high,
        low,
        close,
        volume,
        ROUND((close - open) / NULLIF(open, 0) * 100, 4)   AS daily_pct_change,
        ROUND(close - open, 4)                              AS daily_price_change,
        ROUND(high - low, 4)                                AS daily_range
    FROM fact_stock_prices
""").df()

dim_df = conn.execute("""
    SELECT
        stock_id,
        ticker,
        sector,
        country,
        CASE WHEN country = 'India' THEN 'Indian Market'
             ELSE 'US Market' END AS market
    FROM dim_stock
""").df()

conn.close()
print(f"  fact_stock_prices : {len(fact_df):,} rows")
print(f"  dim_stock         : {len(dim_df):,} rows")

# ── BigQuery schema definitions ────────────────────────────────────────────────
FACT_SCHEMA = [
    {"name": "fact_id",             "type": "INTEGER"},
    {"name": "date",                "type": "DATE"},
    {"name": "ticker",              "type": "STRING"},
    {"name": "sector",              "type": "STRING"},
    {"name": "country",             "type": "STRING"},
    {"name": "open",                "type": "FLOAT"},
    {"name": "high",                "type": "FLOAT"},
    {"name": "low",                 "type": "FLOAT"},
    {"name": "close",               "type": "FLOAT"},
    {"name": "volume",              "type": "INTEGER"},
    {"name": "daily_pct_change",    "type": "FLOAT"},
    {"name": "daily_price_change",  "type": "FLOAT"},
    {"name": "daily_range",         "type": "FLOAT"},
]

DIM_SCHEMA = [
    {"name": "stock_id",  "type": "INTEGER"},
    {"name": "ticker",    "type": "STRING"},
    {"name": "sector",    "type": "STRING"},
    {"name": "country",   "type": "STRING"},
    {"name": "market",    "type": "STRING"},
]

# ── upload to BigQuery ─────────────────────────────────────────────────────────
try:
    import pandas_gbq

    print("\nUploading to BigQuery...")

    pandas_gbq.to_gbq(
        fact_df,
        destination_table=f"{DATASET}.fact_stock_prices",
        project_id=PROJECT_ID,
        if_exists="replace",
        table_schema=FACT_SCHEMA,
        progress_bar=True,
    )
    print(f"  ✅ {DATASET}.fact_stock_prices uploaded")

    pandas_gbq.to_gbq(
        dim_df,
        destination_table=f"{DATASET}.dim_stock",
        project_id=PROJECT_ID,
        if_exists="replace",
        table_schema=DIM_SCHEMA,
        progress_bar=True,
    )
    print(f"  ✅ {DATASET}.dim_stock uploaded")

    print("\nBigQuery migration complete.")
    print(f"  Project : {PROJECT_ID}")
    print(f"  Dataset : {DATASET}")
    print(f"  Tables  : fact_stock_prices, dim_stock")

except ImportError:
    print("\npandas-gbq not installed.")
    print("Run: pip install google-cloud-bigquery pandas-gbq")
except Exception as e:
    print(f"\nMigration failed: {e}")