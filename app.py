import streamlit as st

from src.components.dashboard_header import render_dashboard_header
from src.components.feed_panels import render_alerts_panel, render_news_panel
from src.components.kpi_row import render_kpi_row
from src.components.newsletter import render_newsletter
from src.components.price_trend import render_price_trend
from src.components.risk_graph import render_risk_graph
from src.components.sidebar import render_sidebar
from src.components.trending_report import render_trending_report
from src.styles import inject_global_styles

st.set_page_config(page_title="Crypto Market Analyzer", page_icon="📈", layout="wide")

inject_global_styles()
render_sidebar()
render_dashboard_header()
render_kpi_row()

left, right = st.columns([2.2, 1], gap="large")

with left:
  render_price_trend()
  render_trending_report()

with right:
  render_risk_graph()
  render_alerts_panel()
  render_news_panel()

render_newsletter()
