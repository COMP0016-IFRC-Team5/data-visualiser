from enum import Enum


class Folders(Enum):
    unsliced = "unsliced_data_sheets"
    sliced = "sliced_data_sheets"

    def __eq__(self, other):
        return self.value == other.value
