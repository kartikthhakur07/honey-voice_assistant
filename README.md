# 🍯 Honey - AI Voice Assistant

Honey is a Python-based, fully functional AI voice assistant. It uses offline wake word detection to listen securely in the background, processes natural language queries using the Groq API (LLaMA 3), and responds with a natural-sounding voice using Google Text-to-Speech (gTTS).

## ✨ Features

* **Offline Wake Word Detection:** Uses `openwakeword` to listen locally for the name "Honey" without constantly sending your audio stream to the cloud.
* **Conversational AI:** Powered by Groq's lightning-fast inference and the LLaMA 3 model to answer general questions intelligently.
* **Natural Voice Engine:** Utilizes `gTTS` and `pygame` for smooth, human-like text-to-speech audio playback.
* **Web Automation:** Automatically opens websites (e.g., "open Google", "search GitHub").
* **Media Playback:** Uses `pywhatkit` to search and instantly play YouTube videos on command.
* **Live News Fetching:** Integrates with NewsAPI to read aloud the top 5 current headlines in India.

## 🛠️ Prerequisites

Before running this project, you will need to get two free API keys:
1. **Groq API Key:** Get it from [console.groq.com](https://console.groq.com)
2. **NewsAPI Key:** Get it from [newsapi.org](https://newsapi.org)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kartikthhakur07/honey_voice_assistant.git](https://github.com/kartikthhakur07/honey_voice_assistant.git)
   cd honey_voice_assistant
