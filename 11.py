from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    # Setup Chrome options for headless mode
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Automatically download and setup the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    return driver

def speak(text):
    driver = setup_driver()
    
    try:
        # Open the ElevenLabs website
        driver.get("https://elevenlabs.io/")
        
        # Wait until the textarea is present
        wait = WebDriverWait(driver, 10)
        textarea = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div[2]/div[1]/div[3]/div/div/div[1]/div[2]/div/div/textarea')))
        
        # Enter the text into the textarea
        textarea.clear()
        textarea.send_keys(text)
        
        # Wait until the button is present
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div/div[2]/div[1]/div[3]/div/div/div[1]/div[2]/div/div/div[3]/button[2]')))
        
        # Click the button
        button.click()
        
        # Wait for a few seconds to let the action complete
        time.sleep(5)
        
    finally:
        # Close the browser
        driver.quit()

# Example usage
speak("Hello, this is a test.")
