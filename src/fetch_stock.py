import yfinance as yf
import pandas as pd
import os

STOCKS = {
    "TCS.NS": "Indian IT", "INFY.NS": "Indian IT",
    "WIPRO.NS": "Indian IT", "HCLTECH.NS": "Indian IT",
    "HDFCBANK.NS": "Indian Banking", "ICICIBANK.NS": "Indian Banking",
    "SBIN.NS": "Indian Banking", "AXISBANK.NS": "Indian Banking",
    "RELIANCE.NS": "Indian Energy", "LT.NS": "Indian Industrial",
    "ONGC.NS": "Indian Energy", "ITC.NS": "Indian FMCG",
    "HINDUNILVR.NS": "Indian FMCG", "TITAN.NS": "Indian Consumer",
    "BAJFINANCE.NS": "Indian Finance",
    "AAPL": "US Tech", "MSFT": "US Tech", "GOOGL": "US Tech",
    "META": "US Tech", "AMZN": "US Tech",
    "NVDA": "US Semiconductors", "AMD": "US Semiconductors",
    "TSLA": "US EV", "JPM": "US Banking", "BAC": "US Banking",
}

def fetch_stock_data():
    print("Starting stock data download...\n")
    all_data = []

    for stock, sector in STOCKS.items():
        print(f"Fetching {stock}...")
        try:
            df = yf.download(stock, period="3y", auto_adjust=False)
            if df.empty:
                print(f"No data for {stock}")
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df.reset_index(inplace=True)
            df.rename(columns={df.columns[0]: "Date"}, inplace=True)
            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
            df["Stock"] = stock
            df["Sector"] = sector
            all_data.append(df)
            print(f"{stock} done!")
        except Exception as e:
            print(f"Error: {stock}: {e}")

    combined = pd.concat(all_data, ignore_index=True)
    os.makedirs("data", exist_ok=True)
    combined.to_csv("data/stocks.csv", index=False)
    print("Saved to CSV!")
    print(f"\nTotal rows: {len(combined)}")
    print(f"Total stocks: {combined['Stock'].nunique()}")
    return combined

fetch_stock_data()