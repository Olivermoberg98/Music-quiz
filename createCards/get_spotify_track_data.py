import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
CLIENT_ID = 'fa6a760e4e794ecb8c642e8d3de00b50'
CLIENT_SECRET = 'd68cb70dd3f54e0a9326ceb210ef0113'

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def get_playlist_tracks(playlist_uri):
    # Fetch playlist tracks
    results = sp.playlist_tracks(playlist_uri)
    
    tracks = []
    while results:
        for item in results['items']:
            track = item['track']
            track_info = {
                'Artist': ', '.join(artist['name'] for artist in track['artists']),
                'Song Name': track['name'],
                'Album Release Year': track['album']['release_date'][:4],
                'URL': track['external_urls']['spotify']
            }
            tracks.append(track_info)
        
        # Check if there are more tracks to fetch
        if results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        else:
            results = None
        
        # For more than 100 songs
        #while results['next']:
        #results = sp.next(results)
        #tracks.extend(results['items'])
        #return tracks

    return tracks

def save_to_excel(tracks, filename):
    # Create a DataFrame from the tracks
    df = pd.DataFrame(tracks)
    
    # Save DataFrame to Excel file
    df.to_excel(filename, index=False)

def fetch_and_save_spotify_data(playlist_url, output_file):
    tracks = get_playlist_tracks(playlist_url)
    save_to_excel(tracks, output_file)
    print(f"Saved {len(tracks)} tracks to {output_file}")

#if __name__ == '__main__':
    #fetch_and_save_spotify_data('https://open.spotify.com/playlist/6J8d6E84rS0go6ImsCfRcn?si=e18531110a164e69', 'Hitster_data_svenska_latar_v0.xlsx')
