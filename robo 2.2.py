import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit
import datetime
import  os
import random
from ecapture import ecapture as ec
import wikipedia
import re
import requests
from tkinter import messagebox
import pyjokes
from os import path
import subprocess
from gtts import gTTS
from googletrans import Translator
from playsound import playsound  
from robo_tts import take_command, talk
import wikipedia


def time_now():      
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        print("Hello,Good Morning")
        S_text = "Hello,Good Morning"
    elif hour>=12 and hour<18:
        print("Hello,Good Afternoon")
        S_text = "Hello,Good Afternoon"
    else:
        print("Hello,Good Evening")
        S_text = "Hello,Good Evening"




  

'''def math_():

    
    elif re.search('add|addition', voice_data):
        #s = input("Input a string: ")
        n= stringtolist(voice_data)
        l=0
        d=[]
        for c in n:
            if c.isdigit():
                d.append(c)
            elif c.isalpha():
                l=l+1
            else:
                pass
        add1=0
        for num in d:
            #add1=int(add1)
            add1=add1+int(num)
        print(add1)
        #print("Letters", l)
        #print("Digits", d)

        S_text = add1'''
'''def wiki():

    try:
        S_text = 'Searching Wikipedia...'
        voice_data =voice_data.replace("wikipedia", "")
        S_text = 'Whats you want summary or content of query'
        result_s =take_command()
        if 'summary' in result_s:
            results = wikipedia.summary(voice_data)
            print("According to Wikipedia")
            S_text = "According to Wikipedia"
            print(results)
            S_text = results
        elif 'content' in result_s:
            page = wikipedia.page(voice_data)
            results = page.content
            print("According to Wikipedia")
            S_text = "According to Wikipedia"
            print(results)
            S_text = results
    except wikipedia.exceptions.DisambiguationError as e:
        s = random.choice(e.options)
        print(s)
        S_text = s
    except wikipedia.exceptions.WikipediaException as e:
        print('Search not include, try again wikipedia and your search')'''

'''def weather():

    api_key="394d4ebf0a7de20604147666d665d2d0"
    base_url="https://api.openweathermap.org/data/2.5/weather?"
    print("Whats the city name")
    S_text = "whats the city name"
    if language != 'en':
        change_language(S_text, language)
    else:
        talk(S_text)
    city_name=take_command()
    complete_url=base_url+"appid="+api_key+"&q="+city_name
    response = requests.get(complete_url)
    x=response.json()
    if x["cod"]!="404":
        y=x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        print(city_name+" Temperature in kelvin unit = "+
                str(current_temperature) +
                "\n humidity (in percentage) = " +
                str(current_humidiy) +
                "\n description = " +
                str(weather_description))
        S_text = (city_name+" Temperature in kelvin unit is"+
                str(current_temperature) +
                "\n humidity in percentage is " +
                str(current_humidiy) +
                "\n description  " +
                str(weather_description))
        if language != 'en':
            change_language(S_text, language)
        else:
            talk(S_text)
    else:
        print(" City Not Found\n")
        S_text = " City Not Found "
        if language != 'en':
            change_language(S_text, language)
        else:
            talk(S_text)'''

def joke():

    with open("joke.txt", "r") as m:
        sents = m.read().split("\n\n")
        se = random.choice(sents)
        print(se)
        S_text = se





def exit():
    #elif 'exit' in voice_data or "goodbye" in voice_data or "ok bye" in voice_data or "stop" in voice_data:
    print('Your robo is shutting down,Good bye')
    S_text = 'your robo is shutting down,Good bye'
    exit()
def log_off():
 
    shut=take_command()
    if shut == 'yes':
        print("Ok , your pc will log off in 10 sec make sure you exit from all applications")
        S_text = "Ok , your pc will log off in 10 sec make sure you exit from all applications"
        subprocess.call(["shutdown", "/l"])
    else:
        pass


if __name__ == "__main__":
    with open("startup.txt", "r") as m:
        sents = m.read().split("\n\n")
        se = random.choice(sents)
        print(se)
        talk(se)
        
        joke()
  