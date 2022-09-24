import spotipy
import sys
import os
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"))
)

# results = sp.search(q='equation of time', type='album')
# print(results['albums']['items'][0])

artists = sp.search(q="joji", type="album", limit=2)
print(artists['albums']['items'][1:])