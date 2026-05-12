import plotly.graph_objects as go
import streamlit as st

from src.data.mock_market import risk_graph_colors, risk_graph_labels, risk_graph_scores


def render_risk_graph():
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("Risk Graph")
  rfig = go.Figure(data=[go.Bar(
    x=risk_graph_scores(),
    y=risk_graph_labels(),
    orientation="h",
    marker=dict(color=risk_graph_colors()),
  )])
  rfig.update_layout(height=240, margin=dict(l=4, r=4, t=6, b=4), xaxis=dict(range=[0, 100]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  st.plotly_chart(rfig, use_container_width=True)
  st.markdown("</div>", unsafe_allow_html=True)
