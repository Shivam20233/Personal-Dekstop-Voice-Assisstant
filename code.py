import pyttsx3
import speech_recognition as sr
import wikipedia
import datetime
import os
import smtplib
import webbrowser
import random
import pyaudio

engine = pyttsx3.init('sapi5')                                 # object creation
voices = engine.getProperty('voices')                          # To get detail of current voice
engine.setProperty('voice',voices[1].id)                       # 1 for female voice

def speak(audio):                                              # function to speak by my assisstant
    engine.say(audio)
    engine.runAndWait()

def wishMe():                                                  # wish according to the system time
    hour=int(datetime.datetime.now().hour)                     # to get integer between 0 to 24
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am chitti the Robot assisstant of Shivam Sharma with Speed 1 terahertz, memory 1 zeta byte please tell me what can I help you")
def takeCommand():                                             # It takes microphone input from the user and returns string as output
    r= sr.Recognizer()                                         #Initialise the recognizer
    with sr.Microphone() as source:                            # use the microphone as source for input
        print("Listening...")
        r.pause_threshold=0.8                                  # seconds of non speaking audio before a phrase is considered complete
        r.energy_threshold=300
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language="en-in")       # using google to recognize audio
        print(f"User said:{query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)                  #creates SMTP session
    server.ehlo()
    server.starttls()                                          # start TLS for security
    with open("pswd.txt") as f:
        pswd=f.read()
    server.login('sender_email_Id@gmail.com',pswd)
    server.sendmail('sender_email_Id@gmail.com',to,content)
    server.close()


if __name__ == '__main__':
    wishMe()
    while True:
        query=takeCommand().lower()                            # string converted into lower case
    # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentence=1)
            speak('According to wikipedia')
            speak(results)
        elif 'youtube' in query:
            speak("Opening youtube")
            webbrowser.open("youtube.com")
        elif 'google' in query:
            webbrowser.open("google.com")
        elif 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'music' in query:
            music_dir='C:\\Users\\ramkrishna katare\\Music'
            songs=os.listdir(music_dir)# make list of all the musics present in this directory
            song_random=random.choice(songs)
            os.startfile(os.path.join(music_dir,song_random))
        elif 'time' in query:
            str_time=datetime.datetime.now().strftime("%H:%M:%S")
            print(str_time)
            speak(f"The time is {str_time}")
        elif 'email' in query:
            try:
                print("To whom u want to send email, please provide complete email id:")
                to=input()
                speak("Tell me the content u want to send:")
                content=takeCommand()
                sendEmail(to,content)
                speak("Email has been sent!")
            except Exception as e:
                speak("Sorry, I am not able to send this email at this moment")
        elif 'quit' in query:
            exit()
