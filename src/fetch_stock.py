# ============================================
# FETCH REAL STOCK MARKET DATA
# ============================================
import yfinance as yf
import pandas as pd

# ============================================
# STOCK LIST WITH SECTORS
# ============================================
STOCKS = {
    # --- INDIAN STOCKS ---
    # IT Sector
    "TCS.NS":       "Indian IT",
    "INFY.NS":      "Indian IT",
    "WIPRO.NS":     "Indian IT",
    "HCLTECH.NS":   "Indian IT",

    # Banking Sector
    "HDFCBANK.NS":  "Indian Banking",
    "ICICIBANK.NS": "Indian Banking",
    "SBIN.NS":      "Indian Banking",
    "AXISBANK.NS":  "Indian Banking",

    # Energy & Industrial
    "RELIANCE.NS":  "Indian Energy",
    "LT.NS":        "Indian Industrial",
    "ONGC.NS":      "Indian Energy",

    # Consumer & FMCG
    "ITC.NS":       "Indian FMCG",
    "HINDUNILVR.NS":"Indian FMCG",
    "TITAN.NS":     "Indian Consumer",

    # Finance
    "BAJFINANCE.NS":"Indian Finance",

    # --- US STOCKS ---
    # Big Tech
    "AAPL":         "US Tech",
    "MSFT":         "US Tech",
    "GOOGL":        "US Tech",
    "META":         "US Tech",
    "AMZN":         "US Tech",

    # Semiconductors
    "NVDA":         "US Semiconductors",
    "AMD":          "US Semiconductors",

    # EV & Innovation
    "TSLA":         "US EV",

    # Finance
    "JPM":          "US Banking",
    "BAC":          "US Banking",
}

# ============================================
# FETCH FUNCTION
# ============================================
def fetch_stock_data():
    print("Starting stock data download...\n")

    all_data = []

    for stock, sector in STOCKS.items():
        print(f"Fetching data for {stock}...")
        try:
            df = yf.download(
                stock,
                period="3y",
                auto_adjust=False
            )

            if df.empty:
                print(f"No data found for {stock}")
                continue

            # Fix multi-level columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.reset_index(inplace=True)

            df.rename(
                columns={df.columns[0]: "Date"},
                inplace=True
            )

            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

            # Add stock name and sector
            df["Stock"] = stock
            df["Sector"] = sector

            all_data.append(df)
            print(f"{stock} data downloaded successfully!\n")

        except Exception as e:
            print(f"Error downloading {stock}: {e}")

    # ============================================
    # COMBINE ALL STOCKS
    # ============================================
    combined = pd.concat(all_data, ignore_index=True)

    # ============================================
    # SAVE DATASET
    # ============================================
    combined.to_csv("data/stocks.csv", index=False)

    print("\n===================================")
    print("All stock data downloaded successfully!")
    print(f"Total rows: {len(combined)}")
    print(f"Total stocks: {combined['Stock'].nunique()}")
    print(f"Date range: {combined['Date'].min()} to {combined['Date'].max()}")
    print("Dataset saved to: data/stocks.csv")
    print("===================================")


# ============================================
# RUN FUNCTION
# ============================================
fetch_stock_data()