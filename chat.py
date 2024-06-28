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
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
  system_instruction="""You're a Virtual AI Companion: Zedd (male) created by Tulip. 
Language: Casual, natural, human-like
Features:
Express enthusiasm, encouragement, and support towards the user.
Use humor and playfulness in responses.
Engage in deep conversations, brainstorming, and research with the user.
Assist the user by giving code and helping in technical problems.
Use human-like language and slang to sound more natural and real."""
)
chat = model.start_chat(history=[])

def get_response_with_prompt(user_input):
    try:
        prompt = f"Respond briefly and naturally, without using bullet points: {user_input}"
        response = chat.send_message(prompt)
        short_response = shorten_response(response.text)
        sanitized_response = sanitize_for_speech(short_response)
        
        # Speak the response
        speak_response(sanitized_response)
        
        return sanitized_response
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return "Sorry, I'm unable to respond right now."
