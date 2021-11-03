import pyautogui
import time 
from robo_tts import take_command as takeCommand
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def whatsapp():
    query = takeCommand().lower()
    if 'y' in query:
        pyautogui.moveTo(250,1200) 
        pyautogui.click()
        time.sleep(1)
        pyautogui.write('whatsapp')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.moveTo(100,140)   
        pyautogui.click() 
        speak('To whom you want to send message,.....just write the name here in 5 seconds')
        time.sleep(7)
        pyautogui.moveTo(120,300)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(800,990)
        pyautogui.click()
        speak('Say the message,....or if you want to send anything else,...say send document, or say send emoji')
        query = takeCommand()
        if ('sent' in query or 'send' in query) and 'document' in query:
            pyautogui.moveTo(660,990)   
            pyautogui.click() 
            time.sleep(1)
            pyautogui.moveTo(660,740)
            pyautogui.click()
            speak('please select the document within 10 seconds')
            time.sleep(12)
            speak('Should I send this document?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('sending the document......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('document' in query or 'message' in query or 'it' in query or 'emoji' in query or 'select' in query):
                pyautogui.doubleClick(x=800, y=990)
                pyautogui.press('backspace')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
        elif ('sent' in query or 'send' in query) and 'emoji' in query:
            pyautogui.moveTo(620,990)  
            pyautogui.click() 
            pyautogui.moveTo(670,990)
            pyautogui.click()
            pyautogui.moveTo(650,580) 
            pyautogui.click()
            speak('please select the emoji within 10 seconds')
            time.sleep(11)
            speak('Should I send this emoji?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('Sending the emoji......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('message' in query or 'it' in query or 'emoji' in query or 'select' in query):
                pyautogui.doublClick(x=800, y=990)
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
        else:
            pyautogui.write(f'{query}')
            speak('Should I send this message?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('sending the message......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('message' in query or 'it' in query or 'select' in query):
                pyautogui.doubleClick(x=800, y=990)               
                pyautogui.press('backspace')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
    else:
        speak('ok')