import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres123@localhost:5432/stock_db")

# ============================================
# DIM STOCK TABLE
# ============================================
dim_stock_data = {
    "ticker": [
        "TCS.NS","INFY.NS","WIPRO.NS","HCLTECH.NS",
        "HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","AXISBANK.NS",
        "RELIANCE.NS","LT.NS","ONGC.NS","ITC.NS",
        "HINDUNILVR.NS","TITAN.NS","BAJFINANCE.NS",
        "AAPL","MSFT","GOOGL","META","AMZN",
        "NVDA","AMD","TSLA","JPM","BAC"
    ],
    "company_name": [
        "Tata Consultancy Services","Infosys","Wipro","HCL Technologies",
        "HDFC Bank","ICICI Bank","State Bank of India","Axis Bank",
        "Reliance Industries","Larsen & Toubro","ONGC","ITC Limited",
        "Hindustan Unilever","Titan Company","Bajaj Finance",
        "Apple","Microsoft","Alphabet","Meta","Amazon",
        "NVIDIA","AMD","Tesla","JPMorgan Chase","Bank of America"
    ],
    "sector": [
        "Indian IT","Indian IT","Indian IT","Indian IT",
        "Indian Banking","Indian Banking","Indian Banking","Indian Banking",
        "Indian Energy","Indian Industrial","Indian Energy","Indian FMCG",
        "Indian FMCG","Indian Consumer","Indian Finance",
        "US Tech","US Tech","US Tech","US Tech","US Tech",
        "US Semiconductors","US Semiconductors","US EV","US Banking","US Banking"
    ],
    "country": [
        "India","India","India","India",
        "India","India","India","India",
        "India","India","India","India",
        "India","India","India",
        "US","US","US","US","US",
        "US","US","US","US","US"
    ]
}

dim_stock = pd.DataFrame(dim_stock_data)
dim_stock.to_sql("dim_stock", engine, if_exists="replace", index=True, index_label="stock_id")
print("✅ dim_stock created!")

# ============================================
# DIM DATE TABLE
# ============================================
dates = pd.date_range(start="2022-01-01", end="2025-12-31", freq="D")
dim_date = pd.DataFrame({
    "date": dates,
    "day": dates.day,
    "month": dates.month,
    "month_name": dates.strftime("%B"),
    "quarter": dates.quarter,
    "year": dates.year,
    "week": dates.isocalendar().week.values,
    "day_name": dates.strftime("%A"),
    "is_weekend": dates.weekday >= 5
})
dim_date.to_sql("dim_date", engine, if_exists="replace", index=True, index_label="date_id")
print("✅ dim_date created!")

# ============================================
# FACT TABLE
# ============================================
query = "SELECT * FROM stock_prices"
df = pd.read_sql(query, engine)
df["Date"] = pd.to_datetime(df["Date"])
df["country"] = df["Stock"].apply(lambda x: "India" if ".NS" in x else "US")

fact = df[["Date","Stock","Sector","Open","High","Low","Close","Volume","country"]]
fact.columns = ["date","ticker","sector","open","high","low","close","volume","country"]
fact.to_sql("fact_stock_prices", engine, if_exists="replace", index=True, index_label="fact_id")
print("✅ fact_stock_prices created!")

print("\n🎉 Star Schema complete!")