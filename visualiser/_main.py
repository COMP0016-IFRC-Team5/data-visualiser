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
    """Sets the data folder to be used for retrieving data.

    Args:
        path: A string specifying the path of the data folder.
    """
    global _country_adapter
    _config.set_data_folder(path)
    folder_selector = FolderSelector(_config.get_data_folder())
    folder_selector.select_folder(_config.get_selected_folder())
    _country_adapter = CountryAdapter(folder_selector.selected_folder)


def get_data_folder():
    """Returns the path of the data folder."""
    return _config.get_data_folder()


def get_available_countries() -> list[str]:
    """Returns a list of all available countries."""
    return _country_adapter.countries


def __country_event_df(countries, events):
    """Returns a dictionary of dataframes, one for each country and event
    combination.

    Args:
        countries: A string or list of strings specifying the countries.
        events: A string or list of strings specifying the events.

    Returns:
        A dictionary of dataframes, one for each country and event combination.
    """
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
    """Plots the exceedance curves for the specified countries, events, and losses.

    Args:
        countries: A string or list of strings specifying the countries.
        events: A string or list of strings specifying the events.
        losses: A Loss enum or list of Loss enums specifying the losses.
        years_required: An int specifying the minimum number of years of data
            required. Default is -1.
    """
    if isinstance(losses, Enum):
        losses = [losses]
    country_event_dataframes = __country_event_df(countries, events)
    __plot_all(country_event_dataframes, losses, years_required)


def __plot_all(country_event_dataframes, metrics: list[Loss], years_required):
    """Plots the exceedance curves for all countries, events, and losses.

    Args:
        country_event_dataframes: A dictionary of dataframes, one for each
            country and event combination.
        metrics: A list of Loss enums specifying the losses.
        years_required: An int specifying the minimum number of years of data
            required.
    """
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
    """Plots the exceedance curve for a single country, event, and loss.

    Args:
        metric: A Loss enum specifying the loss.
        country: A string specifying the country.
        event: A string specifying the event.
        df: A pandas dataframe containing the data.
        years_required: An int specifying the minimum number of years of data
            required.

    """
    rpc = ReturnPeriodCalculator(country, event, df, metric, years_required)
    if _config.get_selected_folder() == Folders.sliced:
        rpc.plot(sliced=True)
    rpc.plot()


def get_exceedance_table(countries, events, years_required: int = -1):
    """Returns a dictionary of tables, one for each country and event
    combination.

    Args:
        countries: A string or list of strings specifying the countries.
        events: A string or list of strings specifying the events.
        years_required: An int specifying the minimum number of years of data
            required. Default is -1.

    Returns:
        A dictionary of tables, one for each country and event combination.
    """
    country_event_dataframes = __country_event_df(countries, events)
    return __get_all_tables(country_event_dataframes, years_required)


def __get_all_tables(country_event_dataframes, years_required: int = -1):
    """Return a dictionary of tables, one for each country and event
    combination.

    Args:
        country_event_dataframes: A dictionary of dataframes, one for each
            country and event combination.
        years_required: An int specifying the number of years of data required.
            Default is -1.

    Returns:
        A dictionary of tables, one for each country and event combination.
    """
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
                    country_event_dataframes[country][event],
                    years_required
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


def __get_one_table(metric, country, event, df, years_required: int = -1):
    """Return a table for a single country, event, and loss.

    Args:
        metric: A Loss enum specifying the loss.
        country: A string specifying the country.
        event: A string specifying the event.
        df: A pandas dataframe containing the data.
        years_required: An int specifying the number of years of data required.

    Returns:
        A pandas dataframe containing the table.
    """
    rpc = ReturnPeriodCalculator(country, event, df, metric, years_required)
    return rpc.get_table()
