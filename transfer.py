import pandas as pd

class Transfer:

    def __init__(self, name, desc, amount) -> None:
        self.__name = name
        self.__desc = desc
        self.__amount = amount

    def __add__(self, other):
        return Transfer(self.name, self.desc, self.amount + other.amount)

    def __mul__(self, other):
        return Transfer(self.name, self.desc, self.amount * other.amount)
    
    def __sub__(self, other):
        return Transfer(self.name, self.desc, self.amount - other.amount)

    def __repr__(self) -> str:
        return self.__name

    def to_series(self, dates) -> pd.Series:
        """duplicates this transfer for n months in a pandas series

        Args:
            months (int): n number of months

        Returns:
            pd.Series: the costs series
        """
        return pd.Series([self.amount] * len(dates), index=dates, name=self.name)

    @property
    def name(self):
        return self.__name

    @property
    def desc(self):
        return self.__desc

    @property
    def amount(self):
        return self.__amount

    @property
    def is_percentage(self):
        return self.__percentage_of
