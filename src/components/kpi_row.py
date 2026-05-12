import streamlit as st


def render_kpi_row():
  c1, c2, c3, c4 = st.columns(4)
  c1.markdown(
    '<div class="card"><div class="small">Market Cap Tracked</div><div class="val">$2.14T</div>'
    '<div style="color:#12b76a">+2.8%</div></div>',
    unsafe_allow_html=True,
  )
  c2.markdown(
    '<div class="card"><div class="small">24H Volume</div><div class="val">$86.3B</div>'
    '<div style="color:#12b76a">+5.1%</div></div>',
    unsafe_allow_html=True,
  )
  c3.markdown(
    '<div class="card"><div class="small">Risk Index</div><div class="val">62 / 100</div>'
    '<div style="color:#f79009">Elevated</div></div>',
    unsafe_allow_html=True,
  )
  c4.markdown(
    '<div class="card"><div class="small">Active Alerts</div><div class="val">7</div>'
    '<div style="color:#3b5bff">3 triggered today</div></div>',
    unsafe_allow_html=True,
  )
