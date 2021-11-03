import speech_recognition as sr
import pyttsx3
import  os
import re
import RPi.GPIO as GPIO
import time
from os import path
import subprocess
from gtts import gTTS
from googletrans import Translator
from playsound import playsound  
#import wikipedia
led =7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT, initial=GPIO.HIGH)    

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

voice_data =""

translator = Translator()


def stringtolist(string):
    listres = list(string.split(" "))
    return listres
def talk_gtts(text_val,language):
    
    language = language 
    obj = gTTS(text=text_val, lang=language, slow=False)
    obj.save("exam.mp3")  
    playsound("exam.mp3")
    os.remove("exam.mp3")

def talk(text):
    engine.say(text)
    engine.runAndWait()

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True
def take_command():
  
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        #print(r.energy_threshold)
        #print("Chucking rate: ", source.CHUNK)
        #print("format rate :", source.format)

        for i in range(7):
            GPIO.output(led, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(led,GPIO.LOW)
            time.sleep(0.1)
        #print(r.energy_threshold)
        r.energy_threshold += 280
        # # print(r.adjust_for_ambient_noise(source,duration=1))
        audio = r.listen(source)
        
        GPIO.output(led, GPIO.HIGH)
        # Speech recognition using Google Speech Recognition
    try:
        #print("Parsing ...")  # Debugging To
        voice_data = r.recognize_google(audio)
        '''output_language = translator.translate(voice_data)
        language = output_language.src
        if language != 'en':
            voice_data = output_language.text
            print(voice_data)'''
        language = "en"
        #return voice_data.lower(), language  # returning the text which has been inputed.
        return voice_data

    except sr.UnknownValueError:
        talk_gtts("Speech Recognition could not understand audio","en")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
def change_language(S_text, language):
    trans3 = translator.translate(S_text,dest = language)
    print(trans3.text)
    talk_gtts(trans3.text,language)

