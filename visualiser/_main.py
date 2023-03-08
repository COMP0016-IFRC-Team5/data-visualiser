from enum import Enum

import pandas as pd

from . import _config
from ._adapters import CountryAdapter, FolderSelector, Folders, DataFrameAdapter
from ._models import Loss, ReturnPeriodCalculator

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
    # folder_selector.select_folder(Folders.sliced)
    _country_adapter = CountryAdapter(folder_selector.selected_folder)


def get_data_folder():
    return _config.get_data_folder()


def get_available_countries() -> list[str]:
    return _country_adapter.countries


def __country_event_df(countries, events):
    if isinstance(countries, str):
        countries = [countries]
    if isinstance(events, str):
        events = [events]
    # filter out countries that are not available
    unavailable_countries = set(countries) - set(_country_adapter.countries)
    if len(unavailable_countries) > 0:
        print(f'Countries {unavailable_countries} are not available')
    countries = list(set(countries) - unavailable_countries)
    # uppercase all events
    events = list(map(lambda event: event.upper(), events))
    return {
        country: {
            event: DataFrameAdapter(
                _country_adapter.get_country(country), event
            ).dataframe
            for event in events
        }
        for country in countries
    }


def plot_exceedance_curves(
        countries: list[str] | str,
        events: list[str] | str,
        losses: list[Loss] | Loss,
        years_required: int = -1
):
    if isinstance(losses, Enum):
        losses = [losses]
    country_event_dataframes = __country_event_df(countries, events)
    __plot_all(country_event_dataframes, losses, years_required)


def __plot_all(country_event_dataframes, metrics: list[Loss], years_required):
    for country in country_event_dataframes:
        for event in country_event_dataframes[country]:
            for metric in metrics:
                __plot_one(
                    metric,
                    country,
                    event,
                    country_event_dataframes[country][event],
                    years_required
                )


def __plot_one(metric, country, event, df, years_required):
    rpc = ReturnPeriodCalculator(country, event, df, metric, years_required)
    rpc.plot()


def get_exceedance_table(countries, events):
    country_event_dataframes = __country_event_df(countries, events)
    return __get_all_tables(country_event_dataframes)


def __get_all_tables(country_event_dataframes):
    country_event_table = {}
    for country in country_event_dataframes:
        event_table = {}
        for event in country_event_dataframes[country]:
            metrics_table = None
            for metric in Loss:
                table = __get_one_table(
                    metric,
                    country,
                    event,
                    country_event_dataframes[country][event]
                )
                if metrics_table is None:
                    metrics_table = table
                else:
                    metrics_table = pd.merge(
                        metrics_table, table, on='Return period', how='outer'
                    )
            event_table[event] = metrics_table
        country_event_table[country] = event_table
    return country_event_table


def __get_one_table(metric, country, event, df):
    rpc = ReturnPeriodCalculator(country, event, df, metric)
    return rpc.get_table()
