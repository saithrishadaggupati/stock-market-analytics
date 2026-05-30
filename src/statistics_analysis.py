# ============================================
# STOCK RISK & CORRELATION ANALYSIS
# What makes a stock worth holding?
# ============================================
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres123@localhost:5432/stock_db")

df = pd.read_sql("SELECT * FROM fact_stock_prices", engine)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(['ticker', 'date'])

# Daily returns
df['daily_return'] = df.groupby('ticker')['close'].pct_change()

# ============================================
# Q1: Which stocks are riskiest?
# ============================================
volatility = df.groupby('ticker')['daily_return'].std() * np.sqrt(252)
volatility = volatility.sort_values(ascending=False).reset_index()
volatility.columns = ['ticker', 'annual_volatility']
print("\n🔥 Riskiest Stocks:")
print(volatility.head(5).to_string(index=False))

# ============================================
# Q2: Which stocks move together?
# ============================================
pivot = df.pivot_table(index='date', columns='ticker', values='close')
correlation = pivot.corr()
print("\n📊 Most correlated US Tech stocks:")
us_tech = ['AAPL','MSFT','GOOGL','META','AMZN','NVDA']
print(correlation.loc[us_tech, us_tech].round(2))

# ============================================
# Q3: Most stable Indian stocks?
# ============================================
indian = df[df['ticker'].str.contains('.NS')]
stability = indian.groupby('ticker')['daily_return'].std().sort_values()
print("\n🛡️ Most Stable Indian Stocks:")
print(stability.head(5).round(4).to_string())

# ============================================
# SAVE RESULTS TO POSTGRESQL
# ============================================
volatility.to_sql("stock_volatility", engine, if_exists="replace", index=False)
print("\n✅ Volatility data saved to PostgreSQL!")