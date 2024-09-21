import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# Spotify API credentials
CLIENT_ID = '93d06e128a9841d3a049499ae6e3f362'
CLIENT_SECRET = '98f60411b2784b64abdb5f88c1e3e754'

# Spotify API function to get artist details
def spotify(name):
    # Authentication using client credentials
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Search for the artist
    results = sp.search(q='artist:' + name, type='artist')
    
    # Extract artist info
    artists = results['artists']['items']
    if artists:
        artist = artists[0]
        return {
            "Name": artist['name'],
            "Followers": artist['followers']['total'],
            "Genres": ', '.join(artist['genres'])
        }
    else:
        return None  # Return None if artist not found

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="gdsc@1234",
        database="devjam"
    )

# Function to get all users from the database
def get_all_users():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id, q1 FROM user_responses")
    users = cursor.fetchall()  # Returns a list of tuples [(user_id, q1_response), ...]
    db.close()
    return users

# Function to calculate points
def calculate_points(artist_name, db_user_artists):
    artist_data = spotify(artist_name)  # Fetch artist data using Spotify API
    if artist_data is None:
        return 0  # Artist not found
    
    # Points assignment based on followers
    followers = artist_data['Followers']
    if followers > 10_000_000:
        artist_points = 2
    elif 1_000_000 <= followers <= 10_000_000:
        artist_points = 4
    else:
        artist_points = 6
    
    # Check if the artist is present in any of the db user's artists (comma-separated string)
    if artist_name.lower() in db_user_artists.lower():
        return artist_points  # Return the calculated points if match is found
    else:
        # Check for genre match
        artist_genres = artist_data['Genres']
        db_user_genres = [spotify(a.strip())['Genres'] for a in db_user_artists.split(',')]
        for genre in db_user_genres:
            if genre in artist_genres:
                return 1  # 1 point for genre match
        return 0  # No match at all

# Main function to generate point pairings for all users
def generate_pairings(user_id, input_artists):
    all_users = get_all_users()
    
    # Loop through each user in the database and compare artists
    pairings = {}
    for db_user_id, db_user_artists in all_users:
        if db_user_id == user_id:
            continue  # Skip comparison with the same user
        
        total_points = 0
        for artist in input_artists:
            total_points += calculate_points(artist, db_user_artists)
        
        # Store pairing in dictionary (user_id, points)
        pairings[db_user_id] = total_points
    
    return pairings

# Example usage
if __name__ == "__main__":
    # Let's assume the 4th user has these 3 favorite artists
    user_id = 4
    input_artists = ['Taylor Swift', 'The Weeknd', 'Billie Eilish']  # Input from user
    
    # Generate pairings and points for the 4th user
    pairings = generate_pairings(user_id, input_artists)
    
    # Output results
    for user, points in pairings.items():
        print(f"User {user} paired with User {user_id} has {points} points.")
