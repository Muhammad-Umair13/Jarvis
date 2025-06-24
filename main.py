import streamlit as st
import speech_recognition as sr
import requests
import pyttsx3
import datetime
import webbrowser
import os
import time
import threading

# === OpenRouter Key ===
OPENROUTER_API_KEY = "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"

engine = pyttsx3.init()

def speak(text):
    st.markdown(f"<div class='bubble jarvis'><strong>Jarvis:</strong> {text}</div>", unsafe_allow_html=True)
    engine.say(text)
    engine.runAndWait()

def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant named Jarvis."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"Error: {e}"

def handle_command(command):
    command = command.lower()
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open gmail" in command:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")
    elif "open settings" in command:
        speak("Opening Windows Settings")
        os.system("start ms-settings:")
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "shutdown" in command:
        speak("Shutting down in 5 seconds...")
        time.sleep(5)
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting system...")
        os.system("shutdown /r /t 1")
    elif "date" in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "weather" in command:
        speak("Opening weather updates")
        webbrowser.open("https://www.google.com/search?q=weather")
    elif "calculate" in command:
        try:
            expr = command.replace("calculate", "")
            result = eval(expr)
            speak(f"The result is {result}")
        except:
            speak("Sorry, I couldn't calculate that.")
    else:
        return False
    return True

def listen_and_process():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Jarvis is listening. Say 'Jarvis' followed by your command.")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "jarvis" in command:
                    command = command.replace("jarvis", "").strip()
                    if not handle_command(command):
                        reply = ask_openrouter(command)
                        speak(reply)
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                speak("Internet connection issue.")
                break

# === Streamlit UI ===
st.set_page_config(page_title="Jarvis Voice Assistant", page_icon="🤖")

st.markdown(
    """
    <style>
        body {
            background-image: url('https://i.gifer.com/QWc9.gif');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .stApp {
            background-color: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            color: white;
        }
        .bubble {
            background-color: #1f1f1f;
            border-radius: 15px;
            padding: 10px 15px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: white;'>Jarvis Voice Assistant</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

if st.button("🎙️ Start Listening"):
    threading.Thread(target=listen_and_process).start()