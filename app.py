# app.py — New Tech HVAC AI Assistant
# -------------------------------------------------
import os
import streamlit as st
from chatgpt_helper import ask_chatgpt
from superheat_assistant import calculate_superheat

# -------------------------------------------------
# 1) Page config
# -------------------------------------------------
st.set_page_config(
    page_title="New Tech HVAC AI Assistant",
    page_icon="🛠️",
    layout="centered"
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
# 4) Top header bar (menu left, gear right) + orange banner
# -------------------------------------------------
HEADER_HTML = """
<header class="nt-header">
  <div class="nt-header__bar container">
    <button class="nt-iconbtn" title="Menu">
      <img src="assets/graphics/icon_menu.svg" alt="Menu">
    </button>
    <div style="margin-left:auto">
      <button class="nt-iconbtn" title="Settings">
        <img src="assets/graphics/icon_gear.svg" alt="Settings">
      </button>
    </div>
  </div>
  <div class="nt-banner">
    <div class="nt-banner__wrap container">
      <img class="nt-banner__icon" src="assets/graphics/icon_bullhorn.svg" alt="Ad"/>
      Advertise your HVAC brand here
    </div>
  </div>
</header>
"""
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# -------------------------------------------------
# 5) Centered logo hero (hat-N logo + NEW TECH wordmark)
# -------------------------------------------------
LOGO = "assets/graphics/logo.png"  # ensure this file exists
if os.path.exists(LOGO):
    st.markdown(
        f"""
        <div class="nt-logo-hero">
            <img src="{LOGO}" alt="New Tech Logo"/>
            <h1 class="nt-wordmark">NEW TECH</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div class="nt-logo-hero">
            <div style="font-size:48px">🔧</div>
            <h1 class="nt-wordmark">NEW TECH</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# 6) Ask an HVAC Question — headline band + search pill
# -------------------------------------------------
st.markdown('<section class="nt-hero container"><h1>Ask an HVAC question</h1></section>', unsafe_allow_html=True)

# Search pill layout: text input + mic icon + send button
with st.container():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([8, 1, 1])
    with c1:
        user_question = st.text_input(
            "", placeholder="e.g, normal subcooling for R-410A?", label_visibility="collapsed", key="q_text"
        )
    with c2:
        # Visual mic icon (placeholder — no action wired yet)
        st.markdown('<div class="nt-pillbtn"><img src="assets/graphics/icon_mic.svg" alt="Mic"/></div>', unsafe_allow_html=True)
    with c3:
        # Real Streamlit button (styled by CSS override below)
        send_clicked = st.button("", key="send_btn")
        st.markdown(
            # This styles the default Streamlit button to look like a plain pill icon button
            '<style>div[data-testid="baseButton-secondary"] button{background:#fff;border:2px solid #D1D5DB;border-radius:12px;height:44px}</style>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Ask OpenAI on click
if send_clicked and user_question and user_question.strip():
    with st.spinner("Thinking..."):
        answer = ask_chatgpt(user_question.strip())
    st.session_state["last_answer"] = answer

# -------------------------------------------------
# 7) Tabs: Technician / Customer
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

# Recent list (exact wording like mockup)
st.markdown('<div class="section container"><div class="h2">Recent</div></div>', unsafe_allow_html=True)
recent_items = [
    "It's the normal for air conditioning to have much subcooling in heat mode?",
    "What is the purpose of an equalizer tube?",
    "Why does an A/C unit freeze up?",
]
for txt in recent_items:
    st.markdown(f'<div class="container" style="padding:12px 0;border-bottom:1px solid #E5E7EB">{txt}</div>', unsafe_allow_html=True)

# -------------------------------------------------
# 8) Superheat Calculator
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
# 9) Footer ad banner
# -------------------------------------------------
st.markdown(
    '<footer class="nt-footer">'
    '<div class="nt-footer__wrap container">Advertise your HVAC brand here</div>'
    '</footer>',
    unsafe_allow_html=True
)
