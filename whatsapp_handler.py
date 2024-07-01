import pywhatkit

try:
    pywhatkit.sendwhatmsg("+919428693489","Hello. This is automated message. Somry for disturbing",14, 45)
    print("Successfully Sent!")

except:
    print("An Unexpected Error!")
