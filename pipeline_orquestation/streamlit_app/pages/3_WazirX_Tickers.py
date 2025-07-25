import streamlit as st
import pandas as pd
import plotly.express as px
from utils.mongo_conn import get_wazirx_tickers

# ✅ Page Title
st.title("📂 WazirX 24h Market Data")

# ✅ Fetch processed WazirX data from MongoDB
data = get_wazirx_tickers()

if data and isinstance(data, list):
    latest = data[0]  # Latest processed record
    wazirx_data = latest.get("wazirx_data", [])  # ✅ Correct key based on MongoDB
    metadata = latest.get("metadata", {})

    if wazirx_data:
        # ✅ KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Symbols Tracked", metadata.get("total_symbols", 0))
        col2.metric("Top Pair", metadata.get("top_symbol", "N/A"))
        col3.metric("Source", "WazirX API")

        # ✅ Prepare DataFrame
        columns_to_show = ["symbol", "base_asset", "open_price", "high_price", "low_price"]
        df = pd.DataFrame(wazirx_data)[columns_to_show]

        # ✅ Remove rows where any numeric field is strictly 0
        numeric_cols = ["open_price", "high_price", "low_price"]
        for col in numeric_cols:
            df = df[df[col] != 0]

        # ✅ Chart first: High vs Low Price
        st.subheader("📊 High vs Low Price (Top 10 by High Price)")
        top10 = df.sort_values(by="high_price", ascending=False).head(10)
        fig = px.bar(
            top10,
            x="symbol",
            y=["high_price", "low_price"],
            barmode="group",
            title="Top 10 WazirX Pairs: High vs Low Price",
            labels={"value": "Price (INR)", "symbol": "Trading Pair"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # ✅ Table after the chart
        st.subheader("📋 Filtered WazirX Data")
        st.dataframe(df)

    else:
        st.warning("No WazirX ticker data found.")
else:
    st.warning("No processed WazirX data found in MongoDB.")
