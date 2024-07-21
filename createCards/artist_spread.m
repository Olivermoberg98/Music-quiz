clear all; close all; clc

folder_path = "mixed_v0";
file_name = "hitster_data_mixed_v0.xlsx";
column_name = "Artist";

% Construct the full file path
file_path = fullfile(folder_path, file_name);

% Read the data from the specified column in the Excel file
data = readtable(file_path);
artist_str = data{:, column_name};

% Convert artist_str to a categorical array
artist_categorical = categorical(artist_str);

% Count the occurrences of each artist
artist_counts = tabulate(artist_categorical);

% Sort the artists by the number of songs in descending order
[~, sortIdx] = sort([artist_counts{:, 2}], 'descend');
sorted_artists = artist_counts(sortIdx, 1);
sorted_counts = [artist_counts{sortIdx, 2}];

% Display the top 3 artists with the most songs
top_n = 5;
if numel(sorted_artists) < top_n
    top_n = numel(sorted_artists); % Adjust if fewer than 3 artists
end

fprintf('Top %d Artists with the Most Songs:\n', top_n);
for i = 1:top_n
    fprintf('%s: %d songs\n', sorted_artists{i}, sorted_counts(i));
end
