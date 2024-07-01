import pygame
from config import AUDIO_FILE_PATH, BACKGROUND_MUSIC_FILES
from audio import stop_audio, change_background_music
from chat import get_response_with_prompt, switch_persona
from search import handle_search
from weather import get_weather
from utils import terminate_program, open_application, play_song, play_song_on_spotify, google_search, speak_response
import sys
from datetime import datetime, timedelta
import time
import threading
from calendar_handler import initialize_calendar, add_event, list_events
from web_scraper import fetch_news  # Import the fetch_news function
from pyvirtualdisplay import Display
from whatsapp_handler import send_whatsapp_message, send_scheduled_whatsapp_message, send_whatsapp_image

# Initialize pygame mixer
pygame.mixer.init()

# To-do list file
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
        time.sleep(60 * 30)  # Remind every 30 minutes
        tasks = get_todo_list()
        if tasks:
            pending_tasks = "\n".join(f"- {task}" for task in tasks)
            speak_response("You have pending tasks in your to-do list.")
            print(f"Zedd: You have pending tasks:\n{pending_tasks}")

def play_music(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)  # -1 to loop indefinitely
    pygame.mixer.music.set_volume(.1)

def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

def unpause_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

def change_music():
    change_background_music(BACKGROUND_MUSIC_FILES, pygame.mixer.music)


def main():
    is_music_playing = False
    command_count = 0
    # Start reminder thread
    threading.Thread(target=remind_todo, daemon=True).start()

    # Start playing background music
    play_music(AUDIO_FILE_PATH)
    is_music_playing = True

    print("Zedd: Hi there, I'm Zedd.")
    while True:
        user_input = input("You: ")

        command_count += 1

        if any(command in user_input for command in ["quit", "exit", "sleep", "deactivate"]):
            terminate_program()
            break

        elif user_input.startswith("switch to "):
            persona_name = user_input.split("switch to ")[1].strip().title()
            switch_persona(persona_name)
            print(f"Zedd: Switched to {persona_name}.")


        elif user_input.startswith("open "):
            app_to_open = user_input[5:].strip()
            open_application(app_to_open)

        elif "tell me about the weather" in user_input.lower() or "what's the weather today" in user_input.lower():
            response = get_weather()
            print(f"Zedd: {response}")

        elif "what time is it" in user_input or "current time" in user_input:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"Zedd: The current time is {current_time}")
            speak_response(f"The current time is {current_time}")

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
                        print(f"Unsupported platform: {platform}. Supported platforms are 'spotify' and 'youtube'.")
                else:
                    print("Invalid command format. Please specify the song title and platform.")
            else:
                play_song(song_info)

        elif user_input.startswith("google "):
            query = user_input[7:]
            google_search(query)

        elif user_input.startswith("search for ") or user_input.startswith("search "):
            results = handle_search(user_input)
            print(f"Zedd: {results}")

        elif user_input.startswith("add ") and "on my todo" in user_input:
            task = user_input[4:user_input.index("on my todo")].strip()
            add_to_todo(task)
            print(f"Zedd: Added '{task}' to your to-do list.")

        elif "what's in my todo" in user_input.lower() or "what in my todo" in user_input.lower():
            pending_tasks, completed_tasks = get_todo_list()
            if pending_tasks:
                tasks_text = "\n".join(f"{i+1}. {task.strip()}" for i, task in enumerate(pending_tasks))
                print(f"Zedd: You have pending tasks:\n{tasks_text}")
                speak_response(f"You have pending tasks. {tasks_text}")
            else:
                print("Zedd: Your to-do list is empty.")
                speak_response("Your to-do list is empty.")

        elif user_input.startswith("complete task "):
            try:
                task_index = int(user_input.split()[2]) - 1
                mark_task_completed(task_index)
                print(f"Zedd: Marked task {task_index + 1} as completed.")
                speak_response(f"Zedd: Marked task {task_index + 1} as completed.")
            except IndexError:
                print("Zedd: Task index out of range.")
                speak_response("Zedd: Task index out of range.")
            except ValueError:
                print("Zedd: Invalid command format. Use 'complete task <task number>'.")
                speak_response("Zedd: Invalid command format. Use 'complete task <task number>'.")

        elif user_input.startswith("delete task "):
            try:
                task_index = int(user_input.split()[2]) - 1
                delete_task(task_index)
                print(f"Zedd: Deleted task {task_index + 1}.")
                speak_response(f"Zedd: Deleted task {task_index + 1}.")
            except IndexError:
                print("Zedd: Task index out of range.")
                speak_response("Zedd: Task index out of range.")
            except ValueError:
                print("Zedd: Invalid command format. Use 'delete task <task number>'.")
                speak_response("Zedd: Invalid command format. Use 'delete task <task number>'.")

        elif user_input.lower() == "pause music":
            pause_music()
            print("Zedd: Music paused.")

        elif user_input.lower() == "resume music":
            unpause_music()
            print("Zedd: Music playing.")
        elif user_input.lower() == "change music" :
            change_music()
            print("Zedd: Background music changed.")
            speak_response("Background music changed.")

        elif user_input.startswith("add event to calendar") or user_input.startswith("add event"):
            service = initialize_calendar()
            add_event(service)  # Pass service object to add_event function

        elif user_input.startswith("list events") or user_input.startswith("event details"):
            service = initialize_calendar()
            list_events(service) 

        elif user_input.lower().startswith(("fetch news", "get news", "what's the news")):
            print("Zedd: Fetching the latest news. Please wait...")
            news = fetch_news()
            if news:
                print("Zedd: Here are the top headlines in various categories:")
                for category, headlines in news.items():
                    print(f"\n{category}:")
                    for i, headline in enumerate(headlines, 1):
                        print(f"{i}. {headline}")
                    speak_response(f"Top headline in {category}: {headlines[0]}")
            else:
                print("Zedd: I'm sorry, I couldn't fetch any news at the moment.")
                speak_response("I'm sorry, I couldn't fetch any news at the moment.")

        elif user_input.startswith("send whatsapp message"):
            parts = user_input.split(maxsplit=4)
            phone_no = parts[3]
            message = parts[4]
            send_whatsapp_message(phone_no, message)
            
        elif user_input.startswith("schedule whatsapp message"):
            parts = user_input.split(maxsplit=5)
            phone_no = parts[3]
            time_info = parts[4]
            message = parts[5]
            time_parts = time_info.split(":")
            time_hour = int(time_parts[0])
            time_min = int(time_parts[1])
            send_scheduled_whatsapp_message(phone_no, message, time_hour, time_min)
        
        elif user_input.startswith("send whatsapp image"):
            parts = user_input.split(maxsplit=5)
            phone_no = parts[3]
            image_path = parts[4]
            caption = parts[5] if len(parts) > 5 else ""
            send_whatsapp_image(phone_no, image_path, caption)


        else:
            generated_response = get_response_with_prompt(user_input)
            print(f"Zedd: {generated_response}")

        if command_count % 10 == 0:
            pending_tasks, completed_tasks = get_todo_list()
            if pending_tasks:
                tasks_text = "\n".join(f"- {task}" for task in pending_tasks)
                print(f"Zedd: You have pending tasks:\n{tasks_text}")
                speak_response(f"You have pending tasks. {tasks_text}")
            else:
                print("Zedd: Your to-do list is empty.")
                speak_response("Your to-do list is empty.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        terminate_program()
