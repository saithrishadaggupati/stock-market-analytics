# Visualize stock market trends

import pandas as pd
import matplotlib.pyplot as plt


def visualize_data():

    print("Loading cleaned stock dataset...\n")

    # Load cleaned dataset
    df = pd.read_csv("data/stocks_clean.csv")

    print("Dataset loaded successfully!")

    # Convert Date column into date format
    df["Date"] = pd.to_datetime(df["Date"])

    # Get RELIANCE stock only
    reliance = df[df["Stock"] == "RELIANCE.NS"]

    # Create graph
    plt.figure(figsize=(12, 6))

    plt.plot(
        reliance["Date"],
        reliance["Close"],
        marker='o'
    )

    # Graph labels
    plt.title("Reliance Stock Closing Price Trend")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")

    # Rotate date labels
    plt.xticks(rotation=45)

    # Adjust layout
    plt.tight_layout()

    # Save graph
    plt.savefig("data/reliance_stock_trend.png")

    # Show graph
    plt.show()

    print("\n===================================")
    print("Visualization completed successfully!")
    print("Graph saved to:")
    print("data/reliance_stock_trend.png")
    print("===================================")


# Run function
visualize_data()