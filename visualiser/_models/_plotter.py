import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__all__ = ['Plotter']


class Plotter:
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
        if sliced and required_years != -1:
            line.set_label(f'{required_years}_sliced')

        elif sliced:
            line.set_label("sliced")

        elif required_years != -1:
            line.set_label(f'{required_years}_unsliced')

        else:
            line.set_label("unsliced")

    def __is_data_sufficient(self):
        return self.__y.nunique() >= 4 or self.__y.max() >= 10

    def __highlight(self, plot):
        start_point = 1 if self.__y.min() > 0 else self.__y.min()
        end = 10 if self.__y.max() > 10 or math.isnan(self.__y.max()) \
            else self.__y.max()

        def highlight_point(start_return_period):
            if not self.__is_data_sufficient() or start_return_period > end:
                return
            corresponding_loss = \
                np.interp(start_return_period, self.__y, self.__x)
            plot.plot(corresponding_loss, start_return_period, 'ro')
            self.__table = pd.concat(
                [self.__table, pd.DataFrame(
                    [[start_return_period, corresponding_loss]],
                    columns=['Return period', self.__loss],
                )],
                ignore_index=True
            )
            plot.text(
                corresponding_loss, start_return_period,
                f'({round(corresponding_loss)}, {round(start_return_period)})',
                ha='center', va='bottom'
            )
            highlight_point(start_return_period + 2)

        # Call the recursive function with the initial start point
        highlight_point(start_point)

    def get_table(self):
        return self.__table
