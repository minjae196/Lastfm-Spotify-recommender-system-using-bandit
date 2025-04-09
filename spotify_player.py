from dotenv import load_dotenv
import os
import requests
import urllib.parse

load_dotenv()
SPOTIFY_ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

def search_track_on_spotify(track_name, artist_name=None, access_token=None):
    if access_token is None:
        access_token = SPOTIFY_ACCESS_TOKEN
    query = f"{track_name} {artist_name}" if artist_name else track_name
    url = f"https://api.spotify.com/v1/search?q={urllib.parse.quote(query)}&type=track&limit=3"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        items = response.json()["tracks"]["items"]
        if items:
            uri = items[0]["uri"]
            return {"uri": uri, "id": uri.split(":")[-1]}
    return {"uri": "", "id": ""}
