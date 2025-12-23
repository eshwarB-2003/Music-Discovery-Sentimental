from pysentimiento import create_analyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import json
import os
import speech_recognition as sr
from Levenshtein import distance
import os
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0

spotify_client_credentials_manager = SpotifyClientCredentials(client_id='9959a1d8eb1b4f378da63ad9b59335d1', client_secret='054e13dc8da540338247c00a933a20ac')
sp = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

def load_model():
   sentiment_analysis = create_analyzer(task="sentiment", lang="en")
   tokenizer = AutoTokenizer.from_pretrained("aiknowyou/it-emotion-analyzer")
   model = AutoModelForSequenceClassification.from_pretrained("aiknowyou/it-emotion-analyzer")
   emotion_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
   return sentiment_analysis ,emotion_analysis

def getting_artist_id(artist):
    results = sp.search(q=f'artist:{artist}', type='artist')
    artist_id = results['artists']['items'][0]['id']
    print(f"Artist ID: {artist_id}")
    return artist_id

def getting_artist_genres(artist_id):
    artist_info = sp.artist(artist_id)
    artist_genres = artist_info['genres']
    print(f"Artist Genres: {artist_genres}")
    return artist_genres

def find_closest_genre(input_genre, genres):
    min_distance = float('inf')
    closest_genre = None
    for genre in genres:
        d = distance(input_genre, genre)
        if d < min_distance:
            min_distance = d
            closest_genre = genre

    print(f"Closest genre to '{input_genre}': {closest_genre}")
    return closest_genre

def get_tracks(artist_name, output_genre):
    filtered_tracks = []

    if artist_name:
        print('In if Block')
        tracks = sp.search(q=f'artist:{artist_name}', type='track', limit=50)
        tracks_items = tracks['tracks']['items']

        for track in tracks_items:
            track_info = sp.track(track['id'])
            track_artists = track_info['artists']
            track_genres = []

            # Get all genres of the artists involved in the track
            for track_artist in track_artists:
                artist_info = sp.artist(track_artist['id'])
                track_genres.extend(artist_info['genres'])

            # Check if the desired genre is in the track genres
            if output_genre in track_genres:
                filtered_tracks.append(track_info)

    else:
        query = f"genre:{output_genre}" 
        results = sp.search(q=query, type="track", limit=10)

        track_uri = results['tracks']['items']

        tracks = results['tracks']['items']
        filtered_tracks.extend(tracks)
    # return filtered_tracks
    return [(track['name'], ', '.join([artist['name'] for artist in track['artists']]), track['album']['images'][0]['url'] if track['album']['images'] else None) for track in filtered_tracks]


emotion_keywords = {
    "joy": "happy",
    "love": "romantic",
    "sadness": "sad",
    "anger": "angry",
    "fear": "scary",
    "surprise": "surprise"
}
emotion_labels = {
    "0": "sadness",
    "1": "joy",
    "2": "love",
    "3": "anger",
    "4": "fear",
    "5": "surprise"
}


combined_labels = {
    "POS_love": ["R&B", "soul", "romance", "classic pakistani pop"],
    "NEG_love": ["sad","emo"],
    "POS_joy": ["pop", "dance", "happy", "modern bollywood", "sufi", "chill", "ambient"],
    "NEG_joy": ["indie", "emo", "sad"],
    "POS_sadness": ["folk", "blues", "acoustic"],
    "NEG_sadness": ["emo", "grunge", "black-metal"],
    "POS_anger": ["rock", "hard-rock", "metal"],
    "NEG_anger": ["punk-rock", "hardcore", "metalcore"],
    "POS_fear": ["hip-hop", "trap", "rap"],
    "NEG_fear": ["heavy-metal", "death-metal", "industrial"],
    "POS_surprise": ["dance", "edm", "house"],
    "NEG_surprise": ["electronic", "ambient", "minimal-techno"],
    "NEU_love": ["R&B", "soul"],  # Same as "POS_love"
    "NEU_joy": ["pop", "dance", "sufi", "chill", "ambient"],  # Same as "POS_joy"
    "NEU_sadness": ["folk", "blues"],  # Same as "POS_sadness"
    "NEU_anger": ["rock", "hard-rock"],  # Same as "POS_anger"
    "NEU_fear": ["hip-hop", "rap"],  # Same as "POS_fear"
    "NEU_surprise": ["dance", "house"],  # Same as "POS_surprise"
}

