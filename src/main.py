from GraphDataFrame import GraphDataFrame
from Enums import  Loss
from File import country_and_event, df, paths

import pandas as pd


def main():
    paths_ = paths()
    print(paths_)
    for path in paths_:     
        country_, event_ = country_and_event(path)

        graph = GraphDataFrame()
        graph.dataframe = df(path)

        graph.set_data([1,10], country_, event_, Loss.Deaths)

        if len(graph.dataframe) > 5:
            plt = graph.calculate_return_period()
            plt.plot()

main()