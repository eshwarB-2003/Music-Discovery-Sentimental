

🎵 Emotion-Aware Music Recommendation System

An AI-powered music recommendation system that understands human emotions and sentiment from text or voice input and delivers personalized Spotify music recommendations — all wrapped in a clean Streamlit web app experience.

🚀 Project Overview

Music connects deeply with human emotions. This project bridges Natural Language Processing (NLP), Speech Recognition, and Spotify’s music ecosystem to recommend songs based on:

🎙 Voice input (speech-to-text)

✍️ Text input

😊 Emotion detection

📊 Sentiment analysis

🎧 Spotify genre & artist matching

The system dynamically adapts recommendations based on the user’s emotional state and sentiment polarity.

✨ Key Features
🔐 User Authentication

Signup & Login system

Persistent user data using data.json

🧠 Emotion & Sentiment Intelligence

Sentiment Analysis using pysentimiento

Emotion Classification using Hugging Face Transformers

Detects emotions like:

Joy 😄

Sadness 😢

Anger 😡

Fear 😨

Love ❤️

Surprise 😲

🎤 Voice-Based Music Recommendations

Speech recognition using Google Speech API

Converts real-time voice input into emotion-aware recommendations

🎶 Spotify-Powered Recommendations

Spotify Web API integration

Genre-based track discovery

Artist-specific recommendations

Album cover previews

🖥 Interactive UI

Built with Streamlit

Clean, responsive dashboard

Sidebar navigation

🧩 System Architecture
User Input (Text / Voice)
        ↓
Sentiment Analysis (pysentimiento)
        ↓
Emotion Detection (Transformers)
        ↓
Emotion + Sentiment Mapping
        ↓
Spotify Genre Matching
        ↓
Music Recommendations 🎧

🛠 Tech Stack
Category	Technologies
Frontend	Streamlit
NLP	pysentimiento, Hugging Face Transformers
Speech	SpeechRecognition
Music API	Spotify Web API (Spotipy)
ML Models	Emotion & Sentiment Classifiers
Database	JSON-based persistence
Utilities	Levenshtein Distance
📦 Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/emotion-music-recommender.git
cd emotion-music-recommender

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Spotify API Credentials

Create a Spotify Developer account and update:

SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)


⚠️ Never expose credentials in production

▶️ Running the App
streamlit run app.py


Then open:

http://localhost:8501

🧪 Sample User Credentials
{
  "email": "user@gmail.com",
  "password": "1234"
}

🎯 Emotion → Genre Mapping
Emotion	Positive Genres	Negative Genres
Joy	Pop, Dance, Chill	Indie, Emo
Sadness	Folk, Blues	Grunge, Metal
Love	R&B, Soul	Alt-rock
Anger	Rock, Metal	Hardcore
Fear	Hip-Hop, Rap	Industrial
Surprise	EDM, House	Minimal Techno
🌟 Highlights

Multimodal input (text + voice)

Emotion-aware personalization

Real-time Spotify integration

Lightweight, scalable architecture

Recruiter-ready ML + NLP project

🔮 Future Enhancements

🎧 Spotify playlist generation

🤖 User emotion history & learning

📱 Mobile-friendly UI

☁️ Cloud database integration

🔐 OAuth-based authentication
