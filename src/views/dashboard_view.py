import streamlit as st
from src.components.assistant import render_assistant_panel
from src.components.dashboard_header import render_dashboard_header
from src.components.feed_panels import render_alerts_panel, render_news_panel
from src.components.kpi_row import render_kpi_row
from src.components.price_trend import render_price_trend
from src.components.risk_graph import render_risk_graph
from src.components.trending_report import render_trending_report
from src.data.dashboard_query import load_dashboard_snapshot


def render_dashboard_page(time_window: str, watchlist: list[str]):
    snapshot = load_dashboard_snapshot(time_window, watchlist)
    render_dashboard_header()
    render_kpi_row(snapshot)

    left, right = st.columns([2.2, 1], gap="large")
    with left:
        render_price_trend(snapshot)
        render_trending_report(snapshot)
    with right:
        render_risk_graph(snapshot)
        render_alerts_panel(snapshot)
        render_news_panel(snapshot)
        render_assistant_panel(time_window, watchlist)
