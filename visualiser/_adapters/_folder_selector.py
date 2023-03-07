__all__ = [
    'FolderSelector',
]

from _utils import Directory
from ._folders import Folders


class FolderSelector:
    def __init__(self, data_folder: Directory):
        self.__data_folder = data_folder
        self.__selected_folder: Directory | None = None

    def select_folder(self, folder: Folders):
        self.__selected_folder = self.__data_folder.find_directory(folder.value)

    @property
    def selected_folder(self) -> Directory:
        if self.__selected_folder is None:
            raise ValueError('Folder not selected. '
                             'Please call select_folder() first.')
        return self.__selected_folder
