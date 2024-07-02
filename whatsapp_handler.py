import pywhatkit as kit
import pyautogui
import time

def send_whatsapp_message(phone_no, message):
    try:
        kit.sendwhatmsg_instantly(phone_no, message)
        time.sleep(15) 
        pyautogui.press('enter') 
        print(f"Message sent to {phone_no} successfully.")
    except Exception as e:
        print(f"Failed to send message to {phone_no}: {str(e)}")

def send_scheduled_whatsapp_message():
    phone_no = input("Enter phone number (with country code): ")
    time_info = input("Enter time (HH:MM): ")
    message = input("Enter the message: ")
    try:
        time_parts = time_info.split(":")
        time_hour = int(time_parts[0])
        time_min = int(time_parts[1])
        kit.sendwhatmsg(phone_no, message, time_hour, time_min)
        time.sleep(20)  # Adjust sleep time to ensure WhatsApp is ready
        pyautogui.press('enter')  # Simulate pressing enter key
        print(f"Scheduled message sent to {phone_no} for {time_hour}:{time_min} successfully.")
    except IndexError:
        print("Error: Please provide the phone number, time (HH:MM), and message.")
    except ValueError:
        print("Error: Time must be in HH:MM format.")
    except Exception as e:
        print(f"Failed to send scheduled message to {phone_no}: {str(e)}")

def send_whatsapp_image():
    phone_no = input("Enter phone number (with country code): ")
    image_path = input("Enter the image path: ")
    caption = input("Enter the caption (optional): ")
    try:
        kit.sendwhatsappimage(phone_no, image_path, caption)
        time.sleep(15)  # Wait for WhatsApp to open and load the image
        pyautogui.press('enter')  # Simulate pressing enter key
        print(f"Image sent to {phone_no} successfully.")
    except Exception as e:
        print(f"Failed to send image to {phone_no}: {str(e)}")
