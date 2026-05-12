import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_kpi_row(snapshot: DashboardSnapshot):
    c1, c2, c3, c4 = st.columns(4)
    for column, card in zip((c1, c2, c3, c4), snapshot.kpis, strict=True):
        column.markdown(
            f'<div class="card"><div class="small">{card["label"]}</div><div class="val">{card["value"]}</div>'
            f'<div style="color:{card["color"]}">{card["delta"]}</div></div>',
            unsafe_allow_html=True,
        )
