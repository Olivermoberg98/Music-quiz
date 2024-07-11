clear all; close all; clc

folder_path = "mixed_v0";
file_name = "hitster_data_mixed_v0.xlsx";
column_name = "AlbumReleaseYear";

% Construct the full file path
file_path = fullfile(folder_path, file_name);

% Read the data from the specified column in the Excel file
data = readtable(file_path);
years_str = data{:, column_name};

% Convert the strings to integers
years = str2double(years_str);

% Check for and handle NaN values that may result from non-numeric strings
if any(isnan(years))
    warning('Some entries could not be converted to numbers and will be ignored.');
    years = years(~isnan(years)); % Remove NaN entries
end

% Define the histogram bins (5-year intervals)
start_year = floor(min(years)/5)*5; % Start year rounded down to nearest 5
end_year = ceil(max(years)/5)*5; % End year rounded up to nearest 5
bins_5yr = start_year:5:end_year;

% Define bins for individual years
unique_years = min(years):max(years) + 1; % Create bin edges for each individual year

% Create the figure
figure;

% Subplot 1: Histogram with 5-year intervals
subplot(2, 1, 1);
histogram(years, bins_5yr, 'FaceColor', [0.2 0.2 0.5], 'EdgeColor', 'k');
xlabel('Year');
ylabel('Number of Albums');
title('Album Release Year Histogram (5-Year Intervals)');
xticks(bins_5yr);
grid on;

% Subplot 2: Histogram with individual years
subplot(2, 1, 2);
histogram(years, 'BinEdges', unique_years, 'FaceColor', [0.5 0.2 0.2], 'EdgeColor', 'k');
xlabel('Year');
ylabel('Number of Albums');
title('Album Release Year Histogram (Individual Years)');
xticks(unique_years(1):5:unique_years(end)); % Set x-ticks every 5 years for readability
grid on;
