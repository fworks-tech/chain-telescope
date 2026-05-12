import streamlit as st

TIME_WINDOWS = ["24H", "7D", "30D", "90D"]
WATCHLIST_OPTIONS = ["BTC", "ETH", "SOL", "BNB", "XRP"]


def render_sidebar_filters():
    with st.sidebar:
        st.markdown("## Ceremco AI")
        st.caption("Crypto Command Center")
        time_window = st.selectbox("Time Window", TIME_WINDOWS, index=2)
        watchlist = st.multiselect("Watchlist", WATCHLIST_OPTIONS, default=["BTC", "ETH", "SOL"])
    return time_window, watchlist
