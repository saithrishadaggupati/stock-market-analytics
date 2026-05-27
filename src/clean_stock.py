import pandas as pd

print("Loading raw stock dataset...")

# Load dataset
df = pd.read_csv("data/stocks.csv")

# Reset index properly
df.reset_index(inplace=True)

# Keep only required columns
df = df[[
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Stock"
]]

# Remove missing values
df.dropna(inplace=True)

# Save cleaned dataset
df.to_csv("data/stocks_clean.csv", index=False)

print("Dataset cleaned successfully!")
print("Saved file: data/stocks_clean.csv")