import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

# results = sp.search(q='juice', limit=5)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx+1, track['name'])

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
                                                           client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET")))


# playlists = sp.user_playlists('liaozhutwo')
# while playlists:
#     for i, playlist in enumerate(playlists['items']):
#         print(playlist[])
#     if playlists['next']:
#         playlists = sp.next(playlists)
#     else:
#         playlists = None

# user = sp.user('liaozhutwo')
# topsong = sp.current_user_top_tracks(limit=5)
# print(topsong)

artistResults = sp.search(q="keshi", type='artist')
url = artistResults['artists']['items'][0]['external_urls']['spotify']
print(url)