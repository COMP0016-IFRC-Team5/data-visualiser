import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__all__ = ['Plotter']


class Plotter:
    """
    A class that plots the return period curve and highlights certain points
    with their corresponding loss values.

    Args:
        country (str): Country name
        event (str): Event name
        x (pandas.Series): Loss values
        y (pandas.Series): Return period values
        loss (str): Type of loss

    Attributes:
        __x (pandas.Series): Loss values
        __y (pandas.Series): Return period values
        __loss (str): Type of loss
        __country (str): Country name
        __event (str): Event name
        __table (pandas.DataFrame): A table containing highlighted points
            and their corresponding loss and return period values.

    Methods:
        plot: Plots the return period curve and highlights certain points
            with their corresponding loss values.
        get_table: Returns a table containing highlighted points and their
            corresponding loss and return period values.
    """
    def __init__(self, country: str, event: str, x, y, loss: str):
        self.__x = x
        self.__y = y
        self.__loss = loss
        self.__country = country
        self.__event = event
        self.__table = pd.DataFrame()

    def plot(
            self, show_graph: bool = True,
            sliced: bool = False,
            required_years: int = -1
    ):
        """
        Plots the return period curve and highlights certain points
        with their corresponding loss values.

        Args:
            show_graph (bool, optional): Whether to show the graph or not.
                Defaults to True.
            sliced (bool, optional): Whether the data is sliced or not.
                Defaults to False.
            required_years (int, optional): A return period value to
                highlight. Defaults to -1.
        """
        line, = plt.plot(self.__x, self.__y)
        plt.xlabel(self.__loss)
        plt.ylabel('Return period (years)')
        plt.title(f'{self.__country} - {self.__event}')
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        Plotter.__add_label(line, sliced, required_years)
        plt.legend()
        self.__highlight(plt)
        if show_graph:
            plt.show()

    @staticmethod
    def __add_label(line, sliced, required_years):
        """
        Adds label to the plotted curve based on the given input values.

        Args:
            line: A plotted line.
            sliced (bool): Whether the data is sliced or not.
            required_years (int): A return period value to highlight.
        """
        if sliced and required_years != -1:
            line.set_label(f'{required_years}_sliced')

        elif sliced:
            line.set_label("sliced")

        elif required_years != -1:
            line.set_label(f'{required_years}_unsliced')

        else:
            line.set_label("unsliced")

    def __is_data_sufficient(self):
        """
        Checks if the given data is sufficient for plotting or not.

        Returns:
            bool: Whether the given data is sufficient or not.
        """
        return self.__y.nunique() >= 4 or self.__y.max() >= 10

    def __highlight(self, plot):
        """
        Highlights certain points with their corresponding loss values
        and creates a table.

        Args:
            plot: The current plot object.
        """
        start_point = 1 if self.__y.min() > 0 else round(self.__y.min())
        end = 10 if self.__y.max() > 10 or math.isnan(self.__y.max()) \
            else round(self.__y.max())
        accepted_return_periods = [1, 3, 5, 10]

        def highlight_point(start_return_period):
            """Recursively highlights points in the plot and adds corresponding
            data to the table.

            Args:
                start_return_period (int): The return period to start
                highlighting from.
            """
            if start_return_period > end:
                return
            if start_return_period not in accepted_return_periods:
                highlight_point(start_return_period + 1)
                return
            corresponding_loss = \
                np.interp(start_return_period, self.__y, self.__x)
            plot.plot(corresponding_loss, start_return_period, 'ro')
            self.__table = pd.concat(
                [self.__table, pd.DataFrame(
                    [[start_return_period, round(corresponding_loss)]],
                    columns=['Return period', self.__loss],
                )],
                ignore_index=True
            )
            plot.text(
                corresponding_loss, start_return_period,
                f'({round(corresponding_loss)}, {round(start_return_period)})',
                ha='center', va='bottom'
            )
            highlight_point(start_return_period + 1)

        # Call the recursive function with the initial start point
        highlight_point(start_point)

    def get_table(self):
        """
        Returns a table containing highlighted points and their
        corresponding loss and return period values.

        Returns:
            pandas.DataFrame: A table containing highlighted points and their
            corresponding loss and return period values.
        """
        return self.__table
