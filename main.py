from mortgage import Mortgage
import quandl
import numpy as np
import pickle
import pandas as pd
from region import Region

from house import House
from mortgage import Mortgage
from revenue import Revenue
from cost import Cost
from portfolio import Portfolio

def get_data(indicator, region_id):
    # quandl.ApiConfig.api_key = api_key

    # List of indicators here
    # https://www.quandl.com/tables/ZILLOW/ZILLOW-INDICATORS

    # list of regions here 
    # https://www.quandl.com/tables/ZILLOW/ZILLOW-REGIONS
    data = quandl.get_table('ZILLOW/DATA',
                             indicator_id=indicator, region_id=region_id)
    save(data, f'{region_id}-{indicator}')

    return data

def save(data, name):
    with open(f'data/{name}.pickle', 'wb') as file:
        pickle.dump(data, file)

def load(name):
    with open(f'data/{name}', 'rb') as file:
        return pickle.load(file)

def get_michigan():

    MI_REGIONS = [9635, 873, 889, 9729, 8677, 9936, 8889, 9060,
                  9178, 9504, 9642, 9447, 9313, 9316]

    for region in MI_REGIONS:
        print('fetching region', region)
        get_data("Z2BR", region)


def check_area_ytp(pickle_name):
    data = load(pickle_name)

    n_years = 15
    house_cost = data.loc[0].value
    appreciation = 3.0

    n_months = n_years * 12

    dates = pd.date_range(data.loc[0].date, periods=n_months, freq="M")

    rent = Revenue("rent", "monthly payment", 0.011 * house_cost)

    # costs
    utilities = Cost("utilities", "hvac", 150)
    insurance = Cost("insurance", "full coverage", 100)
    property_tax = Cost("insurance", "full coverage",
                        (house_cost * 0.019) / 12)

    mortgage = Mortgage(house_cost, 25000, dates, 3.0)

    # revenue
    revenues = [rent]
    costs = [utilities, insurance, property_tax]

    house = House(revenues, costs, mortgage, dates, appreciation)
    # house.summary()

    house.graph_net_profit()


    portfolio = Portfolio([house])

    ytp = portfolio.get_years_to_positive(house)
    print("years till positive", ytp)
    exit(0)

    return ytp
    

def main():

    # load 1 bedroom apartments from traverse city

    MI_REGIONS = [9635, 873, 889, 9729, 8677, 9936, 8889, 9060,
                9178, 9504, 9642, 9447, 9313, 9316]
    
    ytps = {}

    for region in MI_REGIONS:
        print('house in', region)
        ytps[f"{region}"] = check_area_ytp(f'{region}-Z2BR.pickle')

    lowest = min([i for i in ytps.keys()])
    print('best house:', ytps[f'{lowest}'], lowest)




if __name__ == '__main__':
    main()