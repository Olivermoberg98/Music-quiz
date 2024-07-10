import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
CLIENT_ID = 'fa6a760e4e794ecb8c642e8d3de00b50'
CLIENT_SECRET = 'd68cb70dd3f54e0a9326ceb210ef0113'

# Set up Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def extract_playlist_id(playlist_uri):
    if playlist_uri.startswith('https://open.spotify.com/playlist/'):
        # Extract the playlist ID from a full URL
        return playlist_uri.split('/')[-1].split('?')[0]
    elif playlist_uri.startswith('spotify:playlist:'):
        # Extract the playlist ID from a URI
        return playlist_uri.split(':')[-1]
    else:
        raise ValueError('Unsupported playlist URI format')

def get_playlist_tracks(playlist_uri):
    # Extract playlist ID from the URI
    #playlist_id = extract_playlist_id(playlist_uri)
    
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

def main():
    playlist_uri = 'https://open.spotify.com/playlist/4TJgT7TE9WbJHdk12kEJvt?si=37e252f66ef744a8'  # Replace with your playlist URI
    output_file = 'Hitster_data_v0.xlsx'
    
    # Get playlist tracks and save to Excel
    tracks = get_playlist_tracks(playlist_uri)
    save_to_excel(tracks, output_file)
    print(f"Saved {len(tracks)} tracks to {output_file}")

if __name__ == '__main__':
    main()
