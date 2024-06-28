import requests
from config import CITY_NAME


import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        weather_info = f"The current temperature in {CITY_NAME} is {temp}°C with {weather_description}."
        return weather_info
    else:
        return "Sorry, I couldn't fetch the weather information."
