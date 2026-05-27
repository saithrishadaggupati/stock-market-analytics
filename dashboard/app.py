import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Stock Market Analytics", layout="wide", page_icon="📈")

st.markdown("""
<style>
body { background-color: #0e1117; }
.metric-card { background: #1e2130; padding: 20px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Stock Market Analytics Dashboard")
st.caption("Live analysis of top Indian & US stocks")

df = pd.read_csv("data/stocks_clean.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Stocks Tracked", df["Stock"].nunique())
col2.metric("Total Data Points", len(df))
col3.metric("Date Range", "Last 90 Days")

st.divider()

st.subheader("Price Trend")
selected = st.selectbox("Select a Stock", df["Stock"].unique())
filtered = df[df["Stock"] == selected]

fig = px.line(filtered, x="Price", y="Close",
              title=f"{selected} Closing Price",
              color_discrete_sequence=["#00d4ff"],
              template="plotly_dark")
fig.update_layout(paper_bgcolor="#0e1117", plot_bgcolor="#0e1117")
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Full Data Table")
st.dataframe(df, use_container_width=True)