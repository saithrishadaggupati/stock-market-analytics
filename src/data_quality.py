# ============================================
# DATA QUALITY CHECKS — STOCK MARKET DATA
# Before I trust any insight, I need to make
# sure the data itself is actually reliable.
# ============================================
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres123@localhost:5432/stock_db")
df = pd.read_sql("SELECT * FROM fact_stock_prices", engine)

print("=" * 50)
print("Can I trust this data?")
print("=" * 50)

# Missing values — the most common problem
missing = df.isnull().sum()
print("\n🔍 Missing Values:")
if missing.sum() == 0:
    print("   Clean! No missing values found.")
else:
    print(missing[missing > 0])

# Duplicates — same day same stock twice?
dupes = df.duplicated().sum()
print(f"\n🔍 Duplicate Rows: {dupes} found")

# Prices can't be zero or negative
invalid = df[(df['close'] <= 0) | (df['open'] <= 0)].shape[0]
print(f"\n🔍 Invalid Prices: {invalid} rows with zero/negative prices")

# How much history do we actually have?
print(f"\n🔍 Date Coverage:")
print(f"   {df['date'].min()} → {df['date'].max()}")
print(f"   {df['date'].nunique()} unique trading days")

# All 25 stocks present?
print(f"\n🔍 Stock Coverage:")
print(f"   {df['ticker'].nunique()} stocks tracked")
missing_stocks = 25 - df['ticker'].nunique()
if missing_stocks == 0:
    print("   All 25 stocks accounted for!")
else:
    print(f"   ⚠️ {missing_stocks} stocks missing!")

# High should never be lower than low
bad_candles = df[df['high'] < df['low']].shape[0]
print(f"\n🔍 Price Consistency (High > Low): {bad_candles} bad rows")

# Save quality report to PostgreSQL
quality_summary = pd.DataFrame({
    'check': ['missing_values', 'duplicates', 'invalid_prices', 'bad_candles'],
    'result': [int(missing.sum()), int(dupes), int(invalid), int(bad_candles)],
    'status': ['PASS' if x == 0 else 'FAIL' for x in [missing.sum(), dupes, invalid, bad_candles]]
})
quality_summary.to_sql("data_quality_log", engine, if_exists="replace", index=False)
print("\n📋 Quality report saved to PostgreSQL!")

print("\n" + "=" * 50)
print("✅ Data quality check complete!")
print("=" * 50)