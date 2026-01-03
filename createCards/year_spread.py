import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
folder_path = "hitster_v2"
file_name = "hitster_data_hitster_v2.xlsx"
column_name = "Album Release Year"

# Construct the full file path
file_path = os.path.join(folder_path, file_name)

# Read the data from the specified column in the Excel file
data = pd.read_excel(file_path)
years_str = data[column_name]

# Convert the strings to integers
years = pd.to_numeric(years_str, errors='coerce')

# Check for and handle NaN values
if years.isna().any():
    print('Warning: Some entries could not be converted to numbers and will be ignored.')
    years = years.dropna()

years = years.astype(int)

# Define the histogram bins (5-year intervals)
start_year = (years.min() // 5) * 5  # Start year rounded down to nearest 5
end_year = ((years.max() // 5) + 1) * 5  # End year rounded up to nearest 5
bins_5yr = np.arange(start_year, end_year + 5, 5)

# Define bins for individual years
min_year = years.min()
max_year = years.max()
bins_1yr = np.arange(min_year, max_year + 2, 1)

# Create the figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Subplot 1: Histogram with 5-year intervals
ax1.hist(years, bins=bins_5yr, color=[0.2, 0.2, 0.5], edgecolor='k')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Albums')
ax1.set_title('Album Release Year Histogram (5-Year Intervals)')
ax1.set_xticks(bins_5yr)
ax1.grid(True)

# Subplot 2: Histogram with individual years
ax2.hist(years, bins=bins_1yr, color=[0.5, 0.2, 0.2], edgecolor='k')
ax2.set_xlabel('Year')
ax2.set_ylabel('Number of Albums')
ax2.set_title('Album Release Year Histogram (Individual Years)')
ax2.set_xticks(np.arange(min_year, max_year + 1, 5))  # Set x-ticks every 5 years
ax2.grid(True)

plt.tight_layout()
plt.show()