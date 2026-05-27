# ============================================
# FETCH REAL STOCK MARKET DATA
# ============================================

import yfinance as yf
import pandas as pd

# ============================================
# STOCK LIST
# ============================================

STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "META",
    "TSLA"
]

# ============================================
# FETCH FUNCTION
# ============================================

def fetch_stock_data():

    print("Starting stock data download...\n")

    # Empty list to store stock data
    all_data = []

    # Loop through each stock
    for stock in STOCKS:

        print(f"Fetching data for {stock}...")

        try:

            # Download stock data
            df = yf.download(
                stock,
                period="90d",
                auto_adjust=False
            )

            # Skip empty datasets
            if df.empty:
                print(f"No data found for {stock}")
                continue

            # Fix multi-level columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Convert index into normal column
            df.reset_index(inplace=True)

            # Rename first column to Date
            df.rename(
                columns={df.columns[0]: "Date"},
                inplace=True
            )

            # Keep required columns only
            df = df[
                [
                    "Date",
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume"
                ]
            ]

            # Add stock name
            df["Stock"] = stock

            # Add dataframe to list
            all_data.append(df)

            print(f"{stock} data downloaded successfully!\n")

        except Exception as e:

            print(f"Error downloading {stock}: {e}")

    # ============================================
    # COMBINE ALL STOCKS
    # ============================================

    combined = pd.concat(
        all_data,
        ignore_index=True
    )

    # ============================================
    # SAVE DATASET
    # ============================================

    combined.to_csv(
        "data/stocks.csv",
        index=False
    )

    print("\n===================================")
    print("All stock data downloaded successfully!")
    print("Dataset saved to: data/stocks.csv")
    print("===================================")


# ============================================
# RUN FUNCTION
# ============================================

fetch_stock_data()