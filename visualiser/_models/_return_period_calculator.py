import numpy as np
import pandas as pd

from ._loss import Loss
from ._plotter import Plotter

__all__ = ['ReturnPeriodCalculator']


class ReturnPeriodCalculator:
    def __init__(
            self,
            country: str,
            event: str,
            df: pd.DataFrame,
            loss: Loss,
            years_required: int = -1
    ):
        self.__dataframe = df
        self.__loss = loss
        self.__country = country
        self.__event = event
        self.__plot = None
        self.__is_plotted = False
        self.__required_years = years_required
        self.__calculate_return_period()

    def __length_in_years(self):
        """
        Calculates the length of the dataframe in years

        Example:
            # df['start_date'][0] = 1981-09-04
            # df['secondary_end'][0] = 1981-09-09
            # df['start_date'][1] = 1983-09-20
            # df['secondary_end'][1] = 1983-09-25
            self.__length_in_years() = (1983-09-25 - 1981-09-04) / 365 = 2.08
        """
        self.__convert_time()
        return (self.__dataframe['secondary_end'].max() -
                self.__dataframe['start_date'].min()).days / 365

    def __convert_time(self):
        column = ["start_date", "primary_end", "secondary_end"]
        for col in column:
            self.__dataframe[col] = pd.to_datetime(self.__dataframe[col])
        if self.__required_years > 0:
            self.__dataframe = self.__dataframe[
                self.__dataframe['start_date'] >=
                self.__dataframe['start_date'].max() -
                pd.DateOffset(years=self.__required_years)
                ].reset_index()

    def __calculate_exceedance_frequency(self):
        """
        Calculates the exceedance frequency for each row in the dataframe
        """
        length = self.__length_in_years()
        series = None
        match self.__loss:
            case Loss.deaths:
                series = self.__dataframe['deaths']
            case Loss.affected_people:
                series = self.__dataframe['directly_affected'] \
                         + self.__dataframe['indirectly_affected']
                self.__dataframe['affected_people'] = series
        exceedance_num = \
            series.value_counts(ascending=True).sort_index()[::-1].cumsum()

        return self.__dataframe[self.__loss.value.lower().replace(' ', '_')]\
            .map(exceedance_num / length)

    def __calculate_return_period(self):
        """
        Calculates the return period for each row in the dataframe
        """
        exceedance_frequency = self.__calculate_exceedance_frequency()
        sort_index = np.argsort(exceedance_frequency)[::-1]
        loss = self.__loss.value.lower().replace(' ', '_')
        y = 1/exceedance_frequency[sort_index]
        x = self.__dataframe[loss][sort_index]
        self.__plot = Plotter(self.__country, self.__event, x, y, loss)

    def plot(self, sliced: bool = False):
        self.__plot.plot(sliced=sliced, required_years=self.__required_years)
        self.__is_plotted = True

    def get_table(self):
        if not self.__is_plotted:
            self.__plot.plot(False)
        return self.__plot.get_table()
