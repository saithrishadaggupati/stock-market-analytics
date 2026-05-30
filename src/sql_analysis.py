# SQL analysis for stock market data

import sqlite3
import pandas as pd


def run_sql_analysis():

    print("Connecting to database...")
    connection = sqlite3.connect("stock_market.db")
    print("Database connected!")

    # ----------------------------
    # QUERY 1 - Basic Summary
    # Average price and total volume per stock
    # ----------------------------
    query1 = """
    SELECT
        Stock,
        ROUND(AVG(Close), 2) AS Average_Close_Price,
        ROUND(MAX(Close), 2) AS Highest_Price,
        ROUND(MIN(Close), 2) AS Lowest_Price,
        SUM(Volume) AS Total_Volume
    FROM stock_prices
    GROUP BY Stock
    ORDER BY Average_Close_Price DESC
    """

    # ----------------------------
    # QUERY 2 - Top 5 Stocks by Volume
    # ----------------------------
    query2 = """
    SELECT
        Stock,
        ROUND(AVG(Volume), 0) AS Avg_Daily_Volume
    FROM stock_prices
    GROUP BY Stock
    ORDER BY Avg_Daily_Volume DESC
    LIMIT 5
    """

    # ----------------------------
    # QUERY 3 - Price Growth %
    # Which stock grew the most?
    # ----------------------------
    query3 = """
    SELECT
        Stock,
        ROUND(MIN(Close), 2) AS Start_Price,
        ROUND(MAX(Close), 2) AS End_Price,
        ROUND(((MAX(Close) - MIN(Close)) / MIN(Close)) * 100, 2) AS Growth_Pct
    FROM stock_prices
    GROUP BY Stock
    ORDER BY Growth_Pct DESC
    """

    # ----------------------------
    # QUERY 4 - Volume Spike Detection
    # Days where volume was 2x the average (abnormal activity)
    # ----------------------------
    query4 = """
    SELECT
        Date,
        Stock,
        Volume,
        ROUND(AVG(Volume) OVER (PARTITION BY Stock), 0) AS Avg_Volume,
        ROUND(Volume / AVG(Volume) OVER (PARTITION BY Stock), 2) AS Volume_Ratio
    FROM stock_prices
    WHERE Volume > (
        SELECT AVG(Volume) * 2
        FROM stock_prices AS inner_table
        WHERE inner_table.Stock = stock_prices.Stock
    )
    ORDER BY Volume_Ratio DESC
    """

    # ----------------------------
    # QUERY 5 - Moving Average (Window Function)
    # 7-day and 30-day moving average per stock
    # ----------------------------
    query5 = """
    SELECT
        Date,
        Stock,
        Close,
        ROUND(AVG(Close) OVER (
            PARTITION BY Stock
            ORDER BY Date
            ROWS 6 PRECEDING
        ), 2) AS MA_7,
        ROUND(AVG(Close) OVER (
            PARTITION BY Stock
            ORDER BY Date
            ROWS 29 PRECEDING
        ), 2) AS MA_30
    FROM stock_prices
    ORDER BY Stock, Date
    """

    # ----------------------------
    # RUN ALL QUERIES
    # ----------------------------
    print("\n--- QUERY 1: Stock Summary ---")
    result1 = pd.read_sql(query1, connection)
    print(result1)
    result1.to_csv("data/sql_summary.csv", index=False)

    print("\n--- QUERY 2: Top 5 Stocks by Volume ---")
    result2 = pd.read_sql(query2, connection)
    print(result2)
    result2.to_csv("data/sql_top_volume.csv", index=False)

    print("\n--- QUERY 3: Price Growth % ---")
    result3 = pd.read_sql(query3, connection)
    print(result3)
    result3.to_csv("data/sql_growth.csv", index=False)

    print("\n--- QUERY 4: Volume Spike Days ---")
    result4 = pd.read_sql(query4, connection)
    print(result4)
    result4.to_csv("data/sql_volume_spikes.csv", index=False)

    print("\n--- QUERY 5: Moving Averages ---")
    result5 = pd.read_sql(query5, connection)
    print(result5)
    result5.to_csv("data/sql_moving_avg.csv", index=False)

    print("\nAll SQL analyses exported successfully!")
    connection.close()
    print("Database connection closed.")


run_sql_analysis()