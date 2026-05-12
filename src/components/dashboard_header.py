from datetime import datetime

import streamlit as st


def render_dashboard_header():
    st.markdown("## Good Morning, Richard")
    st.caption(f"Live snapshot • {datetime.utcnow():%Y-%m-%d %H:%M} UTC")
