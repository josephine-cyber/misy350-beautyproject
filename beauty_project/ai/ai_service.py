import streamlit as st
from openai import OpenAI


from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()



st.set_page_config(page_title="AI Order Assistant", page_icon="🤖")
st.title("🤖 Order Data Assistant")


client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

class BeautyChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["OPEN_AI_KEY"])

    def answer_question(self, question, services):
        service_info = ""

        for service in services:
            service_info += (
                f"- {service['service_name']}: "
                f"${service['price']}, "
                f"{service['duration']}, "
                f"Available slots: {service.get('available_slots', [])}\n"
            )

        prompt = f"""
You are an AI beauty booking assistant.

Only recommend services from this salon service list:
{service_info}

Customer question:
{question}

Recommend the best matching service from the list.
Explain why it fits the customer's needs.
Mention price, duration, and available times if helpful.
Do not make up services that are not listed.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful beauty booking assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"AI error: {e}"