import pandas as pd

from .._utils import Directory

__all__ = ["DataFrameAdapter"]


class DataFrameAdapter:
    """A class for reading event data into a Pandas DataFrame.

    Attributes:
        dataframe (pd.DataFrame): The Pandas DataFrame containing the event
            data.

    Args:
        country (Directory): The directory representing the country where the
            event occurred.
        event (str): The name of the event to read.

    """
    def __init__(self, country: Directory, event: str):
        file = country.find_file(f"{event}.csv")
        self.dataframe = pd.read_csv(file.get_filepath())
