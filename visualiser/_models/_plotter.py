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

    def __highlight(self, plot):
        def highlight_point(highlighted_return_period):
            if highlighted_return_period >= (self.__x.max() - self.__x.min()) + 1 or highlighted_return_period > 20:
                return
            corresponding_loss = np.interp(highlighted_return_period, self.__y, self.__x)
            plot.plot(corresponding_loss, highlighted_return_period, 'ro')
            plot.text(
                corresponding_loss, highlighted_return_period,
                f'({round(corresponding_loss)}, {round(highlighted_return_period)})',
                ha='center', va='bottom'
            )
            highlight_point(highlighted_return_period + 2)

        # Call the recursive function with the initial start point
        highlight_point(1)
