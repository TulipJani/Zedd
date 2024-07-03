import pygame
from config import AUDIO_FILE_PATH, BACKGROUND_MUSIC_FILES
from audio import change_background_music
from chat import get_response_with_prompt, switch_persona
from search import handle_search
from weather import get_weather
from utils import terminate_program, open_application, play_song, play_song_on_spotify, google_search, speak_response
from datetime import datetime
import time
import threading
from calendar_handler import initialize_calendar, add_event, list_events
from web_scraper import fetch_news
from whatsapp_handler import send_whatsapp_message
import sys
import random
import shutil
from colorama import Fore, init
from blessed import Terminal

class NullWriter(object):
    def write(self, arg):
        pass

sys.stdout = NullWriter()
sys.stdout = sys.__stdout__
init(autoreset=True)
pygame.mixer.init()
ascii_art = """
                                                           
###### ###### #####  #####     #    # ###### #####  ###### 
    #  #      #    # #    #    #    # #      #    # #      
   #   #####  #    # #    #    ###### #####  #    # #####  
  #    #      #    # #    #    #    # #      #####  #      
 #     #      #    # #    #    #    # #      #   #  #      
###### ###### #####  #####     #    # ###### #    # ###### 
                                                           

"""
def show_loading_animation():
    total_length = 50

    terminal_width = shutil.get_terminal_size().columns

    for percent in range(101):
        bar = ('#' * (percent * total_length // 100)).ljust(total_length)
        speed = random.uniform(10, 50)

        progress = f"Progress: |{bar}| {percent}%"
        speed_info = f"Speed: {speed:.2f} KB/s"



        sys.stdout.write(f"\r{progress} {speed_info}".ljust(terminal_width))
        sys.stdout.flush()
        time.sleep(0.1)


    print("\n")

def handle_help_command():
    print(Fore.GREEN + "\nAvailable Commands:")

    # Help command
    print(Fore.GREEN + "    - help: Display this help message")

    # Open command
    print(Fore.GREEN + "    - open [app_name]: Open a specified application")
    print(Fore.GREEN + "      Example: 'open Chrome'")

    # Play music command
    print(Fore.GREEN + "    - play music: Play relaxing music on YouTube")

    # Weather command
    print(Fore.GREEN + "    - weather: Get the current weather")

    # Add task to to-do list command
    print(Fore.GREEN + "    - add [task]: Add a task to the to-do list")
    print(Fore.GREEN + "      Example: 'add Complete homework on Math'")

    # Schedule command
    print(Fore.GREEN + "    - schedule: Display today's schedule")

    # Send WhatsApp message command
    print(Fore.GREEN + "    - send [message] to [contact]: Send a WhatsApp message")
    print(Fore.GREEN + "      Example: 'send Hi there! to Mom'")

    # Search command
    print(Fore.GREEN + "    - search [query] on [platform]: Search on specified platform")
    print(Fore.GREEN + "      Example: 'search Python tutorials on YouTube'")

    # Play playlist command
    print(Fore.GREEN + "    - play [playlist]: Play a playlist on Spotify")
    print(Fore.GREEN + "      Example: 'play Chill Out playlist'")

    # News command
    print(Fore.GREEN + "    - news: Get the latest news")

    # Switch persona command
    print(Fore.GREEN + "    - switch to [persona]: Switch to a different assistant persona")
    print(Fore.GREEN + "      Example: 'switch to Creative Zedd'")


TODO_FILE = "todo.txt"
def add_to_todo(task):
    with open(TODO_FILE, "a") as file:
        file.write(f"{task}\n")

def get_todo_list():
    try:
        with open(TODO_FILE, "r") as file:
            tasks = [task.strip() for task in file.readlines()]
            pending_tasks = [task for task in tasks if not task.startswith("[Completed]")]
            completed_tasks = [task for task in tasks if task.startswith("[Completed]")]
            return pending_tasks, completed_tasks
    except FileNotFoundError:
        return [], []
    
def delete_task(task_index):
    pending_tasks, completed_tasks = get_todo_list()
    if task_index < len(pending_tasks):
        del pending_tasks[task_index]
        with open(TODO_FILE, "w") as file:
            file.write("\n".join(pending_tasks + completed_tasks))

def mark_task_completed(task_index):
    pending_tasks, completed_tasks = get_todo_list()
    if task_index < len(pending_tasks):
        completed_tasks.append(f"[Completed] {pending_tasks[task_index]}")
        del pending_tasks[task_index]
        with open(TODO_FILE, "w") as file:
            file.write("\n".join(pending_tasks + completed_tasks))

def remind_todo():
    while True:
        time.sleep(60 * 30)

        tasks = get_todo_list()
        if tasks:
            pending_tasks = "\n".join(f"- {task}" for task in tasks)
            speak_response("You have pending tasks in your to-do list.")
            print(Fore.GREEN + f"Zedd: You have pending tasks:\n{pending_tasks}")

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)

    pygame.mixer.music.set_volume(.1)

def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def unpause_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

def change_music():
    change_background_music(BACKGROUND_MUSIC_FILES, pygame.mixer.music)

contacts = {
    "bhai": "+919428693489",
    "papa": "+918000114615",
    "mummy": "+919428718551",
    "prachi": "+12042152409",
}
def process_input(user_input):
    if user_input.startswith("send me"):
        topic = user_input[len("send me "):]
        response = get_response_with_prompt(topic)
        send_whatsapp_message("+919081321913", response)
    elif user_input.startswith("send"):
        parts = user_input.split(maxsplit=3)
        if len(parts) == 4 and parts[2] == "to":
            topic = parts[1]
            contact_name = parts[3]
            if contact_name in contacts:
                phone_no = contacts[contact_name]
                response = get_response_with_prompt(topic)
                send_whatsapp_message(phone_no, response)
            else:
                print(Fore.GREEN + f"Contact {contact_name} not found in contacts.")
        else:
            print(Fore.GREEN + "Error: Please provide the correct command format like 'send topic to contact name'.")
def main():
    is_music_playing = False
    command_count = 0

    threading.Thread(target=remind_todo, daemon=True).start()


    play_music(AUDIO_FILE_PATH)
    is_music_playing = True
    print(Fore.YELLOW + ascii_art)

    print(Fore.GREEN + "Zedd: Hi there, I'm Zedd.")
    handle_help_command()
    while True:
        user_input = input("You: ")

        command_count += 1

        if any(command in user_input for command in ["quit", "exit", "sleep", "deactivate"]):
            terminate_program()
            break

        elif user_input.startswith("switch to "):
            persona_name = user_input.split("switch to ")[1].strip().title()
            switch_persona(persona_name)
            print(Fore.GREEN + f"Zedd: Switched to {persona_name}.")


        elif user_input.startswith("open "):
            app_to_open = user_input[5:].strip()
            open_application(app_to_open)

        elif "tell me about the weather" in user_input.lower() or "what's the weather today" in user_input.lower():
            response = get_weather()
            print(Fore.GREEN + f"Zedd: {response}")

        elif "what time is it" in user_input or "current time" in user_input:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(Fore.GREEN + f"Zedd: The current time is {current_time}")

        elif user_input.startswith(("play", "stream", "start", "broadcast")):
            command, song_info = user_input.split(maxsplit=1)
            if "on" in song_info:
                parts = list(map(str.strip, song_info.rsplit("on", 1)))
                if len(parts) == 2:
                    song_title, platform = parts
                    platform = platform.lower()

                    if platform == "spotify":
                        play_song_on_spotify(song_title)
                    elif platform == "youtube":
                        play_song(song_title)
                    else:
                        print(Fore.GREEN + f"Unsupported platform: {platform}. Supported platforms are 'spotify' and 'youtube'.")
                else:
                    print(Fore.GREEN + "Invalid command format. Please specify the song title and platform.")
            else:
                play_song(song_info)

        elif user_input.startswith("google "):
            query = user_input[7:]
            google_search(query)

        elif user_input.startswith("search for ") or user_input.startswith("search "):
            results = handle_search(user_input)
            print(Fore.GREEN + f"Zedd: {results}")

        elif user_input.startswith("add ") and "on my todo" in user_input:
            task = user_input[4:user_input.index("on my todo")].strip()
            add_to_todo(task)
            print(Fore.GREEN + f"Zedd: Added '{task}' to your to-do list.")

        elif "what's in my todo" in user_input.lower() or "what in my todo" in user_input.lower():
            pending_tasks, completed_tasks = get_todo_list()
            if pending_tasks:
                tasks_text = "\n".join(f"{i+1}. {task.strip()}" for i, task in enumerate(pending_tasks))
                print(Fore.GREEN + f"Zedd: You have pending tasks:\n{tasks_text}")
                speak_response(f"You have pending tasks. {tasks_text}")
            else:
                print(Fore.GREEN + "Zedd: Your to-do list is empty.")
                speak_response("Your to-do list is empty.")

        elif user_input.startswith("complete task "):
            try:
                task_index = int(user_input.split()[2]) - 1
                mark_task_completed(task_index)
                print(Fore.GREEN + f"Zedd: Marked task {task_index + 1} as completed.")
                speak_response(f"Zedd: Marked task {task_index + 1} as completed.")
            except IndexError:
                print(Fore.GREEN + "Zedd: Task index out of range.")
                speak_response("Zedd: Task index out of range.")
            except ValueError:
                print(Fore.GREEN + "Zedd: Invalid command format. Use 'complete task <task number>'.")
                speak_response("Zedd: Invalid command format. Use 'complete task <task number>'.")

        elif user_input.startswith("delete task "):
            try:
                task_index = int(user_input.split()[2]) - 1
                delete_task(task_index)
                print(Fore.GREEN + f"Zedd: Deleted task {task_index + 1}.")
                speak_response(f"Zedd: Deleted task {task_index + 1}.")
            except IndexError:
                print(Fore.GREEN + "Zedd: Task index out of range.")
                speak_response("Zedd: Task index out of range.")
            except ValueError:
                print(Fore.GREEN + "Zedd: Invalid command format. Use 'delete task <task number>'.")
                speak_response("Zedd: Invalid command format. Use 'delete task <task number>'.")

        elif user_input.lower() == "pause music":
            pause_music()
            print(Fore.GREEN + "Zedd: Music paused.")

        elif user_input.lower() == "resume music":
            unpause_music()
            print(Fore.GREEN + "Zedd: Music playing.")
        elif user_input.lower() == "change music" :
            change_music()
            print(Fore.GREEN + "Zedd: Background music changed.")
            speak_response("Background music changed.")

        elif user_input.startswith("add event to calendar") or user_input.startswith("add event"):
            service = initialize_calendar()
            add_event(service)


        elif user_input.startswith("list events") or user_input.startswith("event details"):
            service = initialize_calendar()
            list_events(service) 

        elif user_input.lower().startswith(("fetch news", "get news", "what's the news")):
            print(Fore.GREEN + "Zedd: Fetching the latest news. Please wait...")
            news = fetch_news()
            if news:
                print(Fore.GREEN + "Zedd: Here are the top headlines in various categories:")
                for category, headlines in news.items():
                    print(Fore.GREEN + f"\n{category}:")
                    for i, headline in enumerate(headlines, 1):
                        print(Fore.GREEN + f"{i}. {headline}")
                    speak_response(f"Top headline in {category}: {headlines[0]}")
            else:
                print(Fore.GREEN + "Zedd: I'm sorry, I couldn't fetch any news at the moment.")
                speak_response("I'm sorry, I couldn't fetch any news at the moment.")

        elif user_input.startswith("send") :
            process_input(user_input=user_input)

        else:
            generated_response = get_response_with_prompt(user_input)
            print(Fore.GREEN + f"Zedd: {generated_response}")

        if command_count % 10 == 0:
            pending_tasks, completed_tasks = get_todo_list()
            if pending_tasks:
                tasks_text = "\n".join(f"- {task}" for task in pending_tasks)
                print(Fore.GREEN + f"Zedd: You have pending tasks:\n{tasks_text}")
                speak_response(f"You have pending tasks. {tasks_text}")
            else:
                print(Fore.GREEN + "Zedd: Your to-do list is empty.")
                speak_response("Your to-do list is empty.")

if __name__ == "__main__":
    terminal = Terminal()


    print(terminal.clear())
    with terminal.hidden_cursor(), terminal.cbreak():
        print(Fore.YELLOW + ascii_art)
        for i in range(2):
            sys.stdout.write(Fore.GREEN + f"\rZedd: Loading{'.' * i}{' ' * (4 - i)}")
            sys.stdout.flush()
            time.sleep(0.5)
            for j in range(i):
                show_loading_animation()
                sys.stdout.write(Fore.GREEN + "Loading Succesful")
                time.sleep(1)
            time.sleep(3)
        print(terminal.clear())

    
    
    main()
