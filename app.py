import html as _html
from datetime import UTC, datetime

import plotly.graph_objects as go
import streamlit as st
from src.components.newsletter import render_newsletter
from src.data.dashboard_query import DashboardSnapshot, load_dashboard_snapshot

st.set_page_config(page_title="Jupyter Crypto Wizard", page_icon="📈", layout="wide")

st.markdown(
    """
<style>
:root{
  --bg:#f4f6fb;--panel:#ffffff;--text:#111827;--muted:#667085;
  --accent:#3b5bff;--ok:#12b76a;--warn:#f79009;--bad:#f04438;--border:#e4e7ec;
}
html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(circle at 10% 0%, #eef2ff 0%, #f4f6fb 45%, #f7f8fc 100%);
  color: var(--text);
}
[data-testid="stSidebar"]{ background: linear-gradient(180deg,#f8f9fd 0%,#f1f4fb 100%); border-right:1px solid var(--border); }
.card, .panel{
  background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:14px;
  box-shadow:0 8px 24px rgba(16,24,40,.04);
}
.small{ color:var(--muted); font-size:.85rem; }
.val{ font-size:1.4rem; font-weight:700; }
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Jupyter Crypto Wizard")
    st.caption("Crypto Command Center")
    nav = st.radio(
        "Nav", ["Dashboard", "Alerts", "News", "Risk", "Newsletter"], label_visibility="collapsed"
    )
    time_window = st.selectbox("Time Window", ["24H", "7D", "30D", "90D"], index=2)
    watchlist = st.multiselect(
        "Watchlist", ["BTC", "ETH", "SOL", "BNB", "XRP"], default=["BTC", "ETH", "SOL"]
    )


def _render_kpis(snapshot: DashboardSnapshot) -> None:
    for column, item in zip(st.columns(4), snapshot.kpis, strict=True):
        column.markdown(
            f'<div class="card"><div class="small">{item["label"]}</div>'
            f'<div class="val">{item["value"]}</div><div style="color:{item["color"]}">{item["delta"]}</div></div>',
            unsafe_allow_html=True,
        )


def _render_trend(snapshot: DashboardSnapshot) -> None:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Price Trend")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=snapshot.price_dates,
            y=snapshot.price_values,
            name=snapshot.primary_asset,
            mode="lines",
            line=dict(color="#3b5bff", width=2.4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=snapshot.price_dates,
            y=snapshot.price_trend,
            name="Trend",
            mode="lines",
            line=dict(color="#94a3ff", width=2, dash="dot"),
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=4, r=4, t=6, b=4),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Asset: {snapshot.primary_asset} • Window: {snapshot.time_window}")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_trending(snapshot: DashboardSnapshot) -> None:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Trending Report")
    st.dataframe(snapshot.trending, hide_index=True, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_risk(snapshot: DashboardSnapshot) -> None:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Risk Graph")
    rfig = go.Figure(
        data=[
            go.Bar(
                x=snapshot.risk_scores,
                y=snapshot.risk_labels,
                orientation="h",
                marker=dict(color=snapshot.risk_colors),
            )
        ]
    )
    rfig.update_layout(
        height=240,
        margin=dict(l=4, r=4, t=6, b=4),
        xaxis=dict(range=[0, 100]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(rfig, width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)


def _render_highlights(title: str, lines: list[str]) -> None:
    st.markdown(f'<div class="panel"><h4>{_html.escape(title)}</h4>', unsafe_allow_html=True)
    for line in lines:
        st.markdown(f"<p>{_html.escape(line)}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def _greeting_for_hour(hour: int) -> str:
    """Return a time-of-day greeting for the provided UTC hour."""
    if 5 <= hour < 12:
        return "Good Morning"
    if 12 <= hour < 18:
        return "Good Afternoon"
    return "Good Evening"


display_name = st.session_state.get("display_name")
now_utc = datetime.now(UTC)
greeting = _greeting_for_hour(now_utc.hour)
st.markdown(f"## {greeting}{f', {display_name}' if display_name else ''}")
st.caption(f"Live snapshot • {now_utc:%Y-%m-%d %H:%M} UTC")

if nav == "Newsletter":
    render_newsletter()
else:
    snapshot = load_dashboard_snapshot(time_window=time_window, watchlist=watchlist)
    if nav == "Dashboard":
        _render_kpis(snapshot)
        left, right = st.columns([2.2, 1], gap="large")
        with left:
            _render_trend(snapshot)
            _render_trending(snapshot)
        with right:
            _render_risk(snapshot)
            _render_highlights("Alerts", snapshot.alerts)
            _render_highlights("News Snapshot", snapshot.news)
    elif nav == "Alerts":
        _render_highlights("Alerts", snapshot.alerts)
    elif nav == "News":
        _render_highlights("News Snapshot", snapshot.news)
    elif nav == "Risk":
        _render_risk(snapshot)