def signup(json_file_path="data.json"):
    st.title("Signup Page")
    with st.form("signup_form"):
        st.write("Fill in the details below to create an account:")
        name = st.text_input("Name:")
        email = st.text_input("Email:")
        age = st.number_input("Age:", min_value=0, max_value=120)
        sex = st.radio("Sex:", ("Male", "Female", "Other"))
        password = st.text_input("Password:", type="password")
        confirm_password = st.text_input("Confirm Password:", type="password")
        
        if st.form_submit_button("Signup"):
            if password == confirm_password:
                user = create_account(
                    name,
                    email,
                    age,
                    sex,
                    password,
                    json_file_path,
                )
                session_state["logged_in"] = True
                session_state["user_info"] = user
            else:
                st.error("Passwords do not match. Please try again.")


def check_login(username, password, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        for user in data["users"]:
            if user["email"] == username and user["password"] == password:
                session_state["logged_in"] = True
                session_state["user_info"] = user
                st.success("Login successful!")
                return user
        return None
    except Exception as e:
        st.error(f"Error checking login: {e}")
        return None


def initialize_database(json_file_path="data.json"):
    try:
        if not os.path.exists(json_file_path):
            data = {"users": []}
            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file)
    except Exception as e:
        print(f"Error initializing database: {e}")

def create_account(
    name,
    email,
    age,
    sex,
    password,
    json_file_path="data.json",
):
    try:

        if not os.path.exists(json_file_path) or os.stat(json_file_path).st_size == 0:
            data = {"users": []}
        else:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

        # Append new user data to the JSON structure
        user_info = {
            "name": name,
            "email": email,
            "age": age,
            "sex": sex,
            "password": password,
        }
        data["users"].append(user_info)

        # Save the updated data to JSON
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        st.success("Account created successfully! You can now login.")
        return user_info
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return None

def login(json_file_path="data.json"):
    st.title("Login Page")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    login_button = st.button("Login")

    if login_button:
        user = check_login(username, password, json_file_path)
        if user is not None:
            session_state["logged_in"] = True
            session_state["user_info"] = user
        else:
            st.error("Invalid credentials. Please try again.")


def get_user_info(email, json_file_path="data.json"):
    try:
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)
            for user in data["users"]:
                if user["email"] == email:
                    return user
        return None
    except Exception as e:
        st.error(f"Error getting user information: {e}")
        return None

def render_dashboard(user_info, json_file_path="data.json"):
    try:
        st.title(f"Welcome to the Dashboard, {user_info['name']}!")
        
        st.subheader("User Information:")
        st.write(f"Name: {user_info['name']}")
        st.write(f"Sex: {user_info['sex']}")
        st.write(f"Age: {user_info['age']}")
        
    except Exception as e:
        st.error(f"Error rendering dashboard: {e}")


