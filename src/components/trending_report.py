import streamlit as st

from src.data.mock_market import trending_report_frame


def render_trending_report():
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Trending Report")
    st.dataframe(trending_report_frame(), hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
