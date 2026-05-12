import streamlit as st

GLOBAL_STYLE = """
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
"""


def inject_global_styles():
  st.markdown(GLOBAL_STYLE, unsafe_allow_html=True)
