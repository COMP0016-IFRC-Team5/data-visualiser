from ._utils import Directory
from ._adapters import Folders

__all__ = ['set_data_folder', 'get_data_folder', 'get_selected_folder']

__DATA_FOLDER: Directory | None = None
__SELECTED_FOLDER = Folders.sliced


def set_data_folder(path):
    """
    Sets the path of the data folder.
    Args:
        path (str): The path to the data folder.
    """
    global __DATA_FOLDER
    __DATA_FOLDER = Directory(path)


def get_data_folder():
    """
    Returns the path of the data folder.

    Raises:
        ValueError: If the data folder has not been set.

    Returns:
        Directory: The path to the data folder.
    """
    if __DATA_FOLDER is None:
        raise ValueError('Data folder not set. '
                         'Please call set_data_folder() first.')
    return __DATA_FOLDER


def get_selected_folder():
    """
    Returns the selected folder.

    Returns:
        Folders: The selected folder.
    """
    return __SELECTED_FOLDER
