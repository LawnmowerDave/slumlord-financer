import pandas as pd

class Region:

    def __init__(self, dataframe) -> None:
        self.__df = dataframe

    def get_average(self):
        return self.__df["value"].mean()

