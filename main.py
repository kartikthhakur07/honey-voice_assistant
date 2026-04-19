import speech_recognition as sr  # type: ignore
import webbrowser 
import pyttsx3  # type: ignore 
import pywhatkit  # type: ignore
import requests  # type: ignore
from gtts import gTTS # type: ignore
from groq import Groq # type: ignore
import pygame  # type: ignore
import os
from openwakeword.model import Model
import numpy as np
import pyaudio  # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()
newsapi = os.getenv("NEWS_API_KEY")
api_key = os.getenv("GROQ_API_KEY")

recognizer = sr.Recognizer()

model_path = os.path.join("my_custom_model", "honey.onnx")

def speak(text):# male voice
    ttsx = pyttsx3.init()
    ttsx.say(text)
    ttsx.runAndWait()

def speak_(text):# female voice
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    if os.path.exists("temp.mp3"):
        os.remove("temp.mp3")

def ai(command):
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
    
    model="llama-3.1-8b-instant", 
    messages=[
        {"role": "system", "content": "You are a honey assistant that responds to user commands and queries and skilled in general tasks like alexa and google cloud. give short and concise answers of 1-2 sentences to the user and try to be as helpful as possible."},
        {"role": "user", "content": command },
      ] )

    return response.choices[0].message.content

def listen_for_wake_word():

    model = Model(wakeword_models=["honey.onnx"])  

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1280)

    while True:
        data = stream.read(1280, exception_on_overflow=False, timeout=10)
        audio_data = np.frombuffer(data, dtype=np.int16)

        prediction = model.predict(audio_data)

        for wakeword, score in prediction.items():
            if score > 0.5:  # sensitivity
                print("Wake word detected!")
                return

if __name__ == "__main__":
    speak("initializing assistant honey...")

    while True:
        listen_for_wake_word()   # 👈 WAIT FOR "HONEY"
        speak("Yes, I am listening")

        with sr.Microphone() as source:
                print("Listening...")
                try:
                    audio = recognizer.listen(source, timeout=5,phrase_time_limit=5)
                    command = recognizer.recognize_google(audio).lower()
                    
                    print(f"Recognized command: {command}")


                    if "stop" in command or "exit" in command or "goodbye" in command or "bye" in command:
                        speak("Shutting down the assistant. Goodbyeeeee......!")
                        break

                    elif "hello" in command or "hi" in command or "hey" in command :
                        speak("yahhh... honey is ready. What can i do for you ?")

                    elif "open" in command or "search" in command:
                        search = command.replace("open", "").strip().replace(" ", "").replace("honey", "").strip().replace(" ", "")
                        speak(f"Opening {search}")
                        webbrowser.open(f"https://www.{search}.com")

                    elif "play" in command or "video" in command:
                        song_name = command.replace("play", "").strip().replace("video", "").strip().replace("honey", "").strip()
                        speak(f"Searching YouTube for {song_name}")
                        print(f"Playing: {song_name}")
                        pywhatkit.playonyt(song_name)

                    elif "news" in command:
                        r = requests.get(f"https://newsapi.org/v2/everything?q=india&language=en&sortBy=publishedAt&pageSize=5&apiKey={newsapi}")
                        if r.status_code == 200:
                            news_data = r.json()
                            articles = news_data.get("articles", [])
                            speak("Here are the latest news headlines:")
                            for i, article in enumerate(articles[:5]):
                                speak(article["title"])
                                print(f"Article {i+1}: {article['title']}")
                            speak("thank you")   
                        else:
                            speak("Sorry, I couldn't fetch the latest news at the moment.")

                    else:
                        response = ai(command)
                        print(f"AI Response: {response}")
                        speak(response) 
                
                except sr.WaitTimeoutError:
                    print("Listening timed out while waiting for phrase to start")  
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
              
