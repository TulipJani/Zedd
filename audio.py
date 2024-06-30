import pygame
import time
import random
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
            mixer.music.unpause()  # Resume the music if it's paused
        else:
            mixer.music.play(-1)  # Play the music from the beginning
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
        pygame.mixer.music.play(-1)  # -1 to loop indefinitely
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
