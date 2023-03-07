import numpy as np
from Enums import Loss
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


class GraphDataFrame():
    def __init__(self):
        self.period = -1

        self.country = None
        self.event = None

        self.loss = None
        self.dataframe: pd.DataFrame = None

    def set_data(self, period, country, event, loss: Loss):
        self.period = period
        self.event = event
        self.country = country
        self.loss = loss

    def get_record_length(self):
        record_end = self.dataframe.iloc[-1, -1]
        record_start = self.dataframe.iloc[0, -3]
        start_date = datetime.strptime(record_start, '%Y-%m-%d')

        end_date = datetime.strptime(record_end, '%Y-%m-%d')
        delta: datetime.timedelta = end_date-start_date

        return delta.days/365

    def get_exceedance_period(self):
        total_record = self.get_record_length()
        loss_frequency = np.cumsum(self.dataframe[self.loss.value].value_counts(ascending = True).sort_index()[::-1])
        return self.dataframe[self.loss.value].map(loss_frequency/total_record)

    def calculate_return_period(self):
        ImpactReturnPeriodGraph = Plot()
        exceedance_period = self.get_exceedance_period()
        sort_index = np.argsort(exceedance_period)[::-1]

        y = 1/exceedance_period[sort_index]
        x = self.dataframe[self.loss.value][sort_index]
        ImpactReturnPeriodGraph.set_graph(x,y, self.country, self.event)

        return ImpactReturnPeriodGraph


class Plot():
    def set_graph(self, x, y, country, event):
        self.x = x
        self.y = y

        self.country = country
        self.event = event

    def plot(self):
        """
        Plots the data and generates a matlab graph 
        
        """
        plt.plot(self.x,self.y)
        self.highlight(plt)
        plt.xlabel(f'Loss {self.event}')
        plt.ylabel(f'Return period {self.country}')

        plt.show()

    def highlight(self,plt):
        start_point = 1
        end = 5
        while True:
            if start_point<(self.x.max()-self.x.min())+1 and start_point <= end:

                highlight_point_x = np.interp(start_point, self.y, self.x)
                plt.plot(highlight_point_x, start_point, 'ro')
                plt.text(highlight_point_x, start_point, f'({round(highlight_point_x)}, {round(start_point)})', ha='center', va='bottom')
                start_point += 2
            else:
                return