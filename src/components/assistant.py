import os

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from src.data.mock_market import trending_report_frame

ALERTS = ["BTC below 63,500", "ETH RSI crossed 70", "SOL breakout"]
NEWS = ["ETF flows rebound", "Layer-1 activity rotates to SOL", "Exchange reserves decline"]
KPIS = [
  "Market Cap Tracked: $2.14T (+2.8%)",
  "24H Volume: $86.3B (+5.1%)",
  "Risk Index: 62 / 100 (Elevated)",
  "Active Alerts: 7 (3 triggered today)",
]


def _read_secret_or_env(name, default=None):
  try:
    if name in st.secrets:
      return st.secrets[name]
  except StreamlitSecretNotFoundError:
    pass
  return os.getenv(name, default)


def _build_context(time_window, watchlist):
  top_trending = trending_report_frame().head(3).to_dict("records")
  return {
    "time_window": time_window,
    "watchlist": watchlist,
    "kpis": KPIS,
    "alerts": ALERTS,
    "news": NEWS,
    "trending_top3": top_trending,
  }


def _fallback_response(context, reason):
  watchlist = ", ".join(context["watchlist"]) if context["watchlist"] else "no assets selected"
  top_names = ", ".join(row["Asset"] for row in context["trending_top3"])
  return (
    "I can still summarize the current dashboard context:\n"
    f"- Watchlist: {watchlist}\n"
    f"- Time window: {context['time_window']}\n"
    f"- Top trending assets: {top_names}\n"
    f"- Active alert examples: {context['alerts'][0]}; {context['alerts'][1]}\n\n"
    f"GPT provider is unavailable ({reason}). Set `OPENAI_API_KEY` in environment or Streamlit secrets to enable live responses."
  )


def _query_model(prompt, context):
  api_key = _read_secret_or_env("OPENAI_API_KEY", "")
  if not api_key:
    return _fallback_response(context, "missing credentials")

  base_url = _read_secret_or_env("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
  model = _read_secret_or_env("OPENAI_MODEL", "gpt-4o-mini")
  timeout_seconds = float(_read_secret_or_env("OPENAI_TIMEOUT_SECONDS", 15))

  system_prompt = (
    "You are Ceremco AI, an in-app crypto dashboard assistant. "
    "Answer briefly using only the provided dashboard context (watchlist, KPIs, alerts, news, trending). "
    "If the answer is missing from context, say it is not available yet. "
    "Do not provide financial advice, trade execution instructions, or unverified claims. "
    "Offer practical next-step suggestions based on the shown dashboard panels."
  )

  user_prompt = (
    f"Question: {prompt}\n\n"
    f"Context:\n"
    f"- Time Window: {context['time_window']}\n"
    f"- Watchlist: {', '.join(context['watchlist']) if context['watchlist'] else 'none'}\n"
    f"- KPIs: {', '.join(context['kpis'])}\n"
    f"- Alerts: {', '.join(context['alerts'])}\n"
    f"- News: {', '.join(context['news'])}\n"
    f"- Trending Top3: {context['trending_top3']}\n"
  )

  headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
  body = {
    "model": model,
    "messages": [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_prompt},
    ],
    "temperature": 0.2,
    "max_tokens": 250,
  }

  try:
    response = requests.post(f"{base_url}/chat/completions", headers=headers, json=body, timeout=timeout_seconds)
    if response.status_code == 429:
      return _fallback_response(context, "rate limited")
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"].strip()
    return content if content else _fallback_response(context, "empty response")
  except requests.Timeout:
    return _fallback_response(context, "request timeout")
  except requests.RequestException:
    return _fallback_response(context, "provider request failed")
  except (KeyError, ValueError, TypeError):
    return _fallback_response(context, "provider response parse failed")


def render_assistant_panel(time_window, watchlist):
  st.markdown('<div class="panel">', unsafe_allow_html=True)
  st.subheader("AI Assistant")
  st.caption("Dashboard-grounded help for watchlist, KPIs, alerts, and news. Not financial advice.")

  if "assistant_messages" not in st.session_state:
    st.session_state.assistant_messages = []

  context = _build_context(time_window, watchlist)
  for msg in st.session_state.assistant_messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  prompt = st.chat_input("Ask about the current dashboard context")
  if prompt:
    st.session_state.assistant_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)
    answer = _query_model(prompt, context)
    with st.chat_message("assistant"):
      st.markdown(answer)
    st.session_state.assistant_messages.append({"role": "assistant", "content": answer})

  st.markdown('</div>', unsafe_allow_html=True)
