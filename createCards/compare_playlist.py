import pandas as pd
import os
from collections import defaultdict

# Define file paths and column names
folder_paths = ["movies_v0", "movies_v1"]
file_names = ["hitster_data_movies_v0.xlsx", "hitster_data_movies_v1.xlsx"]
column_name_artist = "Artist"
column_name_song = "Song Name"

# Initialize lists to store data
artists = []
songs = []

# Read data from each file
for i, file_name in enumerate(file_names):
    file_path = os.path.join(folder_paths[i], file_name)
    data = pd.read_excel(file_path)
    artists.append(data[column_name_artist].tolist())
    songs.append(data[column_name_song].tolist())

# Initialize dictionaries for matching songs
matching_songs = defaultdict(list)
matching_artists = defaultdict(list)

# Compare song names across all files
for i in range(len(file_names)):
    for j in range(i+1, len(file_names)):
        # Find common songs
        songs_i = pd.Series(songs[i])
        songs_j = pd.Series(songs[j])
        
        for idx_i, song_i in enumerate(songs_i):
            for idx_j, song_j in enumerate(songs_j):
                if song_i == song_j:
                    song_name = song_i
                    artist_i = artists[i][idx_i]
                    artist_j = artists[j][idx_j]
                    
                    # Store matching songs
                    matching_songs[song_name].append((i, j))
                    
                    # Compare artists for matching songs
                    if artist_i == artist_j:
                        matching_artists[song_name].append((artist_i, i, j))

# Display results
print('Matching Songs:')
for song_name, file_pairs in matching_songs.items():
    print(f'{song_name} appears in files: ', end='')
    for pair in file_pairs:
        print(f'{pair[0]} and {pair[1]} ', end='')
    print()

print('\nMatching Songs with the Same Artist:')
for song_name, artist_info in matching_artists.items():
    artist_name = artist_info[0][0]
    print(f'{song_name} by {artist_name} appears in files: ', end='')
    for info in artist_info:
        print(f'{info[1]} and {info[2]} ', end='')
    print()