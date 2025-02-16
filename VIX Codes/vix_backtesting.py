import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter as ff

def dollar_format(x, _):
    return f'${x:,.2f}'


# # # # #
# Data Analysis Functions
#
#
#

def load():
    """
    load function pulls both the differential data and the spread data for analysis

    """
    file_spreads1 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\1 month Spreads.csv"
    file_spreads2 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\2 month Spreads.csv"
    file_spreads3 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\3 month Spreads.csv"
    file_diff1 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\1 month Differentials.csv"
    file_diff2 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\2 month Differentials.csv"
    file_diff3 = r"c:\Users\andre\VS Code\Projects\VIX\VIX Processed Data\3 month Differentials.csv"
    data_spreads = []
    data_spreads.append(pd.read_csv(file_spreads1))
    data_spreads.append(pd.read_csv(file_spreads2))
    data_spreads.append(pd.read_csv(file_spreads3))
    data_diffs = []
    data_diffs.append(pd.read_csv(file_diff1))
    data_diffs.append(pd.read_csv(file_diff2))
    data_diffs.append(pd.read_csv(file_diff3))
    return data_spreads, data_diffs

# Transaction Functions
def buy(contract, limit):
    fee = 4.76
    buy_prices = contract
    for price in buy_prices:
        if price < limit:
            return (1000*price+fee)
    return False

def sell(contract, limit, sell_window=[-18, None]):
    fee = 4.76
    sale_prices = contract.iloc[sell_window[0]:sell_window[1]]
    for price in sale_prices:
        if price > limit:
            return (1000*price-fee)
    return (1000*sale_prices.iloc[-1]-fee)

def profit(contract, buy_limit, sell_limit, sell_window=[-18, None]):
    cost = buy(contract, buy_limit)
    if cost == False:
        return 0
    proceeds = sell(contract, sell_limit, sell_window=sell_window)
    return proceeds-cost

# Strategy Functions
def spread_sale_price(data, spread=.75, buy_limit=.3, sell_window=[-18, None]):
    profits = []
    for i in range(len(data.iloc[0,:])-1):
        contract = data.iloc[:,i+1]
        cost = buy(contract, buy_limit)
        proceeds = sell(contract, cost+spread, sell_by)
        profits.append(proceeds-cost)
    return pd.DataFrame(profits)

def dynamic_sale_price(data, percent_prior=.8, buy_limit=.3, sell_window=[-18, None]):
    profits = []
    for i in range(len(data.iloc[0,:])-1):
        contract = data.iloc[:,i+1]
        target_price = max(percent_prior*max(data.iloc[0:5,i]), .6) # Calculates percentage of highest value the previous spread reached in last 5 days before expiration
        profits.append(profit(contract, buy_limit, target_price, sell_window=sell_window))
    return pd.DataFrame(profits, columns=['Profits'])






# # # # #
# Sample analysis codes
#
#
#

spread_data, diff_data = load()
x = dynamic_sale_price(spread_data[0])
x.plot(title=f"Histogram of profits n=50\n The total profits from spreads trading is ${round(sum(x.iloc[:,0]))}", kind='hist', bins=50)

ax = x.plot(title=f'Profits line graph\n with mean profit of ${round(x['Profits'].mean())}')
ax.axhline(y=x['Profits'].mean(), color='red', label='Mean')
plt.legend()
plt.show()