def main(json_file_path="data.json"):
    st.sidebar.title("Music Recommendation System")
    page = st.sidebar.radio(
        "Go to", ("Signup/Login", "Dashboard", "Music Recommendation System"), key="Music Recommendation System",
    )

    if page == "Signup/Login":
        st.title("Signup/Login Page")
        login_or_signup = st.radio("Select an option", ("Login", "Signup"), key="login_signup")
        if login_or_signup == "Login":
            login(json_file_path)
        else:
            signup(json_file_path)
    elif page == "Dashboard":
        if session_state.get("logged_in"):
            render_dashboard(session_state["user_info"])
        else:
            st.warning("Please login/signup to view the dashboard.")
    elif page == "Music Recommendation System":
        if session_state.get("logged_in"):
            user_info = session_state["user_info"]
            
            st.title('Music Recommendation System')
            media_format = st.radio("Choose media format", ("Audio", "Text"))
            if media_format == "Audio":
                artist_name = st.text_input('Artist Name : ')
                recognizer = sr.Recognizer()
                microphone = sr.Microphone()
                if st.button("START RECORDING"):
                    with microphone as source:
                        st.info("Listening...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                    try:
                        voice_command = recognizer.recognize_google(audio, language="en")
                        
                    except sr.UnknownValueError:
                        st.write("Could not understand the audio. Please try again.")
                        return
                    except sr.RequestError as e:
                        st.write("Could not understand the audio. Please try again.")
                        return
                    if voice_command:
                        sentiment_analysis , emotion_analysis = load_model()
                        sentiment_prediction = sentiment_analysis.predict(voice_command)
                        highest_emotion = max(sentiment_prediction.probas, key=sentiment_prediction.probas.get)
                        sentiment = highest_emotion

                        sentences = [voice_command]  # Ensure 'sentences' is defined
                        predictions = emotion_analysis(sentences)
                        detected_emotion = emotion_labels[predictions[0]['label']]
                        
                        input_genre = combined_labels.get(f"{sentiment}_{detected_emotion}")
                        # st.write(input_genre)
                        if artist_name :
                            artist_id =getting_artist_id(artist_name)
                            genres = getting_artist_genres(artist_id)
                            output_genre = find_closest_genre(input_genre, genres)
                        else :
                            output_genre = input_genre[0]
                        recommendations = get_tracks(artist_name , output_genre)
                        st.write(f"<h3 style='text-align: center; color: #4285F4;'>Top tracks for emotion '{detected_emotion}'</h3>", unsafe_allow_html=True)
                        for track_name, artists, album_cover_url in recommendations:
                            track_html = f"""
                                <div style='background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center;'>
                                    <h4 style='color: #1B5E20; margin-bottom: 5px;'>{track_name}</h4>
                                    <p style='color: #4E342E; margin: 0;'>by {artists}</p>
                                    {'<img src="{}" style="max-width: 100px; max-height: 100px; margin-top: 10px;">'.format(album_cover_url) if album_cover_url else ''}
                                </div>
                            """
                            st.markdown(track_html, unsafe_allow_html=True)


            else:
                input_text = st.text_input('Enter your input here: ')
                artist_name = st.text_input('Enter Artist Name: ')

    
                if st.button('Get Recommendations'):
                    if input_text:
                        sentiment_analysis , emotion_analysis = load_model()
                        sentiment_prediction = sentiment_analysis.predict(input_text)
                        highest_emotion = max(sentiment_prediction.probas, key=sentiment_prediction.probas.get)
                        sentiment = highest_emotion

                        sentences = [input_text]
                        predictions = emotion_analysis(sentences)
                        detected_emotion = emotion_labels[predictions[0]['label']]

                        input_genre = combined_labels.get(f"{sentiment}_{detected_emotion}")
                        if artist_name :
                            artist_id =getting_artist_id(artist_name)
                            genres = getting_artist_genres(artist_id)
                            output_genre = find_closest_genre(input_genre, genres)
                        else :
                            output_genre = input_genre[0]
                        recommendations = get_tracks(artist_name , output_genre)
                        st.write(f"<h3 style='text-align: center; color: #4285F4;'>Top tracks for emotion '{detected_emotion}'</h3>", unsafe_allow_html=True)
                        for track_name, artists, album_cover_url in recommendations:
                            track_html = f"""
                                <div style='background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 10px; text-align: center;'>
                                    <h4 style='color: #1B5E20; margin-bottom: 5px;'>{track_name}</h4>
                                    <p style='color: #4E342E; margin: 0;'>by {artists}</p>
                                    {'<img src="{}" style="max-width: 100px; max-height: 100px; margin-top: 10px;">'.format(album_cover_url) if album_cover_url else ''}
                                </div>
                            """
                            st.markdown(track_html, unsafe_allow_html=True)


        else:
            st.warning("Please login/signup to app!!.")

if __name__ == "__main__":
    initialize_database()
    main()