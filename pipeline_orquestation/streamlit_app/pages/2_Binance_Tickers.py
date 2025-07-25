import streamlit as st
import pandas as pd
from utils.mongo_conn import get_binance_tickers
from utils.charts import plot_binance_volume

# ✅ Page Title
st.title("📊 Binance 24h Market Data")

# ✅ Fetch processed Binance data from MongoDB
data = get_binance_tickers()

if data and isinstance(data, list):
    latest = data[0]  # Latest processed record
    binance_data = latest.get("binance_data", [])  # ✅ Ensure correct key
    metadata = latest.get("metadata", {})

    if binance_data:
        # ✅ KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Symbols Tracked", metadata.get("total_symbols", 0))
        col2.metric("Top Symbol", metadata.get("top_symbol", "N/A"))
        col3.metric("Source", "Binance API")

        # ✅ Chart: Top 10 by Volume
        st.subheader("Top 10 Symbols by Volume (Base Asset)")
        st.plotly_chart(plot_binance_volume(binance_data), use_container_width=True)

        # ✅ Table - Filtered Columns
        st.subheader("📋 Filtered Binance Data")

        # Create DataFrame and filter by columns of interest
        columns_to_show = [
            "symbol", "price_change", "price_change_percent",
            "last_price", "high_price", "low_price"
        ]
        df = pd.DataFrame(binance_data)[columns_to_show]

        # ✅ Remove rows where ANY of these fields are strictly 0
        # (Keep values like 0.00000003 or negatives)
        numeric_cols = ["price_change", "price_change_percent", "last_price", "high_price", "low_price"]
        for col in numeric_cols:
            df = df[df[col] != 0]

        # ✅ Display table
        st.dataframe(df)

    else:
        st.warning("No Binance ticker data found.")
else:
    st.warning("No processed Binance data found in MongoDB.")
