import streamlit as st
from src.styles import inject_global_styles

st.set_page_config(page_title="Crypto Market Analyzer", page_icon="📈", layout="wide")
inject_global_styles()

pages = [
    st.Page("pages/dashboard.py", title="Dashboard", default=True),
    st.Page("pages/alerts.py", title="Alerts"),
    st.Page("pages/news.py", title="News"),
    st.Page("pages/risk.py", title="Risk"),
    st.Page("pages/newsletter.py", title="Newsletter"),
]

st.navigation(pages).run()
