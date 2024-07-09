import pyaudio
import numpy as np
from asciimatics.screen import Screen
import math
import time

# Function to capture audio
def capture_audio(screen):
    CHUNK = 2048  # Increased chunk size for more detailed waveform
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    try:
        while True:
            data = stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Normalize audio data
            normalized_data = audio_data / np.max(np.abs(audio_data))
            
            # Render waveform ASCII art
            render_waveform(screen, normalized_data)
            screen.refresh()
            
            time.sleep(0.04)  # Adjust sleep time for slower animation
            
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

def render_waveform(screen, data):
    screen.clear()
    rows, cols = screen.dimensions
    amplitude = rows // 5  # Adjust amplitude for smaller size and better visibility
    
    # Scale and adjust data for visualization
    scaled_data = np.int16(data * amplitude * 0.8)  # Adjust scaling factor
    
    # Draw waveform
    for i in range(cols):
        index = math.floor((len(scaled_data) / cols) * i)
        y = amplitude + scaled_data[index]
        screen.print_at('▒', i, y, colour=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK)
    
    screen.refresh()

# Main function to initialize the terminal and start capturing audio
def main(screen):
    screen.set_title("Audio Waveform Animation")
    capture_audio(screen)

Screen.wrapper(main)
