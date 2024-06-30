import re 
import emoji
import webbrowser 
import os
import pygame
import sys
import threading
from config import engine
import urllib
import requests
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs


import os
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speak_response(text):
    # try:
    #     voice = Voice(
    #         voice_id='2EiwWnXFnvU5JabPnv8n',
    #         settings=VoiceSettings(stability=0.5, similarity_boost=0.7, style=0.0, use_speaker_boost=True)
    #     )
    #     audio = client.generate(text=text, voice=voice)
    #     play(audio)
    # except Exception as e:
    #     print(f"Error speaking response: {e}")
    # try:
    #     stop_speaking = threading.Event()

    #     def on_word(name, location, length):
    #         if stop_speaking.is_set():
    #             engine.stop()

    #     engine.connect('started-word', on_word)
    #     sanitized_text = sanitize_for_speech(text)
    #     engine.say(sanitized_text)
    #     engine.runAndWait()

    # except Exception as e:
    #     print(f"Error speaking response: {e}")
    print("Speaking")

def shorten_response(text, max_length=500):
    if len(text) > max_length:
        sentences = text.split('. ')
        truncated_text = ''
        for sentence in sentences:
            if len(truncated_text) + len(sentence) + 1 <= max_length:
                truncated_text += sentence + '. '
            else:
                break
        truncated_text = truncated_text.strip()
        return truncated_text if truncated_text.endswith('.') else truncated_text + '...'
    return text

def sanitize_for_speech(text):
    # Remove asterisks and other unwanted characters
    sanitized_text = text.replace('*', '')
    sanitized_text = emoji.replace_emoji(sanitized_text, replace='')
    # Remove other special characters (if any)
    sanitized_text = re.sub(r'[^A-Za-z0-9\s.,!?\'"]+', '', sanitized_text)
    return sanitized_text    

def terminate_program():
    print("Deactivating. Have a nice day!")
    speak_response("Deactivating. Have a nice day!")
    pygame.mixer.music.stop()  # Stop music immediately
    cleanup()  # Cleanup resources
    sys.exit(0)  # Exit the program



def search_flipkart(query):
    url = f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Flipkart Search", url)]

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("YouTube Search", url)]

def search_amazon(query):
    url = f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Amazon Search", url)]

def search_google(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Google Search", url)]

def search_twitter(query):
    url = f"https://twitter.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Twitter Search", url)]

def search_instagram(query):
    url = f"https://www.instagram.com/web/search/topsearch/?query={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Instagram Search", url)]

def search_reddit(query):
    url = f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Reddit Search", url)]

def search_ebay(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("eBay Search", url)]

def search_wikipedia(query):
    url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Wikipedia Search", url)]

def search_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    webbrowser.open(url)
    return [("Bing Search", url)]

# Add more search functions for other platforms as needed

def parse_input(user_input):
    parts = user_input.lower().strip().split(" on ")
    if len(parts) == 2 and parts[0].startswith("search for "):
        query = parts[0][11:].strip()
        platform = parts[1].strip()
        return query, platform
    elif len(parts) == 2:
        query = parts[0].strip()
        platform = parts[1].strip()
        return query, platform
    else:
        return None, None

def handle_search(user_input):
    query, platform = parse_input(user_input)
    if not query or not platform:
        return "Invalid input format. Please use 'search for [query] on [platform]'."

    search_functions = {
        "flipkart": search_flipkart,
        "amazon": search_amazon,
        "youtube": search_youtube,
        "google": search_google,
        "twitter": search_twitter,
        "instagram": search_instagram,
        "reddit": search_reddit,
        "ebay": search_ebay,
        "wikipedia": search_wikipedia,
        "bing": search_bing,
    }

    search_function = search_functions.get(platform)
    if search_function:
        search_function(query)
        return f"Here's what i've found."
    else:
        return f"Unsupported platform: {platform}."


def interrupt_speech(stop_speaking_event):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                stop_speaking_event.set()
                break

def play_song_on_spotify(song_title):
    search_url = f"https://open.spotify.com/search/{urllib.parse.quote(song_title)}"
    try:
        webbrowser.open(search_url)
        print(f"Playing '{song_title}' on Spotify.")
        speak_response(f"Playing '{song_title}' on Spotify.")
    except Exception as e:
        print(f"Error opening Spotify: {e}")
        speak_response("Error opening Spotify. Please try again.")

def play_song(song_title):
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(song_title)}"
    try:
        with urllib.request.urlopen(search_url) as response:
            html = response.read()
            match = re.search(r"watch\?v=(\S{11})", html.decode("utf-8"))
            if match:
                video_id = match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                webbrowser.open(video_url)
                print(f"Playing '{song_title}' on YouTube.")
                speak_response(f"Playing '{song_title}' on YouTube.")
            else:
                print("Unable to find a video for the given title.")
                speak_response("Unable to play the requested song.")
    except urllib.error.HTTPError as e:
        print(f"Error accessing YouTube search results: {e}")
        speak_response("Error accessing YouTube search results.")

def google_search(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)
    print(f"Searching Google for '{query}'...")
    speak_response(f"Searching Google for '{query}'.")

def cleanup():
    print("\nCleaning up...")
    try:
        if pygame.mixer.get_init():
            pygame.mixer.quit()
    except Exception as e:
        print(f"Error during cleanup: {e}")

def handle_interrupt(signal, frame):
    print("\nCtrl+C detected. Exiting...")
    os._exit(0)


def open_application(app_name):
    app_name = app_name.lower().strip()
    app_urls = {
        "whatsapp": "https://web.whatsapp.com/",
        "telegram": "https://web.telegram.org/",
        "spotify": "https://open.spotify.com/",
        "my portfolio": "https://thetulipjani.vercel.app/",
        "gemini": "https://gemini.google.com/"
    }

    if app_name in app_urls:
        url = app_urls[app_name]
    else:
        if "." in app_name:
            url = f"https://{app_name}"
        else:
            url = f"https://{app_name}.com"
    
    print(f"Opening {url}")
    speak_response(f'Opening {app_name}')
    webbrowser.open(url)
