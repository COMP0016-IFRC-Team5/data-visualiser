from GraphDataFrame import GraphDataFrame
from Enums import  Loss
from File import country_and_event, df, paths
from Last15Years import last_15_year

import pandas as pd


def main():
    paths_ = paths()
    paths_ = ['./data/America_EARTHQUAKES.csv', './data/America_FLOODS.csv', './data/America_STORMS.csv']
    print(paths_)
    for path in paths_:     
        country_, event_ = country_and_event(path)

        graph = GraphDataFrame()
        last15 = last_15_year(df(path), 14)
        graph.dataframe = last15.get_last_15_year()

        graph.set_data([1,10], country_, event_, Loss.Deaths)

        if len(graph.dataframe) > 5:
            plt = graph.calculate_return_period()
            plt.plot()

main()