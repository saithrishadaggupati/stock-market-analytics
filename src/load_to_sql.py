# Load stock data into SQLite database

import pandas as pd
import sqlite3


def load_data():

    print("Loading cleaned stock dataset...")

    # Read cleaned CSV
    df = pd.read_csv("data/stocks_clean.csv")

    # Create SQLite database
    connection = sqlite3.connect("stock_market.db")

    print("Database connected successfully!")

    # Load data into SQL table
    df.to_sql("stock_prices", connection,
              if_exists="replace",
              index=False)

    print("Stock data loaded into SQL database!")

    # Close connection
    connection.close()

    print("Database connection closed.")


# Run function
load_data()