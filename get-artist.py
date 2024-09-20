# Required libraries
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = '93d06e128a9841d3a049499ae6e3f362'
CLIENT_SECRET = '98f60411b2784b64abdb5f88c1e3e754'

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
        return f"No artist found for {name}"

# Test the function
print(spotify('Taylor Swift'))
