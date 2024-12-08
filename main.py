import pygame
import time
import threading
import random
import shutil
import numpy as np
import simpleaudio as sa
from datetime import datetime
from rich.console import Console
from rich.text import Text
from rich.style import Style
from rich.live import Live
from Whisper import recordAndWhisper
from imageGen import imageGen
from chat import get_response_with_prompt
from utils import terminate_program, open_application, play_video_on_youtube, play_song_on_spotify, google_search, speak_response, handle_search, handle_help_command, fetch_news
from Todo import add_to_todo, get_todo_list, delete_task, mark_task_completed, remind_todo

# Create a console instance for rich output
console = Console()

class RetroEffects:
    def __init__(self):
        self.console_width = console.width
        self.console_height = console.height
        self.phosphor_persistence = 0.15
        self.initialize_sounds()

    def initialize_sounds(self):
        """Initialize various sound effects"""
        # Generate boot sound (440Hz for 100ms)
        sample_rate = 44100
        
        # Boot sound (combination of frequencies)
        boot_freq = [440, 880, 1320]
        self.boot_sound = self.generate_sound(boot_freq, duration=0.1)

        # Key press sound (shorter, higher pitch)
        self.key_sound = self.generate_sound([2000], duration=0.02)

        # Error sound (descending tone)
        freq = np.linspace(880, 220, int(sample_rate * 0.2))
        self.error_sound = (np.sin(2 * np.pi * freq * np.linspace(0, 0.2, len(freq))) * 0.15 * 32767).astype(np.int16)

        # Additional sound effects
        self.success_sound = self.generate_sound([523], duration=0.1)  # C5 note for success feedback
        self.warning_sound = self.generate_sound([349], duration=0.1)  # F note for warnings

    def generate_sound(self, frequencies, duration):
        """Generate a sound wave from given frequencies."""
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio = np.zeros(len(t))
        
        for freq in frequencies:
            audio += np.sin(2 * np.pi * freq * t)
        
        audio *= 0.2  # Adjust volume
        return (audio * 32767).astype(np.int16)

    def play_sound(self, audio_data):
        """Play a sound effect"""
        try:
            play_obj = sa.play_buffer(audio_data, 1, 2, 44100)
            threading.Thread(target=play_obj.wait_done).start()
        except Exception as e:
            print(f"Sound playback error: {e}")

    def create_scan_line(self):
        """Create a scan line effect at a random y position"""
        intensity = abs(np.sin(time.time() * 2)) * 0.5 + 0.5
        line = "░" * self.console_width
        return Text(line, style=f"rgb({int(40*intensity)},{int(100*intensity)},{int(40*intensity)})")

    def create_glowing_text(self, text):
        """Create text with a glowing effect"""
        intensity = (abs(np.sin(time.time() * 3)) * 0.3 + 0.7)
        r = int(40 * intensity)
        g = int(200 * intensity)
        b = int(40 * intensity)
        return Text(text, style=f"rgb({r},{g},{b}) bold")

    def loading_animation(self, message):
        """Display a loading animation with phosphor persistence"""
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for _ in range(10):
            for frame in frames:
                text = f"{frame} {message}"
                console.print(self.create_glowing_text(text), end="\r")
                time.sleep(0.025)

    def display_startup_sequence(self):
        """Display an enhanced startup sequence"""
        self.play_sound(self.boot_sound)

        startup_text = [
            "INITIATING BOOT SEQUENCE...",
            "LOADING CORE MODULES...",
            "INITIALIZING MEMORY BANKS...",
            "CALIBRATING CRT DISPLAY...",
            "ESTABLISHING QUANTUM BUFFER...",
            "SYNCHRONIZING FLUX CAPACITORS...",
            "ACTIVATING RETRO PROTOCOLS...",
        ]

        for text in startup_text:
            self.loading_animation(text)
            time.sleep(0.01)

    def create_phosphor_effect(self, text):
        """Create phosphor persistence effect"""
        ghost_text = text.copy()
        ghost_intensity = abs(np.sin(time.time() * 2)) * 0.3 + 0.2
        ghost_text.style = Style(color=f"rgb(0,{int(80*ghost_intensity)},0)")
        return ghost_text

