import streamlit as st

from src.validation.email import is_valid_email


def render_newsletter():
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("Newsletter")
  a, b, c = st.columns([2, 1, 1])
  email = a.text_input("Email", placeholder="you@domain.com")
  freq = b.selectbox("Frequency", ["Daily", "Weekly", "Biweekly"], index=1)
  fmt = c.selectbox("Format", ["Summary", "Deep Dive"], index=0)
  if st.button("Subscribe"):
    if is_valid_email(email):
      st.success(f"Subscribed: {email} • {freq} • {fmt}")
    else:
      st.error("Please enter a valid email.")
  st.markdown('</div>', unsafe_allow_html=True)
