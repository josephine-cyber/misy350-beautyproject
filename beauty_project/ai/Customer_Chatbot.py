import streamlit as st
from data_manager.data_manager import DataManager
from ai.ai_service import BeautyChatbot

st.title("AI Beauty Chatbot")

# Make sure user is logged in
if not st.session_state.get("logged_in"):
    st.error("Please log in first.")
    st.stop()

# Load services from JSON
data = DataManager()
services = data.load_services()

# Create chatbot
chatbot = BeautyChatbot()

st.write(
    "Ask the AI assistant questions about services, pricing, styling goals, hair type, skin type, or what to book."
)

with st.container(border=True):
    question = st.text_area(
        "Ask the AI Beauty Assistant a question:",
        placeholder="Example: I have oily skin and want soft glam for graduation. What should I book?"
    )

    if st.button("Ask AI"):
        if question.strip() == "":
            st.error("Please type a question first.")
        else:
            with st.spinner("AI is thinking..."):
                answer = chatbot.answer_question(question, services)

            st.success("AI Response")
            st.write(answer)

st.divider()

st.subheader("Current Salon Services")
st.dataframe(services)