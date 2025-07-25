clear all; close all; clc

% Define file paths and column names
folder_paths = ["movies_v0", "movies_v1"];
file_names = ["hitster_data_movies_v0.xlsx", "hitster_data_movies_v1.xlsx"];
column_name_artist = "Artist";
column_name_song = "AlbumReleaseYear";

% Initialize cell arrays to store data
artists = cell(1, length(file_names));
songs = cell(1, length(file_names));

% Read data from each file
for i = 1:length(file_names)
    file_path = fullfile(folder_paths{i}, file_names{i});
    data = readtable(file_path);
    artists{i} = data{:, column_name_artist};
    songs{i} = data{:, column_name_song};
end

% Initialize containers for matching songs
matching_songs = containers.Map;
matching_artists = containers.Map;

% Compare song names across all files
for i = 1:length(file_names)
    for j = i+1:length(file_names)
        [common_songs, idx_i, idx_j] = intersect(songs{i}, songs{j});
        for k = 1:length(common_songs)
            song_name = common_songs{k};
            artist_i = artists{i}{idx_i(k)};
            artist_j = artists{j}{idx_j(k)};
            
            % Store matching songs
            if ~isKey(matching_songs, song_name)
                matching_songs(song_name) = {};
            end
            matching_songs(song_name) = [matching_songs(song_name); {i, j}];
            
            % Compare artists for matching songs
            if strcmp(artist_i, artist_j)
                if ~isKey(matching_artists, song_name)
                    matching_artists(song_name) = {};
                end
                matching_artists(song_name) = [matching_artists(song_name); {artist_i, i, j}];
            end
        end
    end
end

% Display results
fprintf('Matching Songs:\n');
matching_song_keys = keys(matching_songs);
for i = 1:length(matching_song_keys)
    song_name = matching_song_keys{i};
    fprintf('%s appears in files: ', song_name);
    file_indices = matching_songs(song_name);
    for j = 1:length(file_indices)
        fprintf('%d and %d ', file_indices{j});
    end
    fprintf('\n');
end

fprintf('\nMatching Songs with the Same Artist:\n');
matching_artist_keys = keys(matching_artists);
for i = 1:length(matching_artist_keys)
    song_name = matching_artist_keys{i};
    artist = matching_artists(song_name);
    fprintf('%s by %s appears in files: ', song_name, artist{1,1});
    file_indices = matching_artists(song_name);
    for j = 1:size(file_indices, 1)
        fprintf('%d and %d ', file_indices{j,2}, file_indices{j,3});
    end
    fprintf('\n');
end
