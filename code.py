import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import os
import smtplib
import webbrowser
import random
import pyaudio
import pywhatkit

# object creation
engine = pyttsx3.init('sapi5') 
# To get detail of current voice
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

# function to speak by my assisstant
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# wish according to the system time
def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Please tell me what can I help you")

# It takes microphone input from the user and returns string as output
def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source: 
        print("Listening...")
        r.pause_threshold=0.8
        audio=r.listen(source)
    try:
        print("Recognizing...")
        # using google to recognize audio
        query=r.recognize_google(audio,language="en-in")
        print(f"User said:{query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def auto_msg(num,content,hour,min):
    pywhatkit.sendwhatmsg(num,content,hour, min)

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    with open("pswd.txt") as f:
        pswd=f.read()
    server.login('your_email_Id@gmail.com',pswd)
    server.sendmail('your_email_Id@gmail.com',to,content)
    server.close()


if __name__ == '__main__':
    wishMe()
    while True:
        query=takeCommand().lower()
        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query=query.replace("wikipedia","")
            results= wikipedia.summary(query)
            print(results)
            speak('According to wikipedia')
            speak(results)
        elif 'youtube' in query:
            speak("Opening youtube")
            webbrowser.open("youtube.com")
        elif 'google' in query:
            webbrowser.open("google.com")
        elif 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'music from computer' in query:
            speak('Plz wait I play random music for u')
            music_dir='path of your music folder'
            # make list of all the musics present in this directory
            songs=os.listdir(music_dir)
            song_random=random.choice(songs)
            os.startfile(os.path.join(music_dir,song_random))
        elif 'play' in query:
            query=query.replace("play","")
            speak('playing'+ query)
            pywhatkit.playonyt(query)
        elif 'time' in query:
            str_time=datetime.datetime.now().strftime("%I:%M %p")
            print(str_time)
            speak(f"The time is {str_time}")
        elif 'email' in query:
            try:
                print("To whom u want to send email, please provide complete email id:")
                to=input()#takeCommand().lower()
                speak("Tell me the content u want to send:")
                content=takeCommand()
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry, I am not able to send this email at this moment")
        elif 'whatsapp' in query:
            speak("Tell me the mobile number on which u want to send message")
            num="+91"+ takeCommand()
            speak("Tell me the meassage u want to send")
            msg=takeCommand()
            speak("at what hour u want to send message")
            hour=int(takeCommand())
            speak("at what minute u want to send message, should be more than 2 minutes from now")
            min=int(takeCommand())
            auto_msg(num,msg,hour,min)
        elif 'quit' in query:
            exit()
