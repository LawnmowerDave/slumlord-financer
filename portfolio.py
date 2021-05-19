from house import House
from mortgage import Mortgage
from house import House
from mortgage import Mortgage
from revenue import Revenue
from cost import Cost
import pandas as pd
import matplotlib.pyplot as plt

class Portfolio:

    def __init__(self, houses) -> None:
        self.__houses = houses


    def get_years_to_positive(self, house):
        """this function takes a house and estimates how many years it will
        take until the house will take until your investment breaks even.
        TODO: this method is inefficient and there's probably a better more
        mathematical way to find it. Probably with calculus

        Args:
            house ([type]): [description]

        Returns:
            [type]: [description]
        """
        for i in range(1, 80):
            dates = pd.date_range("2021-05-01", periods=i * 12, freq="M")
            house.set_new_datetime_index(dates)

            profit = house.net_profit()

            if profit > 0:
                return i


        return -1

    
