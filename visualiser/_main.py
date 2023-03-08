from enum import Enum

import _config
from _adapters import CountryAdapter, FolderSelector, Folders, DataFrameAdapter
from _models import Loss, ReturnPeriodCalculator

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


def plot_exceedance_curves(
        countries: list[str] | str,
        events: list[str] | str,
        losses: list[Loss] | Loss):
    if isinstance(countries, str):
        countries = [countries]
    if isinstance(events, str):
        events = [events]
    if isinstance(losses, Enum):
        losses = [losses]
    # filter out countries that are not available
    unavailable_countries = set(countries) - set(_country_adapter.countries)
    if len(unavailable_countries) > 0:
        print(f'Countries {unavailable_countries} are not available')
    countries = list(set(countries) - unavailable_countries)
    # uppercase all events
    events = list(map(lambda event: event.upper(), events))
    country_event_dataframes = {
        country: {
            event: DataFrameAdapter(
                _country_adapter.get_country(country), event
            ).dataframe
            for event in events
        }
        for country in countries
    }
    __plot_all(country_event_dataframes, losses)


def __plot_all(country_event_dataframes, metrics: list[Loss]):
    for country in country_event_dataframes:
        for event in country_event_dataframes[country]:
            for metric in metrics:
                __plot_one(
                    metric,
                    country,
                    event,
                    country_event_dataframes[country][event]
                )


def __plot_one(metric, country, event, df):
    rpc = ReturnPeriodCalculator(country, event, df, metric)
    rpc.plot()


def get_exceedance_table(countries, events):
    ...
