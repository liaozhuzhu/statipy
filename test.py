import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

# results = sp.search(q='juice', limit=5)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx+1, track['name'])

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"))
)


results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])