# SQL analysis for stock market data

import sqlite3
import pandas as pd


def run_sql_analysis():

    print("Connecting to database...")

    # Connect to SQLite database
    connection = sqlite3.connect("stock_market.db")

    print("Database connected!")

    # SQL query
    query = """
    SELECT
        Stock,
        AVG(Close) AS Average_Close_Price,
        SUM(Volume) AS Total_Volume
    FROM stock_prices
    GROUP BY Stock
    ORDER BY Average_Close_Price DESC
    """

    # Run query
    result = pd.read_sql(query, connection)

    print("\nSQL Analysis Result:")
    print(result)

    # Save SQL analysis
    result.to_csv("data/sql_analysis.csv", index=False)

    print("\nSQL analysis exported successfully!")

    # Close database connection
    connection.close()

    print("Database connection closed.")


# Run SQL analysis
run_sql_analysis()