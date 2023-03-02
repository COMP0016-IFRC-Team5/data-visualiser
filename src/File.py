import glob
import os
import pandas as pd

def get_file_paths():
    """
    Returns a list of file paths for sliced data sheets. 
    """
    os.chdir("../")
    file_paths = []
    directory = f'{"data"}/{"sliced_data_sheets/*/*"}'

    for fn in glob.glob(directory):
        file_paths.append(fn)

    return file_paths

# if os.path.isfile(fn) and fn[-3:] == "csv":
#         file_paths.append(fn)
      
def country_and_event(paths_):
    """
    Retrives the country name and event type from the file path

    """
    k = paths_[24:]
    upper = k.find('/')
    country = paths_[24: 24 + upper]

    event = paths_[25 + upper: -4]
    return country, event

def paths():
    """Calls the get file paths function and returns the output."""
    paths_ = get_file_paths()
    return paths_

def df(path):
    '''Returns a pandas data frame.'''
    return pd.read_csv(path)