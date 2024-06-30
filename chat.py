import google.generativeai as genai
from utils import shorten_response, sanitize_for_speech
from config import engine
from utils import sanitize_for_speech, shorten_response, speak_response
import threading
import os
from dotenv import load_dotenv

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)

class Persona:
    def __init__(self, name, model_name, system_instruction):
        self.name = name
        self.model = genai.GenerativeModel(model_name=model_name, system_instruction=system_instruction)
        self.chat = self.model.start_chat(history=[])

    def get_response(self, user_input):
        try:
            prompt = f"Respond briefly and naturally, without using bullet points: {user_input}"
            response = self.chat.send_message(prompt)
            short_response = shorten_response(response.text)
            sanitized_response = sanitize_for_speech(short_response)
            speak_response(sanitized_response)
            return sanitized_response
        except Exception as e:
            print(f"Error getting response from {self.name}: {e}")
            return "Sorry, I'm unable to respond right now."

# Define personas
techie_zedd = Persona(
    name="Techie Zedd",
    model_name="gemini-1.5-flash",
    system_instruction="You're a super formal and technical coding assistant. Use precise language and provide detailed explanations."
)

creative_zedd = Persona(
    name="Creative Zedd",
    model_name="gemini-1.5-flash",
    system_instruction="You're a creative and cool assistant. Use imaginative language and help with brainstorming and image generation. you're completely for new gen, you're GenZ. be cool! super cool"
)

default_zedd = Persona(
    name="Default Zedd",
    model_name="gemini-1.5-flash",
    system_instruction="""You're a Virtual AI Companion: Zedd (male) created by Tulip, 18 y/o kid. Use natural language and words. Use works like 'uhmmms' and "ahhhh" and "hmmm" to make your responses sound more real. You have to be fully accurate while giving response, understand user's prompt in detail, and try to give as much as accurate answer. be real, and cool. you're created by Tulip, he's so cool, so as you also! give extreme information while brainstorming, and detailed answers whenever needed. try to be real, and also rude sometimes."""
)

# Set default persona
current_persona = default_zedd

def switch_persona(persona_name):
    global current_persona
    if persona_name == "Techie Zedd":
        current_persona = techie_zedd
    elif persona_name == "Creative Zedd":
        current_persona = creative_zedd
    elif persona_name == "Default Zedd":
        current_persona = default_zedd
    print(f"Switched to {current_persona.name}")

def get_response_with_prompt(user_input):
    return current_persona.get_response(user_input)

