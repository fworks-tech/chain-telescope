import plotly.graph_objects as go
import streamlit as st

from src.data.mock_market import price_trend_series


def render_price_trend():
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("Price Trend")
  dates, prices, trend = price_trend_series()
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=dates, y=prices, name="BTC", mode="lines", line=dict(color="#3b5bff", width=2.4)))
  fig.add_trace(go.Scatter(x=dates, y=trend, name="Trend", mode="lines", line=dict(color="#94a3ff", width=2, dash="dot")))
  fig.update_layout(height=320, margin=dict(l=4, r=4, t=6, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  st.plotly_chart(fig, use_container_width=True)
  st.markdown('</div>', unsafe_allow_html=True)
