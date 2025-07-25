import streamlit as st
import pandas as pd
from utils.mongo_conn import get_crypto_market_data
from utils.charts import plot_top_cryptos, plot_price_change

# ✅ Page Title
st.title("📈 Cryptocurrency Market Overview")

# ✅ Fetch processed crypto data from MongoDB
data = get_crypto_market_data()  # Use the correct function

if data and isinstance(data, list):
    latest = data[0]  # Only the latest processed record
    crypto_list = latest.get("crypto_data", [])
    metadata = latest.get("metadata", {})

    if crypto_list:
        # ✅ KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Coins", metadata.get("total_coins", 0))
        col2.metric("Top Coin", metadata.get("top_coin", "N/A"))
        col3.metric("Source", "CoinGecko")

        # ✅ Charts
        st.subheader("Top Cryptos by Market Cap")
        st.plotly_chart(plot_top_cryptos(crypto_list), use_container_width=True)

        st.subheader("Top Movers (24h % Change)")
        st.plotly_chart(plot_price_change(crypto_list), use_container_width=True)

        # ✅ Simplified Table with Images
        st.subheader("📋 Simplified Data View")
        columns_to_show = [
            "id", "symbol", "name", "image",
            "current_price", "price_change_24h", "price_change_percentage_24h"
        ]

        df = pd.DataFrame(crypto_list)[columns_to_show]

        # Render images as HTML
        def render_image(url):
            return f'<img src="{url}" width="30">'

        df["image"] = df["image"].apply(render_image)

        # Display HTML table
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.warning("No cryptocurrency data available in the latest record.")
else:
    st.warning("No processed crypto data found in MongoDB.")
