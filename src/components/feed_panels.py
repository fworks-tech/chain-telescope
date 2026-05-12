import streamlit as st

from src.data.mock_market import alerts_snapshot, news_snapshot


def render_alerts_panel():
  alerts = "".join(f"<p>{item}</p>" for item in alerts_snapshot())
  st.markdown(f'<div class="panel"><h4>Alerts</h4>{alerts}</div>', unsafe_allow_html=True)


def render_news_panel():
  news = "".join(f"<p>{item}</p>" for item in news_snapshot())
  st.markdown(f'<div class="panel"><h4>News Snapshot</h4>{news}</div>', unsafe_allow_html=True)
