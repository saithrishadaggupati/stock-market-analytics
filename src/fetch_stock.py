# This file fetches real stock data from the internet
# yfinance gives us FREE real stock market data

import yfinance as yf
import pandas as pd
import os

# These are the stocks we will track
# These are top Indian + US companies
STOCKS = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "AAPL", "GOOGL"]

def fetch_stock_data():
    # Empty list to store all stock data
    all_data = []
    
    for stock in STOCKS:
        print(f"Fetching data for {stock}...")
        
        # Download last 90 days of data
        df = yf.download(stock, period="90d")
        
        # Add stock name as a column
        df["Stock"] = stock
        
        # Add to our list
        all_data.append(df)
    
    # Combine all stocks into one table
    combined = pd.concat(all_data)
    
    # Save to CSV file in data folder
    combined.to_csv("data/stocks.csv")
    print("Done! Data saved to data/stocks.csv")

# Run the function
fetch_stock_data()