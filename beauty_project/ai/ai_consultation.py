import streamlit as st
from data_manager import DataManager
from ai_service import BeautyAIAssistant

st.title("AI Pre-Appointment Consultation")

if not st.session_state.get("logged_in"):
    st.error("Please log in first.")
    st.stop()

data = DataManager()
services = data.load_services()
assistant = BeautyAIAssistant()

st.write("Describe your hair, skin, event, style goals, budget, or any concerns.")

with st.container(border=True):
    client_description = st.text_area(
        "Tell the AI what you need help with:",
        placeholder="Example: I have oily skin, want soft glam for graduation, and I need something that lasts all day."
    )

    if st.button("Get AI Recommendation"):
        if not client_description:
            st.error("Please describe what you need.")
        else:
            with st.spinner("AI is analyzing your beauty needs..."):
                recommendation = assistant.recommend_services(
                    client_description,
                    services
                )

            st.success("AI Recommendation Ready")
            st.write(recommendation)

st.divider()

st.subheader("Available Services")
st.dataframe(services)