import streamlit as st
from openai import OpenAI


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

Answer in a friendly, helpful way.
Recommend the best matching service from the list.
Mention price, duration, and available times if helpful.
Do not make up services that are not listed.
"""

        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            return response.output_text

        except Exception as e:
            return f"AI error: {e}"