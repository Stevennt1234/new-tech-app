import os
import streamlit as st
from chatgpt_helper import ask_chatgpt
from superheat_assistant import calculate_superheat

st.set_page_config(page_title="New Tech HVAC AI Assistant", page_icon="🛠️", layout="centered")

# ---------- CSS injection (supports either assets/css/newtech.css OR assets/newtech.css OR styles.css) ----------
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

# ---------- Header + banner (skip if graphics missing) ----------
def file_exists(p): return os.path.exists(p)

ICON_MENU   = os.path.join("assets", "graphics", "icon_menu.svg")
ICON_GEAR   = os.path.join("assets", "graphics", "icon_gear.svg")
ICON_HORN   = os.path.join("assets", "graphics", "icon_bullhorn.svg")
LOGO_SVG    = os.path.join("assets", "graphics", "logo_newtech_hatN.svg")

has_graphics = all(map(file_exists, [ICON_MENU, ICON_GEAR, ICON_HORN, LOGO_SVG]))

if has_graphics:
    st.markdown(f"""
<header class="nt-header">
  <div class="nt-header__bar container">
    <div class="nt-header__left">
      <button class="nt-iconbtn"><img src="{ICON_MENU}" alt="Menu"></button>
      <div class="nt-logo">
        <img src="{LOGO_SVG}" height="36" alt="New Tech"/>
        <span class="nt-title">NEW TECH</span>
      </div>
    </div>
    <div class="nt-header__right">
      <button class="nt-iconbtn"><img src="{ICON_GEAR}" alt="Settings"></button>
    </div>
  </div>
  <div class="nt-banner">
    <div class="nt-banner__wrap container">
      <img class="nt-banner__icon" src="{ICON_HORN}" alt="Ad"/>
      Advertise your HVAC brand here
    </div>
  </div>
</header>
""", unsafe_allow_html=True)
else:
    st.title("🛠️ New Tech HVAC AI Assistant")

# ---------- Ask section ----------
st.markdown('<section class="nt-hero container"><h1>Ask an HVAC question</h1></section>', unsafe_allow_html=True)

user_question = st.text_input("Ask your HVAC question:")
if st.button("Get Answer"):
    if user_question.strip():
        with st.spinner("Thinking..."):
            answer = ask_chatgpt(user_question.strip())
        st.success(answer)
    else:
        st.warning("Please type a question.")

# ---------- Tabs ----------
tab_tech, tab_cust = st.tabs(["Technician", "Customer"])

with tab_tech:
    st.markdown('<div class="section container"><div class="h2">Technical Answer</div></div>', unsafe_allow_html=True)
    st.write("Your technical output will appear above once the Q&A runs.")

with tab_cust:
    st.markdown('<div class="section container"><div class="h2">Customer Answer</div></div>', unsafe_allow_html=True)
    st.write("Customer‑friendly explanation will appear above once the Q&A runs.")

# ---------- HVAC Calculator ----------
st.header("Superheat Calculator")
try:
    suction_temp = st.number_input("Suction Line Temp (°F)", value=50.0)
    saturation_temp = st.number_input("Saturation Temp (°F)", value=40.0)
    if st.button("Calculate Superheat"):
        result = calculate_superheat(suction_temp, saturation_temp)
        st.info(f"Superheat: {result} °F")
except Exception as e:
    st.error(f"Error: {e}")

# ---------- Footer banner ----------
if has_graphics:
    st.markdown('<footer class="nt-footer"><div class="nt-footer__wrap container">Advertise your HVAC brand here</div></footer>', unsafe_allow_html=True)
