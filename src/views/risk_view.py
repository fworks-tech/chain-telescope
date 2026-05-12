import streamlit as st
from src.components.risk_graph import render_risk_graph
from src.data.dashboard_query import load_dashboard_snapshot


def render_risk_page(time_window: str, watchlist: list[str], market_source: str):
    snapshot = load_dashboard_snapshot(time_window, watchlist, market_source)
    st.markdown("## Risk")
    st.caption(f"Risk profile for {snapshot.time_window} across the selected watchlist.")
    render_risk_graph(snapshot)
