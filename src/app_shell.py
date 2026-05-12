import streamlit as st

TIME_WINDOWS = ["24H", "7D", "30D", "90D"]
WATCHLIST_OPTIONS = ["BTC", "ETH", "SOL", "BNB", "XRP"]
MARKET_SOURCE_OPTIONS = {
    "Auto (best available)": "auto",
    "Binance": "binance",
    "CoinGecko": "coingecko",
    "Coinbase": "coinbase",
    "Mock (local)": "mock",
}


def render_sidebar_filters():
    with st.sidebar:
        st.markdown("## Filters")
        time_window = st.selectbox("Time Window", TIME_WINDOWS, index=2)
        watchlist = st.multiselect("Watchlist", WATCHLIST_OPTIONS, default=["BTC", "ETH", "SOL"])
        source_label = st.selectbox("Source", list(MARKET_SOURCE_OPTIONS), index=0)
        market_source = MARKET_SOURCE_OPTIONS[source_label]
    return time_window, watchlist, market_source
