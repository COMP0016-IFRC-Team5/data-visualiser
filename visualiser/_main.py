import _config
from _adapters import CountryAdapter, EventAdapter, FolderSelector, Folders

__all__ = [
    'set_data_folder',
    'get_data_folder',
    'get_available_countries',
    'plot_exceedance_curves',
    'get_exceedance_table',
]

_country_adapter: CountryAdapter | None = None


def set_data_folder(path):
    global _country_adapter
    _config.set_data_folder(path)
    folder_selector = FolderSelector(_config.get_data_folder())
    folder_selector.select_folder(Folders.unsliced)
    _country_adapter = CountryAdapter(folder_selector.selected_folder)


def get_data_folder():
    return _config.get_data_folder()


def get_available_countries() -> list[str]:
    return _country_adapter.countries


def plot_exceedance_curves(countries, events, losses):
    ...


def get_exceedance_table(countries, events):
    ...
