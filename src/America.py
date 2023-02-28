import os
import pandas as pd
from utils import Directory


# Iterate files in America folder
def America():
    directory = Directory('data/America')
    all_files = directory.get_all_files()
    EARTHQUAKES = [pd.read_csv(file.get_filepath()) for file in all_files if 'EARTHQUAKE' in file.get_filename()]
    FLOODS = [pd.read_csv(file.get_filepath()) for file in all_files if 'FLOOD' in file.get_filename()]
    STORMS = [pd.read_csv(file.get_filepath()) for file in all_files if 'STORM' in file.get_filename()]

    # Concatenate all dataframes
    EARTHQUAKE_df = pd.concat(EARTHQUAKES, ignore_index=True)
    FLOOD_df = pd.concat(FLOODS, ignore_index=True)
    STORM_df = pd.concat(STORMS, ignore_index=True)

    EARTHQUAKE_df.to_csv('data/America_EARTHQUAKES.csv', index=False)
    FLOOD_df.to_csv('data/America_FLOODS.csv', index=False)
    STORM_df.to_csv('data/America_STORMS.csv', index=False)


if __name__ == '__main__':
    America()