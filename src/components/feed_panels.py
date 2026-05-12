import streamlit as st

from src.data.mock_market import alert_snapshot_lines, news_snapshot_lines


def render_alerts_panel():
  lines = "".join(f"<p>{line}</p>" for line in alert_snapshot_lines())
  st.markdown(f'<div class="panel"><h4>Alerts</h4>{lines}</div>', unsafe_allow_html=True)


def render_news_panel():
  lines = "".join(f"<p>{line}</p>" for line in news_snapshot_lines())
  st.markdown(f'<div class="panel"><h4>News Snapshot</h4>{lines}</div>', unsafe_allow_html=True)
