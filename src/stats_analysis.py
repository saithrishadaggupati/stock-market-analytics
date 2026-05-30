# I built this to go beyond just price charts.
# Wanted to answer 3 real questions:
# 1. Which stocks are the riskiest?
# 2. Do Indian and US stocks move together or independently?
# 3. Were there any unusual days in the data worth flagging?

import pandas as pd
import numpy as np

def run_stats_analysis():

    print("Loading data...")
    df = pd.read_csv("data/stocks_clean.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Stock", "Date"])
    print(f"Loaded {len(df)} rows across {df['Stock'].nunique()} stocks")

    # Daily return tells me how much a stock moved each day
    # Simple but powerful — this is what all risk metrics are built on
    df["Daily_Return"] = df.groupby("Stock")["Close"].pct_change() * 100

    # ----------------------------------------
    # QUESTION 1 — Which stocks are riskiest?
    # I used standard deviation of daily returns
    # High std dev = price jumps around a lot = risky
    # ----------------------------------------
    volatility = df.groupby("Stock")["Daily_Return"].std().round(3).reset_index()
    volatility.columns = ["Stock", "Volatility_Pct"]
    volatility = volatility.sort_values("Volatility_Pct", ascending=False)

    print("\n--- Volatility Ranking ---")
    print(volatility)
    volatility.to_csv("data/stats_volatility.csv", index=False)

    # ----------------------------------------
    # QUESTION 2 — Do stocks move together?
    # Correlation matrix shows this clearly
    # 1.0 = move exactly together, 0 = no relation
    # Useful for understanding market patterns
    # ----------------------------------------
    pivot = df.pivot_table(
        index="Date",
        columns="Stock",
        values="Close"
    )
    correlation = pivot.corr().round(3)

    print("\n--- Correlation Matrix (sample) ---")
    print(correlation.iloc[:5, :5])
    correlation.to_csv("data/stats_correlation.csv")

    # ----------------------------------------
    # QUESTION 3 — Any unusual days worth flagging?
    # I used Z-score to find outliers
    # If a stock moved more than 2 standard deviations
    # from its average — that day is flagged as unusual
    # Could be earnings, news, market crash etc.
    # ----------------------------------------
    mean_return = df.groupby("Stock")["Daily_Return"].transform("mean")
    std_return = df.groupby("Stock")["Daily_Return"].transform("std")
    df["Z_Score"] = (df["Daily_Return"] - mean_return) / std_return

    outliers = df[df["Z_Score"].abs() > 2].copy()
    outliers = outliers[["Date", "Stock", "Close", "Daily_Return", "Z_Score"]]
    outliers = outliers.sort_values("Z_Score", key=abs, ascending=False)

    print("\n--- Top 10 Unusual Trading Days ---")
    print(outliers.head(10))
    outliers.to_csv("data/stats_outliers.csv", index=False)

    # ----------------------------------------
    # Summary — one table with everything
    # Mean return, volatility, best day, worst day
    # ----------------------------------------
    summary = df.groupby("Stock")["Daily_Return"].agg([
        ("Avg_Daily_Return", "mean"),
        ("Volatility", "std"),
        ("Worst_Day", "min"),
        ("Best_Day", "max")
    ]).round(3).reset_index()

    summary = summary.sort_values("Avg_Daily_Return", ascending=False)

    print("\n--- Summary Stats Per Stock ---")
    print(summary)
    summary.to_csv("data/stats_summary.csv", index=False)

    print("\nDone. All stats exported.")

run_stats_analysis()