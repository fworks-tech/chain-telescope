import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_trending_report(snapshot: DashboardSnapshot):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Trending Report")
    st.dataframe(snapshot.trending, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
