# Stock Market Analytics Dashboard
import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Stock Market Analytics", layout="wide")
st.title("📈 Stock Market Analytics Dashboard")
st.caption("Real-time stock analysis for top Indian & US companies")

# Load cleaned data
df = pd.read_csv("data/stocks_clean.csv")

# Show KPI cards at top
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Stocks Tracked", df["Stock"].nunique())
col2.metric("Total Data Points", len(df))
col3.metric("Date Range", "Last 90 Days")

# Stock selector
st.subheader("📉 Price Trend")
selected = st.selectbox("Select a Stock", df["Stock"].unique())
filtered = df[df["Stock"] == selected]

# Line chart
fig = px.line(filtered, x="Price", y="Price", title=f"{selected} Closing Price")
st.plotly_chart(fig, use_container_width=True)

# Full data table
st.subheader("📋 Full Data Table")
st.dataframe(df)