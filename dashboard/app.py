import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Stock Market Intelligence",
    page_icon="📊",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
.main { background-color: #0a0f1e; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a, #1b263b);
}
h1, h2, h3 { color: #e2e8f0; }
p { color: #94a3b8; }
.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid #3b82f6;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/stocks_clean.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Stock", "Date"])
    df["Daily_Return"] = df.groupby("Stock")["Close"].pct_change() * 100
    df["MA_7"] = df.groupby("Stock")["Close"].transform(
        lambda x: x.rolling(7).mean()
    )
    df["MA_30"] = df.groupby("Stock")["Close"].transform(
        lambda x: x.rolling(30).mean()
    )
    df["Volatility"] = df.groupby("Stock")["Daily_Return"].transform(
        lambda x: x.rolling(30).std()
    )
    return df

df = load_data()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title("📊 Stock Intelligence")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Market Overview",
        "📈 Stock Deep Dive",
        "🏭 Sector Analysis",
        "⚡ Volatility & Risk",
        "🔍 Key Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Data: Yahoo Finance | 3 Years | 25 Stocks")

# ============================================
# PAGE 1 — MARKET OVERVIEW
# ============================================
if page == "🏠 Market Overview":

    st.title("🏠 Market Overview")
    st.caption("Performance summary across all 25 stocks — Indian & US markets")
    st.divider()

    # Summary KPIs
    total_stocks = df["Stock"].nunique()
    date_range = f"{df['Date'].min().strftime('%b %Y')} → {df['Date'].max().strftime('%b %Y')}"
    total_records = len(df)
    avg_daily_return = round(df["Daily_Return"].mean(), 3)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Stocks", total_stocks)
    col2.metric("Date Range", date_range)
    col3.metric("Total Records", f"{total_records:,}")
    col4.metric("Avg Daily Return", f"{avg_daily_return}%")

    st.divider()

    # Price Growth % for all stocks
    st.subheader("📊 3-Year Price Growth % — All Stocks")

    growth = df.groupby("Stock").agg(
        Start=("Close", "first"),
        End=("Close", "last")
    ).reset_index()
    growth["Growth_Pct"] = ((growth["End"] - growth["Start"]) / growth["Start"] * 100).round(2)
    growth = growth.sort_values("Growth_Pct", ascending=True)

    colors = ["#ef4444" if x < 0 else "#22c55e" for x in growth["Growth_Pct"]]

    fig = go.Figure(go.Bar(
        x=growth["Growth_Pct"],
        y=growth["Stock"],
        orientation="h",
        marker_color=colors,
        text=growth["Growth_Pct"].apply(lambda x: f"{x}%"),
        textposition="outside"
    ))
    fig.update_layout(
        height=700,
        template="plotly_dark",
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        xaxis_title="Growth %",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top gainers and losers
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Top 5 Gainers")
        top5 = growth.nlargest(5, "Growth_Pct")[["Stock", "Growth_Pct"]]
        top5.columns = ["Stock", "Growth %"]
        st.dataframe(top5, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("📉 Bottom 5 Performers")
        bottom5 = growth.nsmallest(5, "Growth_Pct")[["Stock", "Growth_Pct"]]
        bottom5.columns = ["Stock", "Growth %"]
        st.dataframe(bottom5, use_container_width=True, hide_index=True)

# ============================================
# PAGE 2 — STOCK DEEP DIVE
# ============================================
elif page == "📈 Stock Deep Dive":

    st.title("📈 Stock Deep Dive")
    st.caption("Detailed analysis for individual stocks")
    st.divider()

    selected_stock = st.selectbox("Select Stock", sorted(df["Stock"].unique()))
    sdf = df[df["Stock"] == selected_stock].copy()

    # KPIs
    latest = sdf.iloc[-1]
    first = sdf.iloc[0]
    growth = ((latest["Close"] - first["Close"]) / first["Close"] * 100).round(2)
    avg_vol = sdf["Volume"].mean()
    volatility = sdf["Daily_Return"].std().round(2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"{latest['Close']:.2f}")
    col2.metric("3Y Growth", f"{growth}%")
    col3.metric("Avg Daily Volume", f"{avg_vol:,.0f}")
    col4.metric("Volatility (Std Dev)", f"{volatility}%")

    st.divider()

    # Price + Moving Averages
    st.subheader("📈 Price with Moving Averages (7D & 30D)")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sdf["Date"], y=sdf["Close"],
        name="Close Price", line=dict(color="#3b82f6", width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=sdf["Date"], y=sdf["MA_7"],
        name="7-Day MA", line=dict(color="#f59e0b", width=1.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=sdf["Date"], y=sdf["MA_30"],
        name="30-Day MA", line=dict(color="#ef4444", width=1.5, dash="dot")
    ))
    fig.update_layout(
        height=500, template="plotly_dark",
        paper_bgcolor="#0a0f1e", plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Daily Returns
    st.subheader("📊 Daily Returns %")
    fig2 = px.bar(
        sdf, x="Date", y="Daily_Return",
        color="Daily_Return",
        color_continuous_scale=["#ef4444", "#94a3b8", "#22c55e"],
        template="plotly_dark"
    )
    fig2.update_layout(
        height=400,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Volume
    st.subheader("📦 Trading Volume")
    fig3 = px.bar(
        sdf, x="Date", y="Volume",
        template="plotly_dark",
        color_discrete_sequence=["#6366f1"]
    )
    fig3.update_layout(
        height=400,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig3, use_container_width=True)

# ============================================
# PAGE 3 — SECTOR ANALYSIS
# ============================================
elif page == "🏭 Sector Analysis":

    st.title("🏭 Sector Analysis")
    st.caption("Compare performance across Indian and US market sectors")
    st.divider()

    # Sector mapping
    sector_map = {
        "TCS.NS": "Indian IT", "INFY.NS": "Indian IT",
        "WIPRO.NS": "Indian IT", "HCLTECH.NS": "Indian IT",
        "HDFCBANK.NS": "Indian Banking", "ICICIBANK.NS": "Indian Banking",
        "SBIN.NS": "Indian Banking", "AXISBANK.NS": "Indian Banking",
        "RELIANCE.NS": "Indian Energy", "ONGC.NS": "Indian Energy",
        "LT.NS": "Indian Industrial", "ITC.NS": "Indian FMCG",
        "HINDUNILVR.NS": "Indian FMCG", "TITAN.NS": "Indian Consumer",
        "BAJFINANCE.NS": "Indian Finance",
        "AAPL": "US Tech", "MSFT": "US Tech",
        "GOOGL": "US Tech", "META": "US Tech", "AMZN": "US Tech",
        "NVDA": "US Semiconductors", "AMD": "US Semiconductors",
        "TSLA": "US EV", "JPM": "US Banking", "BAC": "US Banking"
    }

    df["Sector"] = df["Stock"].map(sector_map)

    # Average growth by sector
    growth = df.groupby("Stock").agg(
        Start=("Close", "first"),
        End=("Close", "last")
    ).reset_index()
    growth["Growth_Pct"] = ((growth["End"] - growth["Start"]) / growth["Start"] * 100).round(2)
    growth["Sector"] = growth["Stock"].map(sector_map)

    sector_avg = growth.groupby("Sector")["Growth_Pct"].mean().round(2).reset_index()
    sector_avg.columns = ["Sector", "Avg_Growth_Pct"]
    sector_avg = sector_avg.sort_values("Avg_Growth_Pct", ascending=False)

    st.subheader("📊 Average 3-Year Growth by Sector")
    fig = px.bar(
        sector_avg, x="Sector", y="Avg_Growth_Pct",
        color="Avg_Growth_Pct",
        color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
        template="plotly_dark",
        text="Avg_Growth_Pct"
    )
    fig.update_layout(
        height=500,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Stock breakdown by sector
    st.subheader("🔍 Stock-Level Breakdown by Sector")
    selected_sector = st.selectbox("Select Sector", sorted(df["Sector"].dropna().unique()))
    sector_stocks = growth[growth["Sector"] == selected_sector].sort_values("Growth_Pct", ascending=False)

    fig2 = px.bar(
        sector_stocks, x="Stock", y="Growth_Pct",
        color="Growth_Pct",
        color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
        template="plotly_dark",
        text="Growth_Pct"
    )
    fig2.update_layout(
        height=400,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 4 — VOLATILITY & RISK
# ============================================
elif page == "⚡ Volatility & Risk":

    st.title("⚡ Volatility & Risk Analysis")
    st.caption("Which stocks are the riskiest? Which are the most stable?")
    st.divider()

    # Volatility per stock
    vol = df.groupby("Stock")["Daily_Return"].std().round(3).reset_index()
    vol.columns = ["Stock", "Volatility"]
    vol = vol.sort_values("Volatility", ascending=False)

    st.subheader("📊 Volatility Ranking — All Stocks")
    fig = px.bar(
        vol, x="Stock", y="Volatility",
        color="Volatility",
        color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
        template="plotly_dark",
        text="Volatility"
    )
    fig.update_layout(
        height=500,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔴 Top 5 Most Volatile")
        st.dataframe(vol.head(5), use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🟢 Top 5 Most Stable")
        st.dataframe(vol.tail(5), use_container_width=True, hide_index=True)

    st.divider()

    # Risk vs Return scatter
    st.subheader("🎯 Risk vs Return — Every Stock")
    st.caption("High return + low risk = ideal investment. Top-left quadrant is best.")

    growth = df.groupby("Stock").agg(
        Start=("Close", "first"),
        End=("Close", "last")
    ).reset_index()
    growth["Growth_Pct"] = ((growth["End"] - growth["Start"]) / growth["Start"] * 100).round(2)

    risk_return = vol.merge(growth[["Stock", "Growth_Pct"]], on="Stock")

    fig2 = px.scatter(
        risk_return, x="Volatility", y="Growth_Pct",
        text="Stock", size_max=20,
        color="Growth_Pct",
        color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
        template="plotly_dark"
    )
    fig2.update_traces(textposition="top center", marker=dict(size=12))
    fig2.update_layout(
        height=600,
        paper_bgcolor="#0a0f1e",
        plot_bgcolor="#0a0f1e",
        font=dict(color="white"),
        xaxis_title="Volatility (Risk)",
        yaxis_title="3Y Growth % (Return)"
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 5 — KEY INSIGHTS
# ============================================
elif page == "🔍 Key Insights":

    st.title("🔍 Key Insights")
    st.caption("What does 3 years of data actually tell us?")
    st.divider()

    # Auto-generate insights from data
    growth = df.groupby("Stock").agg(
        Start=("Close", "first"),
        End=("Close", "last")
    ).reset_index()
    growth["Growth_Pct"] = ((growth["End"] - growth["Start"]) / growth["Start"] * 100).round(2)

    top_gainer = growth.loc[growth["Growth_Pct"].idxmax()]
    worst = growth.loc[growth["Growth_Pct"].idxmin()]

    vol = df.groupby("Stock")["Daily_Return"].std().round(3).reset_index()
    vol.columns = ["Stock", "Volatility"]
    most_volatile = vol.loc[vol["Volatility"].idxmax()]
    most_stable = vol.loc[vol["Volatility"].idxmin()]

    avg_indian = growth[growth["Stock"].str.contains(".NS")]["Growth_Pct"].mean().round(2)
    avg_us = growth[~growth["Stock"].str.contains(".NS")]["Growth_Pct"].mean().round(2)

    st.subheader("📌 Auto-Generated Findings")

    st.success(f"🏆 Best Performer: **{top_gainer['Stock']}** grew **{top_gainer['Growth_Pct']}%** over 3 years")
    st.error(f"📉 Worst Performer: **{worst['Stock']}** grew only **{worst['Growth_Pct']}%** over 3 years")
    st.warning(f"⚡ Most Volatile: **{most_volatile['Stock']}** with daily std dev of **{most_volatile['Volatility']}%**")
    st.info(f"🛡️ Most Stable: **{most_stable['Stock']}** with daily std dev of only **{most_stable['Volatility']}%**")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Indian Stock Growth (3Y)", f"{avg_indian}%")
    with col2:
        st.metric("Avg US Stock Growth (3Y)", f"{avg_us}%")

    if avg_us > avg_indian:
        st.info(f"📊 US stocks outperformed Indian stocks by **{round(avg_us - avg_indian, 2)}%** on average over 3 years")
    else:
        st.info(f"📊 Indian stocks outperformed US stocks by **{round(avg_indian - avg_us, 2)}%** on average over 3 years")

    st.divider()

    st.subheader("📋 Full Stock Performance Table")
    growth_display = growth.sort_values("Growth_Pct", ascending=False).copy()
    growth_display.columns = ["Stock", "Start Price", "End Price", "3Y Growth %"]
    st.dataframe(growth_display, use_container_width=True, hide_index=True)