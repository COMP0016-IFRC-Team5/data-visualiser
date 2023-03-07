import _config


def set_data_folder(path):
    _config.set_data_folder(path)
    ...


def get_data_folder():
    return _config.get_data_folder()


def get_available_countries():
    ...


def plot_exceedance_curves(countries, events, losses):
    ...


__all__ = [
    'set_data_folder',
    'get_data_folder',
    'get_available_countries',
    'plot_exceedance_curves',
]
