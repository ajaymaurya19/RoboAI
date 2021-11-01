import speech_recognition as sr
import pyttsx3
import  os
import re
from os import path
import subprocess
from gtts import gTTS
from googletrans import Translator
from playsound import playsound  
#import wikipedia

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
    client_id = ""  # this is the google api client id
    client_secret = ""  # this is the google api client secret key
    api_key = ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        #print(r.energy_threshold)
        print("Chucking rate: ", source.CHUNK)
        print("format rate :", source.format)

        print("Say something!...")
        #print(r.energy_threshold)
        r.energy_threshold += 280
        # # print(r.adjust_for_ambient_noise(source,duration=1))
        audio = r.listen(source)

        # Speech recognition using Google Speech Recognition
    try:
        print("Parsing ...")  # Debugging To
        voice_data = r.recognize_google(audio)
        output_language = translator.translate(voice_data)
        language = output_language.src
        if language != 'en':
            voice_data = output_language.text
            print(voice_data)
        return voice_data.lower(), language  # returning the text which has been inputed.


    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
def change_language(S_text, language):
    trans3 = translator.translate(S_text,dest = language)
    print(trans3.text)
    talk_gtts(trans3.text,language)

