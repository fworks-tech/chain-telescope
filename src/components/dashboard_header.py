from datetime import datetime

import streamlit as st


def render_dashboard_header(time_window: str, watchlist: list[str], market_source: str):
    watchlist_label = ", ".join(watchlist) if watchlist else "No assets selected"
    st.markdown("## Market dashboard")
    st.caption(
        f"Tracking {watchlist_label} over {time_window} from {market_source}. "
        f"Updated {datetime.utcnow():%Y-%m-%d %H:%M} UTC."
    )
