import re 
import emoji
import webbrowser 
import os
import pygame
import sys
import urllib
import requests  
import threading
import tempfile
import urllib.parse
import webbrowser

TTS_SERVER_URL = "http://localhost:5050/v1/audio/speech"
stop_event = threading.Event()

def speak_response(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_file:
        audio_file_path = audio_file.name

    data = {
        "input": text,
        "voice": "nova",  
        "response_format": "mp3",
        "speed": 1.175
    }

    try:
        response = requests.post(TTS_SERVER_URL, json=data, stream=True)
        response.raise_for_status()  
        with open(audio_file_path, 'wb') as audio_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    audio_file.write(chunk)

        pygame.mixer.init()

        try:
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy() and not stop_event.is_set():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {e}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: Please check if the TTS server is running.")
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
    sanitized_text = text.replace('*', '')
    sanitized_text = emoji.replace_emoji(sanitized_text, replace='')
    sanitized_text = re.sub(r'[^A-Za-z0-9\s.,!?\'"]+', '', sanitized_text)
    return sanitized_text    

def terminate_program():
    print("Deactivating. Have a nice day!")
    pygame.mixer.music.stop() 
    speak_response("Bye! See ya later...")
    cleanup()  
    sys.exit(0)  

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

def play_video_on_youtube(video):
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(video)}"
    try:
        with urllib.request.urlopen(search_url) as response:
            html = response.read()
            match = re.search(r"watch\?v=(\S{11})", html.decode("utf-8"))
            if match:
                video_id = match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                webbrowser.open(video_url)
                print(f"Playing '{video}' on YouTube.")
                speak_response(f"Playing '{video}' on YouTube.")
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
        "my portfolio": "https://imtulip.vercel.app/",
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

def fetch_news():
    categories = {
        'Top Stories': 'https://news.google.com/news/rss',
        'World': 'https://news.google.com/news/rss/headlines/section/topic/WORLD',
        'Business': 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS',
        'Technology': 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY',
        'Entertainment': 'https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT',
        'Sports': 'https://news.google.com/news/rss/headlines/section/topic/SPORTS',
        'Science': 'https://news.google.com/news/rss/headlines/section/topic/SCIENCE',
        'Health': 'https://news.google.com/news/rss/headlines/section/topic/HEALTH'
    }

    news_dict = {}

    for category, url in categories.items():
        feed = feedparser.parse(url)
        news_dict[category] = [entry.title for entry in feed.entries[:3]]

    return news_dict

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
    url = f"https://www.instagram.com/{urllib.parse.quote(query)}/"
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


def handle_help_command():
    print(Fore.GREEN + "\nAvailable Commands:")

    # Help command
    print(Fore.GREEN + "    - help: Display this help message")

    # Open command
    print(Fore.GREEN + "    - open [app_name]: Open a specified application")
    print(Fore.GREEN + "      Example: 'open Chrome'")

    # Current time command
    print(Fore.GREEN + "    - what time is it or current time: Display the current time")

    # Play music command
    print(Fore.GREEN + "    - play music: Play relaxing music on YouTube")

    # Search command
    print(Fore.GREEN + "    - search [query]: Search for a specific query")
    print(Fore.GREEN + "      Example: 'search Python tutorials on YouTube'")

    # Add task to to-do list command
    print(Fore.GREEN + "    - add [task] on my todo: Add a task to the to-do list")
    print(Fore.GREEN + "      Example: 'add Complete homework on Math'")

    # View to-do list command
    print(Fore.GREEN + "    - what's in my todo or what in my todo: View the tasks in your to-do list")

    # Complete task command
    print(Fore.GREEN + "    - complete task [task_number]: Mark a task as completed")
    print(Fore.GREEN + "      Example: 'complete task 2'")

    # Delete task command
    print(Fore.GREEN + "    - delete task [task_number]: Delete a task from your to-do list")
    print(Fore.GREEN + "      Example: 'delete task 3'")

    # Fetch news command
    print(Fore.GREEN + "    - fetch news or what's the news: Fetch the latest news headlines")

    # Add event to calendar command
    print(Fore.GREEN + "    - add event to calendar or add event: Add an event to your calendar")

    # List events command
    print(Fore.GREEN + "    - list events or event details: View upcoming events on your calendar")

    # Quit or exit command
    print(Fore.GREEN + "    - quit, exit, sleep, deactivate: Terminate the program")
