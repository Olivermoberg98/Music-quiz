import pandas as pd
import os

# Configuration
folder_path = "hitster_v2"
file_name = "hitster_data_hitster_v2.xlsx"
column_name = "Artist"  # Artist or SongName

# Construct the full file path
file_path = os.path.join(folder_path, file_name)

# Read the data from the specified column in the Excel file
data = pd.read_excel(file_path)
artist_data = data[column_name]

# Count the occurrences of each artist
artist_counts = artist_data.value_counts()

# Display the top artists with the most songs
top_n = 30
if len(artist_counts) < top_n:
    top_n = len(artist_counts)  # Adjust if fewer than 30 artists

print(f'Top {top_n} Artists with the Most Songs:')
for artist, count in artist_counts.head(top_n).items():
    print(f'{artist}: {count} songs')