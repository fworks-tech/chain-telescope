import streamlit as st

from src.data.dashboard_query import DashboardSnapshot


def render_kpi_row(snapshot: DashboardSnapshot):
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    for column, card in zip((c1, c2, c3, c4), snapshot.kpis, strict=True):
        with column.container(border=True):
            st.caption(card["label"])
            st.markdown(f'<div class="kpi-value">{card["value"]}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="kpi-delta" style="color:{card["color"]}">{card["delta"]}</div>',
                unsafe_allow_html=True,
            )
