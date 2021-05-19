import pandas as pd


class Mortgage:

    def __init__(self, amount, down, amortization, apr) -> None:
        """Mortgage

        Args:
            amount (float): mortgage amount
            down (float): down payment
            amortization (int): number of months
            apr (float): percentage
        """
        self.__amount = amount

        if down >= amount:
            self.__down = amount
        else:
            self.__down = down

        self.__amortization = amortization
        self.__apr = apr / 100

    def to_costs(self) -> pd.Series:


        costs = []

        # theoretical amount
        debt = self.amount - self.down

        # principle per month is paid evenly throughout amortization period
        ppm = debt / len(self.amortization)

        for i in range(len(self.__amortization)):
            cost = 0

            # interest per month
            ipm = (debt * self.apr) / 12

            # print(f'debt: {debt} principle: {ppm} interest: {ipm}')
            cost -= (ppm + ipm)

            # you technically pay the down payment when you first take out a
            # mortgage so this is here to reflect that as an actual cost
            if i == 0:
                cost -= self.__down

            debt -= ppm
            costs.append(cost)

        costs_series = pd.Series(
            costs, index=self.amortization, name="mortgage")

        return costs_series

    @property
    def down(self):
        return self.__down

    @property
    def amount(self):
        return self.__amount

    @property
    def amortization(self):
        return self.__amortization

    @property
    def apr(self):
        return self.__apr
