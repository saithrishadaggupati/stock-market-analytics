# Dashboard for stock market analytics

import pandas as pd
import matplotlib.pyplot as plt


def create_dashboard():

    print("Loading stock dataset...\n")

    # Load cleaned data
    df = pd.read_csv("data/stocks_clean.csv")

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    print("Dataset loaded successfully!")

    # Unique stock names
    stocks = df["Stock"].unique()

    # Create large figure
    plt.figure(figsize=(14, 8))

    # Loop through each stock
    for stock in stocks:

        stock_data = df[df["Stock"] == stock]

        plt.plot(
            stock_data["Date"],
            stock_data["Close"],
            label=stock
        )

    # Dashboard styling
    plt.title("Stock Market Dashboard")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")

    # Show legend
    plt.legend()

    # Rotate dates
    plt.xticks(rotation=45)

    # Better spacing
    plt.tight_layout()

    # Save graph
    plt.savefig("data/dashboard.png")

    # Show graph
    plt.show()

    print("\n===================================")
    print("Dashboard created successfully!")
    print("Saved to: data/dashboard.png")
    print("===================================")


# Run function
create_dashboard()