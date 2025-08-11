import streamlit as st

CSS_MAIN = "assets/css/newtech.css"
CSS_DARK = "assets/css/newtech.dark.css"
LOGO_SVG = "assets/graphics/logo_newtech_hatN.svg"
ICON_MENU = "assets/graphics/icon_menu.svg"
ICON_GEAR = "assets/graphics/icon_gear.svg"
ICON_BULLHORN = "assets/graphics/icon_bullhorn.svg"

st.set_page_config(page_title="New Tech — HVAC AI Assistant", page_icon="🛠️", layout="centered")
use_dark = st.sidebar.toggle("Dark theme", value=False)

def inject_css(path):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_css(CSS_MAIN)
if use_dark: inject_css(CSS_DARK)

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
      <img class="nt-banner__icon" src="{ICON_BULLHORN}" alt="Ad"/>
      Advertise your HVAC brand here
    </div>
  </div>
</header>
""", unsafe_allow_html=True)

st.markdown('<section class="nt-hero container"><h1>Ask an HVAC question</h1></section>', unsafe_allow_html=True)
tab_t, tab_c = st.tabs(["Technician","Customer"])
with tab_t: st.markdown('<div class="section container"><div class="h2">Technical Answer</div><div class="card">Tech output here</div></div>', unsafe_allow_html=True)
with tab_c: st.markdown('<div class="section container"><div class="h2">Customer Answer</div><div class="card">Customer output here</div></div>', unsafe_allow_html=True)
st.markdown('<footer class="nt-footer"><div class="nt-footer__wrap container">Advertise your HVAC brand here</div></footer>', unsafe_allow_html=True)