import streamlit as st


def render_sidebar():
  with st.sidebar:
    st.markdown("## Ceremco AI")
    st.caption("Crypto Command Center")
    nav = st.radio("Nav", ["Dashboard", "Alerts", "News", "Risk", "Newsletter"], label_visibility="collapsed")
    time_window = st.selectbox("Time Window", ["24H", "7D", "30D", "90D"], index=2)
    watchlist = st.multiselect("Watchlist", ["BTC", "ETH", "SOL", "BNB", "XRP"], default=["BTC", "ETH", "SOL"])
  return nav, time_window, watchlist
