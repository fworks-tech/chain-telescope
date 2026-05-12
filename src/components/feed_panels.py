import streamlit as st


def render_alerts_panel():
  st.markdown('<div class="panel"><h4>Alerts</h4><p>BTC below 63,500</p><p>ETH RSI crossed 70</p><p>SOL breakout</p></div>', unsafe_allow_html=True)


def render_news_panel():
  st.markdown('<div class="panel"><h4>News Snapshot</h4><p>ETF flows rebound</p><p>Layer-1 activity rotates to SOL</p><p>Exchange reserves decline</p></div>', unsafe_allow_html=True)
