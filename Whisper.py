import requests
import numpy as np
import sounddevice as sd
import wave
import keyboard  # To detect key presses
import time

ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')
AUTH_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/openai/whisper"

def record_audio():
    """Records audio from the microphone while the spacebar is pressed."""
    print("Press and hold the SPACEBAR to start recording...")
    
    # Set parameters for recording
    sample_rate = 16000  # Sample rate in Hz
    audio_frames = []

    while True:
        if keyboard.is_pressed('space'):
            start_time = time.time()  # Record the start time
            audio_frames = []  # Clear previous frames
            
            while keyboard.is_pressed('space'):
                # Record for a short duration (e.g., 1 second)
                frames = sd.rec(int(sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
                sd.wait()  # Wait until recording is finished
                audio_frames.append(frames)
                
                # Check if spacebar is released
                if not keyboard.is_pressed('space'):
                    break
            
            duration = time.time() - start_time
            
            if duration < 2:
                print("Hold longer! Recording stopped.")
                return np.array([]), sample_rate  # Return empty array if not held long enough
            
            print("Finished recording.")
            # Convert frames to a single numpy array
            audio_data = np.concatenate(audio_frames, axis=0)
            return audio_data, sample_rate

def save_audio_to_file(audio_data, sample_rate, filename="recorded_audio.wav"):
    """Saves the recorded audio data to a WAV file."""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(sample_rate)  # Sample rate of 16 kHz
        wf.writeframes(audio_data.tobytes())
    
    return filename

def transcribe_audio(audio_file_path):
    """Transcribes audio using the Whisper model."""
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = list(audio_file.read())  # Convert binary data to a list of integers (0-255)
    
    payload = {
        "audio": audio_data,
        "source_lang": "en",         # Specify source language
        "target_lang": "en"          # Specify target language (currently only English)
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, verify=False)    
    if response.status_code == 200:
        try:
            result = response.json()  # Parse JSON response
            if 'text' in result['result']:  # Check if 'text' key exists in result
                return result['result']['text']  # Get the transcription text
            else:
                print("No transcription found in response.")
        except ValueError as e:
            print(f"Error processing response: {e}")
            print("Response content:", response.text)  # Print raw response for debugging
    else:
        print(f"API Error: {response.status_code} - {response.text}")

def recordAndWhisper():
    """Main function to run the conversational audio transcription."""
    audio_data, sample_rate = record_audio()  # Record audio until space is pressed
    
    if len(audio_data) == 0:
        print("No audio recorded. Please try again.")
        return
    
    audio_file_path = save_audio_to_file(audio_data, sample_rate)  # Save recorded audio to a file
    
    transcription = transcribe_audio(audio_file_path)  # Transcribe the saved audio
    
    if transcription:
        transcription = transcription.lower().strip()
        print(transcription)
        return transcription

if __name__ == "__main__":
    recordAndWhisper()