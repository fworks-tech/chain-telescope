import streamlit as st

from src.data.mock_market import alerts_snapshot, news_snapshot


def render_alerts_panel():
    lines = "".join(f"<p>{line}</p>" for line in alerts_snapshot())
    st.markdown(f'<div class="panel"><h4>Alerts</h4>{lines}</div>', unsafe_allow_html=True)


def render_news_panel():
    lines = "".join(f"<p>{line}</p>" for line in news_snapshot())
    st.markdown(
        f'<div class="panel"><h4>News Snapshot</h4>{lines}</div>',
        unsafe_allow_html=True,
    )
