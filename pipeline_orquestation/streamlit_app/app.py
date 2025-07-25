import streamlit as st
from utils.helpers import load_css
from utils.mongo_conn import get_crypto_market_data, get_binance_tickers, get_wazirx_tickers
import pandas as pd

# ✅ Page configuration
st.set_page_config(page_title="Crypto Market Dashboard", page_icon="💰", layout="wide")

# ✅ Load custom CSS
load_css("styles/style.css")

# ✅ Title & Intro
st.title("💰 Crypto Market Insights Dashboard")
st.write("""
Welcome to the **Crypto Market Dashboard**!  
This app consolidates real-time cryptocurrency data from **three major sources**:
- **CoinGecko**: Global market data for hundreds of cryptocurrencies.
- **Binance**: One of the world's largest crypto exchanges.
- **WazirX**: A popular exchange focused on INR (Indian Rupee) trading pairs.

Here, you can explore:
- **Top Cryptos** by Market Cap 💹
- **24h Price Changes** 📈
- **Trading Volumes** and Market Depth 📊
""")
st.markdown("---")

# ✅ Section: What do the metrics mean?
with st.expander("📘 Understanding the Metrics"):
    st.markdown("""
    **Key Terms Explained:**
    - **Market Cap**: Total value of all coins in circulation. Higher = bigger project.
    - **Price Change (24h)**: How much the price has moved in the last 24 hours.
    - **Volume**: Total traded amount in 24 hours. Shows liquidity.
    - **High / Low (24h)**: Maximum and minimum price during the last 24 hours.
    - **ATH / ATL**: All-Time High and All-Time Low prices historically.
    """)

# ✅ Quick stats section
st.subheader("📊 Market Overview (From CoinGecko)")

# Fetch latest processed data
crypto_data = get_crypto_market_data()
binance_data = get_binance_tickers()
wazirx_data = get_wazirx_tickers()

if crypto_data:
    df = pd.DataFrame(crypto_data[0].get("crypto_data", []))
    total_coins = len(df)
    top_coin = crypto_data[0]["metadata"].get("top_coin", "N/A")

    # ✅ KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Coins", total_coins, help="Number of cryptocurrencies tracked by CoinGecko")
    col2.metric("Top Coin", top_coin, help="Cryptocurrency with highest market cap")
    col3.metric("Data Source", "CoinGecko")

st.markdown("---")

# ✅ Navigation instructions
st.subheader("🧭 How to Use This Dashboard")
st.markdown("""
- **📈 Cryptocurrency Market**: Explore top coins, price trends, and rankings.
- **📊 Binance Market**: Check the most active trading pairs on Binance.
- **📂 WazirX Market**: See crypto prices against INR and liquidity.
""")
