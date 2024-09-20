# pip install spotipy

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Add your Spotify API credentials here
CLIENT_ID = '93d06e128a9841d3a049499ae6e3f362'
CLIENT_SECRET = '98f60411b2784b64abdb5f88c1e3e754'

# Authentication - without user (Client Credentials flow)
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Get artist data by artist name or ID
artist_name = "Taylor Swift"
results = sp.search(q='artist:' + artist_name, type='artist')

# Extract artist info
artists = results['artists']['items']
if artists:
    artist = artists[0]
    print(f"Name: {artist['name']}")
    print(f"Followers: {artist['followers']['total']}")
    print(f"Genres: {', '.join(artist['genres'])}")
    # print(f"Spotify URL: {artist['external_urls']['spotify']}")
else:
    print(f"No artist found for {artist_name}")
