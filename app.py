import math
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Crypto Market Analyzer", page_icon="📈", layout="wide")

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
    st.markdown("## Ceremco AI")
    st.caption("Crypto Command Center")
    st.radio(
        "Nav", ["Dashboard", "Alerts", "News", "Risk", "Newsletter"], label_visibility="collapsed"
    )
    st.selectbox("Time Window", ["24H", "7D", "30D", "90D"], index=2)
    st.multiselect("Watchlist", ["BTC", "ETH", "SOL", "BNB", "XRP"], default=["BTC", "ETH", "SOL"])

st.markdown("## Good Morning, Richard")
st.caption(f"Live snapshot • {datetime.utcnow():%Y-%m-%d %H:%M} UTC")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(
    '<div class="card"><div class="small">Market Cap Tracked</div><div class="val">$2.14T</div><div style="color:#12b76a">+2.8%</div></div>',
    unsafe_allow_html=True,
)
c2.markdown(
    '<div class="card"><div class="small">24H Volume</div><div class="val">$86.3B</div><div style="color:#12b76a">+5.1%</div></div>',
    unsafe_allow_html=True,
)
c3.markdown(
    '<div class="card"><div class="small">Risk Index</div><div class="val">62 / 100</div><div style="color:#f79009">Elevated</div></div>',
    unsafe_allow_html=True,
)
c4.markdown(
    '<div class="card"><div class="small">Active Alerts</div><div class="val">7</div><div style="color:#3b5bff">3 triggered today</div></div>',
    unsafe_allow_html=True,
)

left, right = st.columns([2.2, 1], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Price Trend")
    days = 30
    dates = [datetime.today() - timedelta(days=i) for i in range(days)][::-1]
    prices = [64000 + 1200 * math.sin(i / 3) + i * 45 for i in range(days)]
    trend = pd.Series(prices).rolling(5, min_periods=1).mean()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates, y=prices, name="BTC", mode="lines", line=dict(color="#3b5bff", width=2.4)
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=trend,
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
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Trending Report")
    st.dataframe(
        pd.DataFrame(
            {
                "Asset": ["BTC", "ETH", "SOL", "BNB", "XRP"],
                "7D Change": ["+6.2%", "+4.1%", "+12.8%", "+2.9%", "-1.4%"],
                "Sentiment": ["Bullish", "Bullish", "Very Bullish", "Neutral", "Mixed"],
                "Risk": ["Medium", "Medium", "High", "Medium", "High"],
            }
        ),
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Risk Graph")
    rfig = go.Figure(
        data=[
            go.Bar(
                x=[62, 48, 71, 55],
                y=["Market", "Liquidity", "Momentum", "Whale Activity"],
                orientation="h",
                marker=dict(color=["#f79009", "#12b76a", "#f04438", "#3b5bff"]),
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
    st.plotly_chart(rfig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="panel"><h4>Alerts</h4><p>BTC below 63,500</p><p>ETH RSI crossed 70</p><p>SOL breakout</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="panel"><h4>News Snapshot</h4><p>ETF flows rebound</p><p>Layer-1 activity rotates to SOL</p><p>Exchange reserves decline</p></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.subheader("Newsletter")
a, b, c = st.columns([2, 1, 1])
email = a.text_input("Email", placeholder="you@domain.com")
freq = b.selectbox("Frequency", ["Daily", "Weekly", "Biweekly"], index=1)
fmt = c.selectbox("Format", ["Summary", "Deep Dive"], index=0)
if st.button("Subscribe"):
    st.success(
        f"Subscribed: {email} • {freq} • {fmt}"
    ) if "@" in email and "." in email else st.error("Please enter a valid email.")
st.markdown("</div>", unsafe_allow_html=True)
