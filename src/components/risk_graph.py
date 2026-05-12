import plotly.graph_objects as go
import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_risk_graph(snapshot: DashboardSnapshot):
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("Risk Graph")
  rfig = go.Figure(data=[go.Bar(
    x=snapshot.risk_scores,
    y=snapshot.risk_labels,
    orientation="h",
    marker=dict(color=snapshot.risk_colors),
  )])
  rfig.update_layout(height=240, margin=dict(l=4, r=4, t=6, b=4), xaxis=dict(range=[0, 100]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  st.plotly_chart(rfig, use_container_width=True)
  st.markdown("</div>", unsafe_allow_html=True)
