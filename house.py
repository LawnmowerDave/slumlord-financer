from mortgage import Mortgage
from asset import Asset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class House:

    def __init__(self, revenues, costs, mortgage, datetime_index, appreciation_rate=3.0):
        """This blueprint of a house is going to be used for long-term 
        financial forecasting including a large number of arbitrary revenue
        and cost variables. All of this data is based on a singular pandas
        time series that indicates the number of months

        Args:
            revenues (list): a list of revenues
            costs (list): the costs
            mortgage (Mortgage): the mortgage for the house
            appreciation_rate (float, optional): rate of appreciation. Defaults to 3.0.
        """
        self.__mortgage = mortgage
        # take a list of series for each and turn them into a df

        self.__revenues = revenues
        self.__costs = costs

        # create a couple of dataframes with the newly created series
        self.__series_revenues = pd.DataFrame(
            [i.to_series(datetime_index) for i in revenues]).transpose()
        self.__series_costs = pd.DataFrame(
            [i.to_series(datetime_index) for i in costs]).transpose()

        self.datetime_index = datetime_index

        self.__appreciation_rate = appreciation_rate / 100
        self.__value = self.__mortgage.amount

        # insert mortgage into the costs
        self.__mortgage_costs = self.__mortgage.to_costs()

        self.__series_costs['mortgage'] = self.__mortgage_costs

        self.appreciation = House.get_appreciation_curve(
            self.__value, appreciation_rate, mortgage)

    def set_new_datetime_index(self, datetime_index):

        # create a couple of dataframes with the newly created series
        self.__series_revenues = pd.DataFrame(
            [i.to_series(datetime_index) for i in self.__revenues]).transpose()
        self.__series_costs = pd.DataFrame(
            [i.to_series(datetime_index) for i in self.__costs]).transpose()

        self.__mortgage = Mortgage(self.__value, self.__mortgage.down,
                    datetime_index, self.__mortgage.apr)

        self.__mortgage_costs = self.__mortgage.to_costs()

        self.__series_costs['mortgage'] = self.__mortgage_costs

        self.appreciation = House.get_appreciation_curve(
            self.__value, self.__appreciation_rate, self.__mortgage)

    @staticmethod
    def get_appreciation_curve(value, appreciation_rate, mortgage):
        # calculate appreciation
        index = mortgage.amortization

        appreciation_array = []

        # create a time series for the amount the house appreciates
        for time in index:
            amount = (value * appreciation_rate) / 12
            transfer = Asset("appreciation", "home appreciation", amount)
            appreciation_array.append(transfer)

        return pd.Series(appreciation_array, index=index, name="appreciation")


    def total_cost(self) -> float:
        total_cost = 0

        for index, row in self.__series_costs.iterrows():
            for cost in row:
                total_cost += cost

        return total_cost

    def total_revenue(self) -> float:
        """return the amount of pure revenue coming in every month, not 
        including assets from house appreciation

        Returns:
            float: the total revenue
        """
        total_revenue = 0

        for index, row in self.__series_revenues.iterrows():
            for revenue in row:
                total_revenue += revenue

        return total_revenue

    def total_assets(self) -> float:
        """the total number of assets from the house. These are considered 
        non-liquidable and are thus kept separate from revenue

        Returns:
            float: the total number of assets
        """
        return self.appreciation.sum().amount

    def total_profit(self) -> float:
        """the total amount of gains from both revenue and assets

        Returns:
            float: total gains
        """
        return self.total_revenue() + self.total_assets()

    def net_profit(self) -> float:
        """the total number of gains minus the costs

        Returns:
            float: net gain
        """
        return self.total_profit() + self.total_cost()

    def net_revenue(self) -> float:
        """the total revenue minus cost. This does not include house assets

        Returns:
            float: the net revenue minus costs
        """
        return self.total_revenue() + self.total_cost()


    def graph_net_profit(self):
        # sum costs across 1st axis (horizontally)
        costs = self.__series_costs.sum(axis=1).cumsum()
        profits = self.__series_revenues.sum(axis=1).cumsum()

        net = costs + profits

        # print(net)

        plt.plot(net.index, net)
        plt.title("House investment")
        plt.xlabel("Years")
        plt.ylabel("Net profit")
        # plt.axvline(x=2020, color='k', linestyle='--')
        plt.axhline(y=0, color='k', linestyle='--')
        plt.show()

        plt.close()

    def summary(self) -> float:

        print('Summary')
        print('-------------------------------------------')
        print("total cost      ", self.total_cost())
        print("total revenue   ", self.total_revenue())
        print("net revenue     ", self.net_revenue())

        print("total assets    ", self.total_assets())

        print("total profit    ", self.total_profit())
        print("net profit      ", self.net_profit())
