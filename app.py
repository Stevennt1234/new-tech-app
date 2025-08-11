import streamlit as st
from chatgpt_helper import ask_chatgpt
from superheat_assistant import calculate_superheat

st.set_page_config(page_title="New Tech HVAC AI Assistant", layout="centered")

st.title("🛠️ New Tech HVAC AI Assistant")

# Text input
user_question = st.text_input("Ask your HVAC question:")
if st.button("Get Answer"):
    if user_question:
        with st.spinner("Thinking..."):
            answer = ask_chatgpt(user_question)
        st.success(answer)

# HVAC Calculator
st.header("Superheat Calculator")
try:
    suction_temp = st.number_input("Suction Line Temp (°F)", value=50.0)
    saturation_temp = st.number_input("Saturation Temp (°F)", value=40.0)
    if st.button("Calculate Superheat"):
        result = calculate_superheat(suction_temp, saturation_temp)
        st.info(f"Superheat: {result} °F")
except Exception as e:
    st.error(f"Error: {e}")
