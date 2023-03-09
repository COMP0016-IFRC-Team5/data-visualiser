__all__ = [
    'FolderSelector',
]

from .._utils import Directory
from ._folders import Folders


class FolderSelector:
    """A class for selecting and accessing a specific folder.

    Attributes:
        __data_folder (Directory): The root directory containing all folders.
        __selected_folder (Directory | None): The selected folder.

    Args:
        data_folder (Directory): The root directory containing all folders.

    """
    def __init__(self, data_folder: Directory):
        self.__data_folder = data_folder
        self.__selected_folder: Directory | None = None

    def select_folder(self, folder: Folders):
        """Select a folder.

        Args:
            folder (Folders): The folder to select.

        """
        self.__selected_folder = self.__data_folder.find_directory(folder.value)

    @property
    def selected_folder(self) -> Directory:
        """Directory: The selected folder.

        Raises:
            ValueError: If no folder has been selected.

        """
        if self.__selected_folder is None:
            raise ValueError('Folder not selected. '
                             'Please call select_folder() first.')
        return self.__selected_folder
