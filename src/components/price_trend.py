import plotly.graph_objects as go
import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_price_trend(snapshot: DashboardSnapshot):
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("Price Trend")
  st.caption(f"Primary asset: {snapshot.primary_asset} • Source: {snapshot.price_source}")
  fig = go.Figure()
  fig.add_trace(go.Scatter(
    x=snapshot.price_dates,
    y=snapshot.price_values,
    name=snapshot.primary_asset,
    mode="lines",
    line=dict(color="#3b5bff", width=2.4),
  ))
  fig.add_trace(go.Scatter(
    x=snapshot.price_dates,
    y=snapshot.price_trend,
    name="Trend",
    mode="lines",
    line=dict(color="#94a3ff", width=2, dash="dot"),
  ))
  fig.update_layout(height=320, margin=dict(l=4, r=4, t=6, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  st.plotly_chart(fig, width="stretch")
  st.markdown('</div>', unsafe_allow_html=True)
