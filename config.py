import os
import pyttsx3
# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 200)  # Adjust rate for more natural speed
engine.setProperty('volume', 1)  # Adjust volume for clarity

# Set the dimensions of the window
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# Set up the left and right sections of the screen
LEFT_WIDTH = int(SCREEN_WIDTH * 0.45)
RIGHT_WIDTH = SCREEN_WIDTH - LEFT_WIDTH

CITY_NAME = 'Ahmedabad'

# VOSK Model Path
VOSK_MODEL_PATH = "vosk-model-en-in-0.5/vosk-model-en-in-0.5"

# Audio File Path
AUDIO_FILE_PATH = "D:/CodeVerse/geminiAI/audioo/bg.mp3"

# Load images
FRAME_COUNT = 24
FRAMES_DIR = 'frames'
FRAMES = [f'{FRAMES_DIR}/{i:04}.png' for i in range(1, FRAME_COUNT + 1) if os.path.exists(f'{FRAMES_DIR}/{i:04}.png')]

for voice in engine.getProperty('voices'):
    if "Microsoft David Desktop - English (United States)" in voice.name:
        engine.setProperty('voice', voice.id)
        break
