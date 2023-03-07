import _config


def set_data_folder(path):
    _config.set_data_folder(path)
    ...


def get_data_folder():
    return _config.get_data_folder()


__all__ = [
    'set_data_folder',
    'get_data_folder',
]
