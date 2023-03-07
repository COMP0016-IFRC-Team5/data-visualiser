import pandas
class last_15_year():
    def __init__(self, df, year):
        self.df = df
        self.year = year

    def get_last_15_year(self):
        rslt_df = self.df[self.df['start_date'] > '2008' ]
        print(rslt_df)
        # rslt_df.reset_index(names=['start_date'])
        rslt_df.index = range(len(rslt_df))
        print(rslt_df)
        return rslt_df
