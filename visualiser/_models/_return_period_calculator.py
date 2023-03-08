import pandas as pd

from visualiser import Loss

__all__ = ['ReturnPeriodCalculator']


class ReturnPeriodCalculator:
    def __init__(self, country: str, event: str, df: pd.DataFrame, loss: Loss):
        self.__dataframe = df
        self.__loss = loss
        self.__country = country
        self.__event = event
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

    def __calculate_exceedance_frequency(self):
        """
        Calculates the exceedance frequency for each row in the dataframe
        """
        length = self.__length_in_years()
        series = pd.Series()
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
        self.__dataframe['return_period'] = 1 / exceedance_frequency

    def get_data(self):
        return self.__dataframe, self.__loss, self.__country, self.__event

    def plot(self):
        ...
