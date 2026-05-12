import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_alerts_panel(snapshot: DashboardSnapshot):
  lines = "".join(f"<p>{line}</p>" for line in snapshot.alerts)
  st.markdown(f'<div class="panel"><h4>Alerts</h4>{lines}</div>', unsafe_allow_html=True)


def render_news_panel(snapshot: DashboardSnapshot):
  lines = "".join(f"<p>{line}</p>" for line in snapshot.news)
  st.markdown(f'<div class="panel"><h4>News Snapshot</h4>{lines}</div>', unsafe_allow_html=True)
