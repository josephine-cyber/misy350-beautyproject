import streamlit as st
from openai import OpenAI


class BeautyAIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    def recommend_services(self, client_description, services):
        service_list = ""

        for service in services:
            service_list += (
                f"- {service['service_name']}: "
                f"${service['price']}, "
                f"{service['duration']}, "
                f"Available slots: {service['available_slots']}\n"
            )

        prompt = f"""
        You are a virtual pre-appointment beauty consultant for a salon booking app.

        The client described their needs as:
        {client_description}

        These are the ONLY services the salon currently offers:
        {service_list}

        Your job:
        1. Analyze the client's hair type, skin type, goals, concerns, and occasion.
        2. Recommend the best matching service or services from the salon list only.
        3. Explain why each service fits.
        4. Mention available appointment slots if relevant.
        5. End by encouraging the client to book through the app.

        Do not recommend services that are not in the list.
        Keep the tone friendly, professional, and helpful.
        """

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text