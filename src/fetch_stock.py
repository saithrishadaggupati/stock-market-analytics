# Fetch real stock market data

import yfinance as yf
import pandas as pd


# Stocks we will track
STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "AAPL", "GOOGL"]


def fetch_stock_data():

    print("Starting stock data download...\n")

    # Empty list to store stock data
    all_data = []

    # Loop through each stock
    for stock in STOCKS:

        print(f"Fetching data for {stock}...")

        # Download stock data
        df = yf.download(
            stock,
            period="90d",
            auto_adjust=False
        )

        # Fix multi-level columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Convert index into normal column
        df.reset_index(inplace=True)

        # Print columns for debugging
        print(df.columns)

        # Rename first column to Date
        df.rename(columns={df.columns[0]: "Date"}, inplace=True)

        # Keep only required columns
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

        # Add to list
        all_data.append(df)

    # Combine all stock data
    combined = pd.concat(all_data, ignore_index=True)

    # Save dataset
    combined.to_csv("data/stocks.csv", index=False)

    print("\n===================================")
    print("Stock data downloaded successfully!")
    print("File saved to: data/stocks.csv")
    print("===================================")


# Run function
fetch_stock_data()