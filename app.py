# app.py — New Tech HVAC AI Assistant (clean merged)
# -------------------------------------------------
import os
import streamlit as st
from chatgpt_helper import ask_chatgpt
from superheat_assistant import calculate_superheat

# 1) Page config FIRST
st.set_page_config(page_title="New Tech HVAC AI Assistant", page_icon="🛠️", layout="centered")

# 2) API key wiring (no hardcoding; pulls from env or Streamlit Secrets)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

# 3) Single CSS injector with sensible fallbacks
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

# 4) Header with logo
LOGO = "assets/graphics/logo_newtech_hatN.svg"  # change to "assets/graphics/logo.svg" if that's your file
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists(LOGO):
        st.image(LOGO, width=60)
    else:
        st.write("🔧")
with col2:
    st.markdown(
        "<h1 style='margin-bottom:0;'>New Tech HVAC Assistant</h1>"
        "<p style='color:gray;'>Powered by AI — Helping techs communicate and troubleshoot</p>",
        unsafe_allow_html=True
    )

st.markdown("---")  # Divider

# 5) Ask an HVAC question
st.subheader("Ask an HVAC question")
user_question = st.text_input("Type your question (e.g., 'What does high subcooling mean?')", key="q_text")

answer = None
if st.button("Get Answer", type="primary", use_container_width=True):
    if user_question and user_question.strip():
        with st.spinner("Thinking..."):
            answer = ask_chatgpt(user_question.strip())
        # stash for tabs below
        st.session_state["last_answer"] = answer
        st.success(answer)
    else:
        st.warning("Please enter a question first.")

# 6) Technician / Customer tabs
tech_tab, cust_tab = st.tabs(["Technician", "Customer"])

with tech_tab:
    st.markdown('<div class="section container"><div class="h2">Technical Answer</div></div>', unsafe_allow_html=True)
    tech_ans = st.session_state.get("last_answer")
    if tech_ans:
        st.markdown(f'<div class="card">{tech_ans}</div>', unsafe_allow_html=True)
    else:
        st.info("Ask a question above to see the technical answer here.")

with cust_tab:
    st.markdown('<div class="section container"><div class="h2">Customer Answer</div></div>', unsafe_allow_html=True)
    cust_ans = st.session_state.get("last_answer")
    if cust_ans:
        # For now we mirror the same text; later you can add a 'simplify for customer' transform
        st.markdown(f'<div class="card">{cust_ans}</div>', unsafe_allow_html=True)
    else:
        st.info("Ask a question above to see a customer-friendly explanation here.")

# 7) Superheat Calculator
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

# 8) Footer banner
st.markdown(
    '<footer class="nt-footer">'
    '<div class="nt-footer__wrap container">Advertise your HVAC brand here</div>'
    '</footer>',
    unsafe_allow_html=True
)
