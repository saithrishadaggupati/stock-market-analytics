# This file cleans our raw stock data
import pandas as pd

def clean_data():
    # Load the raw data
    df = pd.read_csv("data/stocks.csv")
    
    # Remove any empty rows
    df = df.dropna()
    
    # Reset the row numbers
    df = df.reset_index(drop=True)
    
    # Save cleaned data
    df.to_csv("data/stocks_clean.csv", index=False)
    print("Cleaning done! Saved to data/stocks_clean.csv")

clean_data()