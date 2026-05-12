import plotly.graph_objects as go
import streamlit as st

from src.components.chart_theme import CHART_FONT_COLOR, CHART_GRID_COLOR
from src.data.dashboard_query import DashboardSnapshot


def render_risk_graph(snapshot: DashboardSnapshot):
    with st.container(border=True):
        st.subheader("Risk graph")
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
            margin=dict(l=0, r=0, t=8, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=CHART_FONT_COLOR),
            xaxis=dict(range=[0, 100], showgrid=True, gridcolor=CHART_GRID_COLOR, zeroline=False),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(rfig, width="stretch")
