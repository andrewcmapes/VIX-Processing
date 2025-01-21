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

def Load():
    """
    Load function pulls both the differential data and the spread data for analysis

    """
    file_spreads1 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\1 Month Spreads.csv"
    file_spreads2 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\2 Month Spreads.csv"
    file_spreads3 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\3 Month Spreads.csv"
    file_diff1 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\1 Month Differentials.csv"
    file_diff2 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\2 Month Differentials.csv"
    file_diff3 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\3 Month Differentials.csv"
    data_spreads = []
    data_spreads.append(pd.read_csv(file_spreads1))
    data_spreads.append(pd.read_csv(file_spreads2))
    data_spreads.append(pd.read_csv(file_spreads3))
    data_diffs = []
    data_diffs.append(pd.read_csv(file_diff1))
    data_diffs.append(pd.read_csv(file_diff2))
    data_diffs.append(pd.read_csv(file_diff3))
    return data_spreads, data_diffs


def Strategy(data, buy_cutoff=.3, buy_month=5, spread=.75, quantity=8):
    """
    Strategy backtests different buying and selling strategies for future spreads. The data used
    goes back to August 2013 as seen from the merged data from which spreads are generated. It works
    by identifying criteria for purchase, criteria for sale, and calculates all proceeds from the 
    transactions after subtracting the trading fees.

    Parameters
    ----------
    data : TYPE DataFrame
        DESCRIPTION. Should be the spread data from either 1, 2, or 3 month spreads.
    buy_cutoff : TYPE, float
        DESCRIPTION. The cutoff price at which positions are either taken or not. The default is .3.
    buy_month : TYPE, int
        DESCRIPTION. The time from expiration at which purchase is made measured in months. The default is 5.
    spread : TYPE, float
        DESCRIPTION. The spread between the buy and sell price for early sale. The default is .75.
    quantity : TYPE, int
        DESCRIPTION. The number of contracts held in each position. The default is 8.

    Returns
    -------
    gains : TYPE list
        DESCRIPTION. gains gives the list of all payoffs from profitable trades.
    losses : TYPE list
        DESCRIPTION. losses gives the list of all payoffs from non-profitable trades. 

    """
    fees = 9.52 # Cost of buying and selling a single future spread
    multiplier = 1000 # Value multiplier from spread price
    gains = []
    losses = []
    for i in range(0, len(data.iloc[0,:])):
        col = data.iloc[:,i]
        buy = col[buy_month*21]
        if buy < buy_cutoff:
            sell = buy + spread
            if max(col[0:buy_month*21]) > sell:
                gains.append((spread * multiplier - fees) * quantity)
            else:
                if (col[0]-buy)>0:
                    gains.append(((col[0] - buy) * multiplier - fees) * quantity)
                else:
                    losses.append(((col[0] - buy) * multiplier - fees) * quantity)
    return gains, losses


def Spread_Comparison(data, buy_cutoff=.3, buy_month=5, spreads: list=[.75]):
    gains = []
    losses = []
    profits = []
    for spread in spreads:
        gain, loss = Strategy(data = data, buy_month=buy_month, spread=spread, buy_cutoff=buy_cutoff)
        gains.append(sum(gain))
        losses.append(sum(loss))
        profits.append(sum(gain+loss))
    return profits, gains, losses


def Buy_Cutoff_Comparison(data, buy_cutoffs: list=[.3], buy_month=5, spread=.75):
    gains = []
    losses = []
    profits = []
    for buy_cutoff in buy_cutoffs:
        gain, loss = Strategy(data = data, buy_cutoff = buy_cutoff, buy_month = buy_month, spread = spread)
        gains.append(sum(gain))
        losses.append(sum(loss))
        profits.append(sum(gain+loss))
    return profits, gains, losses


def Buy_Month_Comparison(data, buy_cutoff=.3, buy_months: list=[5], spread=.75):
    gains = []
    losses = []
    profits = []
    for buy_month in buy_months:
        gain, loss = Strategy(data = data, buy_cutoff = buy_cutoff, buy_month = buy_month, spread = spread)
        gains.append(sum(gain))
        losses.append(sum(loss))
        profits.append(sum(gain+loss))
    return profits, gains, losses


def Comparison_Grapher(data, entries: list, comparable: str='spreads', spread=.75, buy_cutoff=.3, buy_month=5) -> None:
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.yaxis.set_major_formatter(ff(dollar_format))
    ax2.yaxis.set_major_formatter(ff(dollar_format))
    if comparable == 'spreads':
        p, g, l = Spread_Comparison(data=data, spreads=entries, buy_cutoff=buy_cutoff ,buy_month=buy_month)
        plt.title('Spreads Comparison')
    elif comparable == 'months':
        p, g, l = Buy_Month_Comparison(data=data, buy_months=entries, buy_cutoff=buy_cutoff, spread=spread)
        plt.title('Months Comparison')
    elif comparable == 'buys':
        p, g, l = Buy_Cutoff_Comparison(data=data, buy_cutoffs=entries, buy_month=buy_month, spread=spread)
        plt.title('Buy Cutoff Comparison')
    
    
    ax1.plot(entries, p, color='green', label='Profits')
    ax1.plot(entries, g, color='blue', label='Gains')
    ax2.plot(entries, l, color='red', label='Losses')
    ax1.legend(bbox_to_anchor=(1, .5))
    ax2.legend(bbox_to_anchor=(1, .60))
    plt.show()


# # # # #
# Analysis codes
#
#
#

spread_data, diff_data = Load()

buy_months = [i for i in range(2, 6)]
Comparison_Grapher(data=spread_data[0], entries=buy_months, comparable='months')

spreads = [i/100 for i in range(110,250)]
Comparison_Grapher(data=spread_data[0], entries=spreads, comparable='spreads')

buy_cutoffs = [i/100 for i in range(60)]
Comparison_Grapher(data=spread_data[0], entries=buy_cutoffs, comparable='buys')