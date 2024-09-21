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
        host="localhost",
        user="root",
        password="roh286tan910",
        database="gdsc"
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
def calculate_points(user_artists, input_artists):
    total_points = 0
    matched_artists = set()

    for user_artist in user_artists:
        artist_data = spotify(user_artist.strip())  # Fetch artist data using Spotify API
        if artist_data is None:
            continue  # Skip if artist not found

        # Check against each input artist
        for input_artist in input_artists:
            input_artist_data = spotify(input_artist.strip())
            if input_artist_data is None:
                continue  # Skip if input artist not found

            # Check for exact match
            if user_artist.lower() == input_artist.lower():
                followers = artist_data['Followers']
                # Updated points assignment based on followers
                if followers > 25000000:
                    total_points += 10
                elif 7000000 <= followers <= 25000000:
                    total_points += 18
                else:
                    total_points += 25
                matched_artists.add(user_artist.lower())  # Mark as matched
                break  # Stop checking further pairings for this user_artist since a match was found
            
        # If no exact match, check for genre matches
        if user_artist.lower() not in matched_artists:
            user_genres = artist_data['Genres'].lower().split(', ')
            for input_artist in input_artists:
                input_artist_data = spotify(input_artist.strip())
                if input_artist_data is None:
                    continue  # Skip if input artist not found

                input_genres = input_artist_data['Genres'].lower().split(', ')
                if any(genre in input_genres for genre in user_genres):
                    total_points += 1  # Add point for genre match
                    break  # Stop checking further genre matches for this user_artist

    return total_points

# Main function to generate point pairings for all users
def generate_pairings(user_id, input_artists):
    all_users = get_all_users()
    
    # Loop through each user in the database and compare artists
    pairings = {}
    for db_user_id, db_user_artists in all_users:
        if db_user_id == user_id:
            continue  # Skip comparison with the same user
        
        db_user_artist_list = db_user_artists.split(',')
        total_points = calculate_points(db_user_artist_list, input_artists)
        
        # Store pairing in dictionary (user_id, points)
        pairings[db_user_id] = total_points
    
    return pairings

# Example usage
if __name__ == "__main__":
    # Let's assume the 4th user has these 3 favorite artists
    user_id = 4
    input_artists = ['Taylor Swift', 'Billie Eilish', 'The Weeknd']  # Input from user
    
    # Generate pairings and points for the 4th user
    pairings = generate_pairings(user_id, input_artists)
    
    # Output results
    for user, points in pairings.items():
        print(f"User {user} paired with User {user_id} has {points} points.")