class RetroTerminal:
    def __init__(self):
        self.effects = RetroEffects()
        self.running = True
        self.command_history = []

    def process_command(self, command):
         """Process user commands with enhanced feedback"""
        
         if command == "help":
            return """
Available Commands:
- help                        : Display this help message
- status                      : Show system status
- matrix                      : Display the matrix effect full screen
- clear                       : Clear the screen
- history                     : Show command history
- exit                        : Terminate session
- generate [prompt]           : Generates image
- open [app_name]             : Open a specified application
- play music                  : Play relaxing music on YouTube
- search [query]              : Search for a specific query

            
            """
        
         elif command == "status":
            return f"""System Status:
Display: CRT-9000
Resolution: {self.effects.console_width}x{self.effects.console_height}
Phosphor Level: {self.effects.phosphor_persistence:.2f}
Buffer: OPTIMAL
Quantum State: STABLE"""
        
         elif command == "matrix":
            return self.display_matrix_effect()
        
         elif command == "clear":
            console.clear()
            return "Screen cleared."
        
         elif command == "history":
            return "Command History:\n" + "\n".join(f"{i+1}. {cmd}" for i, cmd in enumerate(self.command_history))
        
         elif command == "exit":
            self.running = False
            return "Initiating shutdown sequence..."
        
         else:
             if any(cmd in command for cmd in ["quit", "exit", "sleep", "deactivate"]):
                 terminate_program()
                 return ""
             
             elif command.startswith("open "):
                 app_to_open = command[5:].strip()
                 open_application(app_to_open)
             elif command.startswith("generate "):
                 imagePrompt = command[8:].strip()
                 imageGen(imagePrompt)

             elif any(x in command for x in ["what time is it", "current time"]):
                 current_time = datetime.now().strftime("%H:%M:%S")
                 return f"The current time is {current_time}"

             elif command.startswith(("play", "stream", "start", "broadcast")):
                 command_parts = command.split(maxsplit=1)
                 if len(command_parts) > 1 and 'on' in command_parts[1]:
                     parts = list(map(str.strip, command_parts[1].rsplit("on", 1)))
                     if len(parts) == 2:
                         title, platform = parts[0], parts[1].lower()
                         if platform == 'spotify':
                             play_song_on_spotify(title)
                             self.effects.play_sound(self.effects.success_sound) 
                             return f"Playing '{title}' on Spotify."
                         elif platform == 'youtube':
                             play_video_on_youtube(title)
                             self.effects.play_sound(self.effects.success_sound) 
                             return f"Playing '{title}' on YouTube."
                         else:
                             return f"Unsupported platform: {platform}. Supported platforms are 'Spotify' and 'YouTube'."
                     else:
                         return f"Invalid command format. Please specify the song title and platform."
                 else:
                     title = command_parts[1]
                     play_video_on_youtube(title)
                     self.effects.play_sound(self.effects.success_sound) 
                     return f"Playing '{title}' on YouTube."

             elif command.startswith("google "):
                 query = command[7:]
                 google_search(query)
                 return f"Searching Google for '{query}'..."

             elif command.startswith("search for ") or command.startswith("search "):
                 results = handle_search(command)
                 return f"Zedd: {results}"

             elif command.startswith("add ") and "on my todo" in command:
                 task_index_start = command.index("on my todo")
                 task_name = command[4:task_index_start].strip()
                 add_to_todo(task_name)
                 return f"Added '{task_name}' to your to-do list."

             elif any(x in command.lower() for x in ["what's in my todo", "what in my todo"]):
                 pending_tasks, completed_tasks = get_todo_list()
                 if pending_tasks:
                     tasks_text = "\n".join(f"{i+1}. {task.strip()}" for i, task in enumerate(pending_tasks))
                     speak_response(f"You have pending tasks: {tasks_text}")
                     return f"You have pending tasks:\n{tasks_text}"
                 else:
                     speak_response("Your to-do list is empty.")
                     return f"Your to-do list is empty."

             elif command.startswith("complete task "):
                 try:
                     task_index = int(command.split()[2]) - 1
                     mark_task_completed(task_index)
                     speak_response(f"Marked task {task_index + 1} as completed.")
                     return f"Marked task {task_index + 1} as completed."
                 except IndexError:
                     speak_response("Task index out of range.")
                     return f"Task index out of range."
                 except ValueError:
                     speak_response("Invalid command format. Use 'complete task <task number>'.")
                     return f"Invalid command format. Use 'complete task <task number>'."

             elif command.startswith("delete task "):
                 try:
                     task_index = int(command.split()[2]) - 1
                     delete_task(task_index)
                     speak_response(f"Deleted task {task_index + 1}.")
                     return f"Deleted task {task_index + 1}."
                 except IndexError:
                     speak_response("Task index out of range.")
                     return f"Task index out of range."
                 except ValueError:
                     speak_response("Invalid command format. Use 'delete task <task number>'.")
                     return f"Invalid command format. Use 'delete task <task number>'."

             elif any(x in command.lower() for x in ["fetch news", "get news", "what's the news"]):
                 news_data = fetch_news()
                 if news_data:
                     news_output_lines = []
                     for category, headlines in news_data.items():
                         news_output_lines.append(f"{category}:")
                         news_output_lines.extend(headlines)
                         speak_response(f"Top headline in {category}: {headlines[0]}")
                     return "\n".join(news_output_lines)
                 else:
                     speak_response("I'm sorry, I couldn't fetch any news at the moment.")
                     return "I'm sorry, I couldn't fetch any news at the moment."

             else:
                generated_response = get_response_with_prompt(command)
                return f"Zedd: {generated_response}"

    def display_matrix_effect(self):
         """Display an extended matrix-like effect covering full screen"""
         characters = "ﾊ ﾐ ﾋ ｰ ｳ ｼ ﾅ ﾓ ﾆ ｻ ﾜ ﾂ ｵ ﾘ ｱ ﾎ ﾃ ﾏ ｹ ﾒ ｴ ｶ ｷ ﾑ ﾕ ﾗ ｾ ﾈ ｽ ﾀ ﾇ ﾍ ﾊ ﾐ ﾋ ｰ ｳ ｼ ﾅ ﾓ ﾆ ｻ ﾜ ﾂ ｵ ﾘ ｱ ﾎ ﾃ ﾏ ｹ ﾒ ｴ ｶ ｷ ﾑ ﾕ ﾗ ｾ ﾈ ｽ ﾀ ﾇ ﾍ"
         with Live(refresh_per_second=20) as live:
            for _ in range(100):  
                text_lines = []
                for _ in range(self.effects.console_height):  
                    line_chars = "".join(random.choice(characters) if random.random() > 0.5 else " "
                                        for _ in range(self.effects.console_width))
                    text_lines.append(line_chars)
                live.update(self.effects.create_glowing_text("\n".join(text_lines)))
                time.sleep(0.05)

         return "Matrix sequence completed." 

    def run(self):
        """Main terminal loop with enhanced effects"""
        console.clear()
        
        # Display Zedd ASCII art and logs initialization.
        zedd_ascii_art = """
        .::::::: .::.::::::::.:::::    .:::::    
               .::  .::      .::   .:: .::   .:: 
              .::   .::      .::    .::.::    .::
            .::     .::::::  .::    .::.::    .::
           .::      .::      .::    .::.::    .::
         .::        .::      .::   .:: .::   .:: 
        .:::::::::::.::::::::.:::::    .:::::    
                                         
        

"""

        console.print(self.effects.create_glowing_text(zedd_ascii_art))
        print("\nInitializing Zedd...\n")
        
        # Display startup sequence with sounds and effects.
        self.effects.display_startup_sequence()

        while self.running:
            scan_pos_line = random.randint(0, self.effects.console_height - 1)  
            console.print(self.effects.create_scan_line(), end="\r")

            prompt_text = "\n► "
            prompt_glow_effects = self.effects.create_glowing_text(prompt_text)

            console.print(prompt_glow_effects, end="")
            
            # Get user input and process commands.
            # user_input_command = input().lower().strip()
            user_input_command = recordAndWhisper()
            self.effects.play_sound(self.effects.key_sound)

            if user_input_command: 
                self.command_history.append(user_input_command) 
                response_message = self.process_command(user_input_command)

                # Only print if response_message is not None
                if response_message:  
                    console.print(self.effects.create_glowing_text(response_message))  # Print glowing text
                    ghost_text = self.effects.create_phosphor_effect(Text(response_message))
               
                    time.sleep(0.1)

if __name__ == "__main__":
    try:
       terminal_instance= RetroTerminal()
       terminal_instance.run()
    except KeyboardInterrupt:
       console.print(RetroEffects().create_glowing_text("\nEmergency shutdown initiated... Goodbye!"))
       time.sleep(1)
