import os
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 200) 
engine.setProperty('volume', 1) 

CITY_NAME = 'Ahmedabad'

AUDIO_FILE_PATH = "audioo/erevald.mp3"

BACKGROUND_MUSIC_FILES = [
    "audioo/alterok.mp3",
    "audioo/erevald.mp3",
    "audioo/gaudmire.mp3",
    "audioo/spectreseek.mp3",
]
