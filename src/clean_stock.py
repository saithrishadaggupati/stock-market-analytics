import pandas as pd

print("Loading raw stock dataset...")

df = pd.read_csv("data/stocks.csv")

df.reset_index(inplace=True)

df = df[["Date", "Open", "High", "Low", "Close", "Volume", "Stock", "Sector"]]

# Remove missing values
before = len(df)
df.dropna(inplace=True)
dropped = before - len(df)
print(f"Removed {dropped} rows with missing values")

# Fix data types
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Volume"].astype(int)
df["Close"] = df["Close"].round(2)
df["Open"] = df["Open"].round(2)
df["High"] = df["High"].round(2)
df["Low"] = df["Low"].round(2)

# Add daily return column
df = df.sort_values(["Stock", "Date"])
df["Daily_Return"] = df.groupby("Stock")["Close"].pct_change().round(4)

# Add 20-day and 50-day moving averages
df["MA_20"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(20).mean()).round(2)
df["MA_50"] = df.groupby("Stock")["Close"].transform(lambda x: x.rolling(50).mean()).round(2)

# Remove rows with NaN from moving averages
df.dropna(inplace=True)

df.to_csv("data/stocks_clean.csv", index=False)

print(f"Dataset cleaned successfully — {len(df)} rows ready")
print(f"Stocks: {df['Stock'].nunique()} | Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print("Saved to: data/stocks_clean.csv")