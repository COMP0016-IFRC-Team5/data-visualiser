from enum import Enum


class Folders(Enum):
    """An enumeration of folder names.

    Each member of the enumeration represents the name of a specific folder.

    """
    unsliced = "unsliced_data_sheets"
    sliced = "sliced_data_sheets"

    def __eq__(self, other):
        """Check if two Folders have the same value.

        Args:
            other (Folder): The other Folder to compare against.

        Returns:
            bool: True if the Folders have the same value; False otherwise.

        """
        return self.value == other.value
