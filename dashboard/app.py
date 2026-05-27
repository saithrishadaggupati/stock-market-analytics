import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1e293b);
}

h1, h2, h3, h4 {
    color: white;
}

p {
    color: #d1d5db;
}

.stMetric {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================

st.title("📈 Stock Market Analytics Dashboard")

st.write(
    "Analyze stock market trends using Python, Pandas, Plotly and Streamlit."
)

st.divider()

# ============================================
# LOAD DATA
# ============================================

try:
    df = pd.read_csv("data/stocks_clean.csv")

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ============================================
# FIX DATE COLUMN
# ============================================

df["Date"] = pd.to_datetime(df["Date"])

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("📊 Dashboard Menu")

stock_list = df["Stock"].unique()

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    stock_list
)

# ============================================
# FILTER DATA
# ============================================

filtered_df = df[df["Stock"] == selected_stock]

# ============================================
# KPI METRICS
# ============================================

st.write("## 📌 Key Metrics")

col1, col2, col3 = st.columns(3)

latest_close = round(filtered_df["Close"].iloc[-1], 2)
highest_price = round(filtered_df["High"].max(), 2)
lowest_price = round(filtered_df["Low"].min(), 2)

col1.metric(
    "Latest Close",
    latest_close
)

col2.metric(
    "Highest Price",
    highest_price
)

col3.metric(
    "Lowest Price",
    lowest_price
)

st.divider()

# ============================================
# LINE CHART
# ============================================

st.write("## 📈 Closing Price Trend")

fig = px.line(
    filtered_df,
    x="Date",
    y="Close",
    color="Stock",
    markers=True,
    template="plotly_dark"
)

fig.update_layout(
    height=600,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font=dict(color="white"),
    title_font_size=24
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================
# VOLUME BAR CHART
# ============================================

st.write("## 📊 Trading Volume")

volume_fig = px.bar(
    filtered_df,
    x="Date",
    y="Volume",
    color="Volume",
    template="plotly_dark"
)

volume_fig.update_layout(
    height=500,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font=dict(color="white")
)

st.plotly_chart(
    volume_fig,
    use_container_width=True
)

# ============================================
# DATASET PREVIEW
# ============================================

st.write("## 🗂 Dataset Preview")

st.dataframe(
    filtered_df.head(20),
    use_container_width=True
)

# ============================================
# PROJECT INFO
# ============================================

st.write("## ℹ️ About Project")

st.info(
    """
    This Stock Market Analytics Dashboard was built using:

    • Python  
    • Pandas  
    • Plotly  
    • Streamlit  
    • Real-time stock market data from Yahoo Finance  

    Features:
    - Interactive dashboard
    - KPI metrics
    - Trend analysis
    - Volume analysis
    - Dataset preview
    """
)