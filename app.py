# app.py — New Tech HVAC AI Assistant (mockup-aligned, base64-safe images)
# -----------------------------------------------------------------------
import os
import base64, mimetypes
import streamlit as st
from chatgpt_helper import ask_chatgpt
from superheat_assistant import calculate_superheat

# -------------------------------------------------
# 1) Page config
# -------------------------------------------------
st.set_page_config(
    page_title="New Tech HVAC AI Assistant",
    page_icon="🛠️",
    layout="centered",
)

# -------------------------------------------------
# 2) API key wiring (env or Streamlit Secrets)
# -------------------------------------------------
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

# -------------------------------------------------
# 3) CSS injector
# -------------------------------------------------
def inject_first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            return p
    return None

css_used = inject_first_existing([
    os.path.join("assets", "css", "newtech.css"),
    os.path.join("assets", "newtech.css"),
    "styles.css",
])
if not css_used:
    st.warning("New Tech CSS not found. Expected assets/css/newtech.css (or assets/newtech.css).")

# -------------------------------------------------
# 4) Image helper (embed as base64 data URIs to avoid path issues)
# -------------------------------------------------
def data_uri(path: str) -> str:
    """Return a base64 data URI for any local image file; empty string if not found."""
    if not os.path.exists(path):
        return ""
    mime, _ = mimetypes.guess_type(path)
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime or 'image/png'};base64,{b64}"

# Expected graphics (case-sensitive on Streamlit Cloud)
LOGO_PATH    = "assets/graphics/logo.png"
MENU_SVG     = "assets/graphics/icon_menu.svg"
GEAR_SVG     = "assets/graphics/icon_gear.svg"
BULLHORN_SVG = "assets/graphics/icon_bullhorn.svg"
MIC_SVG      = "assets/graphics/icon_mic.svg"

logo_src     = data_uri(LOGO_PATH)
menu_src     = data_uri(MENU_SVG)
gear_src     = data_uri(GEAR_SVG)
bullhorn_src = data_uri(BULLHORN_SVG)
mic_src      = data_uri(MIC_SVG)

missing = [p for p,s in [
    (LOGO_PATH,logo_src),(MENU_SVG,menu_src),(GEAR_SVG,gear_src),
    (BULLHORN_SVG,bullhorn_src),(MIC_SVG,mic_src)
] if not s]
if missing:
    st.warning("Missing image files: " + ", ".join(missing))

# -------------------------------------------------
# 5) Top header bar (menu left, gear right) + orange banner
# -------------------------------------------------
HEADER_HTML = f"""
<header class="nt-header">
  <div class="nt-header__bar container">
    <button class="nt-iconbtn" title="Menu">
      <img src="{menu_src}" alt="Menu">
    </button>
    <div style="margin-left:auto">
      <button class="nt-iconbtn" title="Settings">
        <img src="{gear_src}" alt="Settings">
      </button>
    </div>
  </div>
  <div class="nt-banner">
    <div class="nt-banner__wrap container">
      <img class="nt-banner__icon" src="{bullhorn_src}" alt="Ad"/>
      Advertise your HVAC brand here
    </div>
  </div>
</header>
"""
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# -------------------------------------------------
# 6) Centered logo hero (hat-N logo + NEW TECH wordmark)
# -------------------------------------------------
st.markdown(
    f"""
    <div class="nt-logo-hero">
        {'<img src="'+logo_src+'" alt="New Tech Logo"/>' if logo_src else '<div style="font-size:48px">🔧</div>'}
        <h1 class="nt-wordmark">NEW TECH</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 7) Ask an HVAC Question — headline band + search pill
# -------------------------------------------------
st.markdown('<section class="nt-hero container"><h1>Ask an HVAC question</h1></section>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([8, 1, 1])
    with c1:
        user_question = st.text_input(
            "", placeholder="e.g, normal subcooling for R-410A?", label_visibility="collapsed", key="q_text"
        )
    with c2:
        st.markdown(f'<div class="nt-pillbtn"><img src="{mic_src}" alt="Mic"/></div>', unsafe_allow_html=True)
    with c3:
        send_clicked = st.button("", key="send_btn")  # styled by CSS override below
        st.markdown(
            '<style>div[data-testid="baseButton-secondary"] button{{background:#fff;border:2px solid #D1D5DB;border-radius:12px;height:44px}}</style>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Ask OpenAI on click
if send_clicked and user_question and user_question.strip():
    with st.spinner("Thinking..."):
        answer = ask_chatgpt(user_question.strip())
    st.session_state["last_answer"] = answer

# -------------------------------------------------
# 8) Tabs: Technician / Customer + Recent list
# -------------------------------------------------
tech_tab, cust_tab = st.tabs(["Technician", "Customer"])

with tech_tab:
    st.markdown('<div class="section container"><div class="h2">Technical Answer</div></div>', unsafe_allow_html=True)
    left, right = st.columns([5, 1])
    with left:
        tech_ans = st.session_state.get("last_answer")
        st.markdown(f'<div class="card">{tech_ans or ""}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="nt-chip">TTS</div>', unsafe_allow_html=True)

with cust_tab:
    st.markdown('<div class="section container"><div class="h2">Customer Answer</div></div>', unsafe_allow_html=True)
    cust_ans = st.session_state.get("last_answer")
    st.markdown(f'<div class="card">{cust_ans or ""}</div>', unsafe_allow_html=True)

# Recent (exact wording from mockup)
st.markdown('<div class="section container"><div class="h2">Recent</div></div>', unsafe_allow_html=True)
for txt in [
    "It's the normal for air conditioning to have much subcooling in heat mode?",
    "What is the purpose of an equalizer tube?",
    "Why does an A/C unit freeze up?",
]:
    st.markdown(f'<div class="container" style="padding:12px 0;border-bottom:1px solid #E5E7EB">{txt}</div>', unsafe_allow_html=True)

# -------------------------------------------------
# 9) Superheat Calculator
# -------------------------------------------------
st.subheader("Superheat Calculator")
with st.form("superheat_calc"):
    c1, c2 = st.columns(2)
    with c1:
        suction_temp = st.number_input("Suction Line Temp (°F)", value=50.0, step=0.5)
    with c2:
        saturation_temp = st.number_input("Saturation Temp (°F)", value=40.0, step=0.5)
    calc = st.form_submit_button("Calculate Superheat")
    if calc:
        try:
            result = calculate_superheat(suction_temp, saturation_temp)
            st.info(f"Superheat: {result} °F")
        except Exception as e:
            st.error(f"Calculation error: {e}")

# -------------------------------------------------
# 10) Footer ad banner
# -------------------------------------------------
st.markdown(
    '<footer class="nt-footer">'
    '<div class="nt-footer__wrap container">Advertise your HVAC brand here</div>'
    '</footer>',
    unsafe_allow_html=True
)
