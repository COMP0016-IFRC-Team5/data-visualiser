import pandas as pd

from _utils import Directory

__all__ = ["DataFrameAdapter"]


class DataFrameAdapter:
    def __init__(self, country: Directory, event: str):
        file = country.find_file(event)
        self.dataframe = pd.read_csv(file.get_filepath())
