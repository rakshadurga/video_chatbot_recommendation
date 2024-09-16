import sqlite3

# Function to log user interactions
def log_interaction(genre, song, artist, url):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY,
            genre TEXT,
            song TEXT,
            artist TEXT,
            url TEXT
        )
    ''')
    cursor.execute('INSERT INTO interactions (genre, song, artist, url) VALUES (?, ?, ?, ?)', 
                   (genre, song, artist, url))
    connection.commit()
    connection.close()

# Update get_recommendation function to log interactions
@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    genre = get_audio_input()
    if genre:
        song = recommend_song(genre)
        if song:
            log_interaction(genre, song[0], song[1], song[2])  # Log user interaction
            return jsonify(success=True, song=song[0], artist=song[1], url=song[2])
    return jsonify(success=False)
