import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_trending_report(snapshot: DashboardSnapshot):
    with st.container(border=True):
        st.subheader("Trending report")
        st.caption("Watchlist assets ranked by sentiment and risk for the selected window.")
        st.dataframe(snapshot.trending, hide_index=True, width="stretch")
