from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()  # Use `webdriver.Firefox()` if using GeckoDriver
        self.login()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            username_input = driver.find_element(By.NAME, "username")
            password_input = driver.find_element(By.NAME, "password")

            username_input.send_keys(self.username)
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            
            WebDriverWait(driver, 20).until(
                EC.url_to_be("https://www.instagram.com/")
            )
            
            print("Successfully logged in!")
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            self.close_browser()


    def send_message(self, recipient, message):
        driver = self.driver
        driver.get("https://www.instagram.com/direct/inbox/")
        
        try:
            # Close the popup if it appears
            close_popup_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            close_popup_button.click()
        except Exception as e:
            print(f"Popup not found or couldn't be closed: {str(e)}")
        
        try:
            # Wait for the search box to be visible
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            search_box.send_keys(recipient)
            
            # Wait for the user to appear in the search results
            user = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='option']"))
            )
            user.click()
            
            # Wait for the next button to be clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
            )
            next_button.click()
            
            # Wait for the message box to be visible
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
            )
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
        
        self.close_browser()

    def close_browser(self):
        self.driver.quit()

if __name__ == "__main__":
    ig_bot = InstagramBot("krrrish_xd", "hehe:)")
    ig_bot.login()
    ig_bot.send_message("imtulip.xyz", "Hello from your bot!")
    ig_bot.close_browser()
    print("bye")
