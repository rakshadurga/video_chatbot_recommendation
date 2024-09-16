from flask import Flask, render_template, jsonify
import speech_recognition as sr
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Spotify Authentication
client_id = 'e4593db6fca14c49b06ba7f75b9a3a44'  # Replace with your Spotify Client ID
client_secret = '04f99b3871da49a6a262d6195b6b7600'  # Replace with your Spotify Client Secret
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def recommend_song(genre):
    results = sp.search(q=f'genre:{genre}', type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_name = track['name']
        artist_name = track['artists'][0]['name']
        song_url = track['external_urls']['spotify']
        return song_name, artist_name, song_url
    return None

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for genre request...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(f"Error with Google API: {e}")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    genre = get_audio_input()
    if genre:
        song = recommend_song(genre)
        if song:
            return jsonify(success=True, song=song[0], artist=song[1], url=song[2])
    return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)
