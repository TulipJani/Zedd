import pygame
import time
import speech_recognition as sr  # Add this import statement

pygame.mixer.init()
current_music_index = -1  
def ensure_mixer_initialized(func):
    def wrapper(*args, **kwargs):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        return func(*args, **kwargs)
    return wrapper

@ensure_mixer_initialized
def play_audio(file_path, volume=0.1, mixer=None, resume=False):
    if mixer is None:
        mixer = pygame.mixer
    try:
        mixer.music.load(file_path)
        mixer.music.set_volume(volume)
        if resume:
            mixer.music.unpause()
        else:
            mixer.music.play(-1)
        while mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        print(f"Error playing audio: {e}")

@ensure_mixer_initialized
def stop_audio(mixer):
    mixer.music.stop()
    pygame.mixer.quit()

def play_audio_background(file_path, mixer_instance, resume=False):
    if not resume:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.unpause()

@ensure_mixer_initialized
def change_background_music(music_files, mixer_instance):
    global current_music_index
    if not music_files:
        return
    current_music_index = (current_music_index + 1) % len(music_files)
    next_file = music_files[current_music_index]
    play_audio_background(next_file, mixer_instance)


def speechRecognition():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 3000  # Lowered threshold for better sensitivity
        print("Listening...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    
    try:
        # Try recognizing with Indian English
        text = recognizer.recognize_google(audio, language="en-IN")
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        # If Indian English fails, try with general English
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Could you please repeat?")
            return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""