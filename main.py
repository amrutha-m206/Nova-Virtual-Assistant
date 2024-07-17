import speech_recognition as sr
import webbrowser
import pyttsx3 
import music_lib
import requests
import time
import cohere
from datetime import datetime


recognizer=sr.Recognizer()
s=pyttsx3.init()
newsapi="fd2b21038bcb407f9bee3ddc85393785"

def speak(text): #takes text and speaks
    s.say(text)
    s.runAndWait()  
    
def limit_sentences(text, max_sentences):
    sentences = text.split('. ')
    return '. '.join(sentences[:max_sentences])
 
def aiFunc(command):
   
        co = cohere.Client("QJL0n4NLfVOYUg8sdvviSdoSQQps8smzDJiCzkFZ")

        response = co.chat(
	       message=command
        )
        output_text = response.text
        limited_output = limit_sentences(output_text, 2)
        return limited_output
       
def standardWeb(cmd):
    print(cmd)
    if "open google" in cmd.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in cmd.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in cmd.lower():
        webbrowser.open("https://youtube.com")
    elif "open gmail" in cmd.lower():
        webbrowser.open("https://gmail.com")    
    elif "open whatsapp" in cmd.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "open google drive" in cmd.lower():
        webbrowser.open("https://drive.google.com/drive/folders/1rDZfniYKDBnosNwDGpq2RphQLsKfNkPO")   
    elif "open google classroom" in cmd.lower():
        webbrowser.open("https://classroom.google.com/?pli=1")
        
        
def playMusic(cmd):
    
        song=" ".join(cmd.lower().split(" ")[1:])  #first splitting into list and extracting song name and then converting back to string to pass a song as an argument to search in dictionary
        link=music_lib.music[song]  #music is the dictionary
        webbrowser.open(link) 
    
def startNews(cmd):
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])
            max_articles=5
            max_time=30
            count = 0
            start_time = time.time()
        
            for article in articles:
               if count >= max_articles:
                  break
            
               elapsed_time = time.time() - start_time
               if elapsed_time >= max_time:
                  break

               speak(article['title'])
               count += 1
               time.sleep(1)
    
def CheckCommand(c):
        output=aiFunc(c)
        speak(output)
        
def get_weather(cmd):
   # print("location given" )
    location=cmd.lower().split(" ")[2] 
    api_key = '5947d6859698547438d815fe522c0ccd'
    base_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        weather_info = f"Current weather in {location}: {data['current']['condition']['text']}, {data['current']['temp_c']}°C"
        return weather_info
    else:
        return "Sorry, I couldn't retrieve the weather information."

def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}."


def get_date():
    today = datetime.now()
    current_date = today.strftime("%Y-%m-%d")
    return f"Today's date is {current_date}."
        
         
if __name__=="__main__":
    speak("Getting started with Nova")
    #Listen for the wake word Nova
    #obtain audio from microphone
    
    while True:
        r=sr.Recognizer()
       
        try:
            with sr.Microphone() as source: #use of with automatically releases microphone
              print("Listening..")
              
              recognizer.adjust_for_ambient_noise(source)
              audio=r.listen(source) #u can add timeout if u want and modify exception accordingly
              print("recognizing")
              
              sentence=r.recognize_google(audio)
        
              if sentence.lower()=="stop Nova":
                print("Stopping Nova")
                break
            
              print(sentence)
            
            #print(word)
              if sentence.lower()=="nova":
                 speak("Hello,How can i help you?")
                 with sr.Microphone() as source:
                        print("Nova active..")
                        recognizer.adjust_for_ambient_noise(source)
                        audio=r.listen(source) 
                        command=r.recognize_google(audio)
                        print(command)
                        if "weather" in command.lower():
                            get_weather(command)
                            
                        elif "open" in command.lower():
                            standardWeb(command)
                        
                        elif command.lower().startswith("play"):
                            playMusic(command)
                            
                        elif "news" in command.lower(): 
                            startNews(command) 
                        
                        elif "time" in command.lower():
                             current_time = get_time()
                             speak(current_time) 
                        
                        elif "date" in command.lower():
                              current_date = get_date()
                              speak(current_date)
                            
                        elif command.lower()=="can you stop nova":
                            print("Stopping Nova.")
                            break
                        
                        else:
                            CheckCommand(command)
              
          
                
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error;{0}".format(e))
    