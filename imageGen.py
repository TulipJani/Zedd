import requests
import base64
import os
import tempfile
from PIL import Image
from io import BytesIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')
AUTH_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

def generate_image(prompt, num_steps=4):
    """Generates an image from a text prompt using Cloudflare AI."""
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "num_steps": num_steps  # Default is 4, max is 8
    }
    
    response = requests.post(API_URL, headers=headers, json=payload, verify=False)
    
    if response.status_code == 200:
        try:
            result = response.json()  # Parse JSON response
            if 'image' in result['result']:  # Check if 'image' key exists in result
                image_data = result['result']['image']  # Get the Base64 encoded image
                return base64.b64decode(image_data)  # Decode Base64 to binary data
            else:
                print("No image found in response.")
        except ValueError as e:
            print(f"Error processing response: {e}")
            print("Response content:", response.text)  # Print raw response for debugging
    else:
        print(f"API Error: {response.status_code} - {response.text}")

def save_image(image_data):
    """Saves the image data to a temporary file and returns the file path."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_data)
        return temp_file.name

def display_image(image_path):
    """Opens the generated image using the default image viewer."""
    try:
        img = Image.open(image_path)
        img.show()  # This will open the image in the default viewer
    except Exception as e:
        print(f"Could not open the image: {e}")

def imageGen(imagePrompt):
    """Main function to run the conversational image generation."""
    print("Welcome to the Image Generator!")
    
    while True:
        # prompt = input("Please enter a description for the image (or type 'exit' to quit): ")

        prompt = imagePrompt
        
        if prompt.lower() == 'exit':
            print("Goodbye!")
            break
        
        print("Generating your image...")
        image_data = generate_image(prompt)
        
        if image_data:
            image_path = save_image(image_data)
            print(f"Image generated and saved to: {image_path}")
            display_image(image_path)
        break
if __name__ == "__main__":
    imageGen("redull cinematic shot")