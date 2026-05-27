# KPI analysis for stock market data

import pandas as pd


def analyze_kpis():

    print("Loading cleaned stock dataset...")

    # Load cleaned data
    df = pd.read_csv("data/stocks_clean.csv")

    print("Dataset loaded successfully!")

    # -----------------------------------
    # Create Price Change KPI
    # -----------------------------------

    df["Price_Change"] = df["Close"] - df["Open"]

    print("Price Change KPI created!")

    # -----------------------------------
    # Average closing price by stock
    # -----------------------------------

    average_prices = df.groupby("Stock")["Close"].mean()

    print("\nAverage Closing Price:")
    print(average_prices)

    # -----------------------------------
    # Highest trading volume
    # -----------------------------------

    highest_volume = df.groupby("Stock")["Volume"].sum()

    print("\nTotal Trading Volume:")
    print(highest_volume)

    print("\nKPI analysis completed successfully!")


# Run KPI analysis
analyze_kpis()