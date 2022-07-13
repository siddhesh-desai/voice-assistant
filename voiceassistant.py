import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
from googlesearch import search
from bs4 import BeautifulSoup
import requests

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'date' in command:
        date = datetime.datetime.now().strftime('%m:%d %Y')
        talk('Today\'s date is ' + date)

    elif 'are you single' in command:
        talk('I am in a relationship with wifi')

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'search' in command:
        google = command.replace('search', '')
        talk('searching on google')
        for j in search(google, tld="co.in", num=1, stop=1, pause=1):
            webbrowser.open(j)

    elif 'open' in command:
        app=command.replace('open', '')
        talk('opening' + app)
        os.system(app)

    elif "weather at" in command:
        city = command.replace('weather at', '')
        url = "https://www.google.com/search?q=" + "weather" + city
        html = requests.get(url).content

        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        data = str.split('\n')
        time = data[0]
        sky = data[1]

        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text

        pos = strd.find('Wind')
        other_data = strd[pos:]

        # printing all data
        print('Temperature is', temp)
        print('Time is', time)
        print('The sky is '+ sky)
        talk('Temperature is'+ temp)
        talk('Time is '+ time)
        talk('The sky is '+ sky)

    else:
        talk('I didn\'t get you. Please say the command again...')


while True:
    run_alexa()
