from ._utils import Directory
from ._adapters import Folders

__all__ = ['set_data_folder', 'get_data_folder', 'get_selected_folder']

__DATA_FOLDER: Directory | None = None
__SELECTED_FOLDER = Folders.unsliced


def set_data_folder(path):
    global __DATA_FOLDER
    __DATA_FOLDER = Directory(path)


def get_data_folder():
    if __DATA_FOLDER is None:
        raise ValueError('Data folder not set. '
                         'Please call set_data_folder() first.')
    return __DATA_FOLDER


def get_selected_folder():
    return __SELECTED_FOLDER
