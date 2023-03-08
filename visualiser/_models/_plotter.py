import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

__all__ = ['Plotter']


class Plotter:
    def __init__(self, country: str, event: str, df: pd.DataFrame, loss: str):
        self.__x = df[loss]
        self.__y = df['return_period']
        self.__loss = loss
        self.__country = country
        self.__event = event

    def plot(self):
        plt.plot(self.__x, self.__y, 'b-')
        plt.xlabel(self.__loss)
        plt.ylabel('Return period')
        plt.title(f'{self.__country} - {self.__event}')
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        self.__highlight(plt)
        plt.show()

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
            plot.text(
                corresponding_loss, start_return_period,
                f'({round(corresponding_loss)}, {round(start_return_period)})',
                ha='center', va='bottom'
            )
            highlight_point(start_return_period + 2)

        # Call the recursive function with the initial start point
        highlight_point(start_point)
