import sqlite3
import pandas as pd

# Load clean CSV
df = pd.read_csv("data/stocks_clean.csv")

# Fix data types
df['Date'] = df['Date'].astype(str)
df['Open'] = pd.to_numeric(df['Open'], errors='coerce')
df['High'] = pd.to_numeric(df['High'], errors='coerce')
df['Low'] = pd.to_numeric(df['Low'], errors='coerce')
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
df['Stock'] = df['Stock'].astype(str)

# Delete old broken database and rebuild
conn = sqlite3.connect("stock_market.db")
cursor = conn.cursor()

# Drop old broken table
cursor.execute("DROP TABLE IF EXISTS stock_prices")
conn.commit()

# Load clean data into database
df.to_sql("stock_prices", conn, if_exists="replace", index=False)

print("Database rebuilt successfully!")
print(f"Total rows loaded: {len(df)}")

# Verify it worked
result = pd.read_sql("SELECT Stock, COUNT(*) as Days FROM stock_prices GROUP BY Stock", conn)
print("\nStocks in database:")
print(result)

conn.close()