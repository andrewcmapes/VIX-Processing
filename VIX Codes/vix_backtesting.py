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
        col = data.iloc[:,i] # col represents the spread being evaluated
        buy = col[buy_month*21] # specifying the buy price paid
        if buy < buy_cutoff: # determines if the contract is purchased or not
            sell = buy + spread # determines the specific sell point for early transaction
            if max(col[0:buy_month*21]) > sell:
                gains.append((spread * multiplier - fees) * quantity)
            else: # handles if the specific sale price is not reached and contract is held to maturity
                if (col[0]-buy)>0:
                    gains.append(((col[0] - buy) * multiplier - fees) * quantity)
                else:
                    losses.append(((col[0] - buy) * multiplier - fees) * quantity)
    return gains, losses


def Spread_Comparison(data, buy_cutoff=.3, buy_month=5, spreads: list=[.75]):
    """
    Spread_Comparison is designed to aid in evaluating the effectiveness of different sell points
    determined by the buy price and the spread. The spread value determines how much the value needs
    to increase from the buy point for the contract to be sold early. 

    Parameters
    ----------
    data : TYPE DataFrame
        DESCRIPTION. 
    buy_cutoff : float, optional
        DESCRIPTION. The default cutoff that will be uniformly used with all spreads. The default is .3.
    buy_month : int, optional
        DESCRIPTION. The default timeframe used for contract purchase. The default is 5.
    spreads : list, optional
        DESCRIPTION. The spreads should be a list of different spread values to be compared. The default 
        is [.75].

    Returns
    -------
    profits : float
        DESCRIPTION. The profits value represents the gains minus the losses thus giving the total proceeds.
    gains : float
        DESCRIPTION. The gains from all successful trades aggregated together.
    losses : float
        DESCRIPTION. The losses from all the unsuccessful trades aggregated together. 

    """
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
    """
    The Buy_Cutoff_Comparison function is used to compare different buy point cutoffs to identify efficient
    values in comparing profit vs exposure.

    Parameters
    ----------
    data : TYPE DataFrame
        DESCRIPTION. 
    buy_cutoff : list, optional
        DESCRIPTION. The list of cutoff values that will be compared. The default is [.3].
    buy_month : int, optional
        DESCRIPTION. The default timeframe used for contract purchase. The default is 5.
    spreads : float, optional
        DESCRIPTION. The default spread that will be uniformly used with all buy point cutoffs. The default 
        is .75.

    Returns
    -------
    profits : float
        DESCRIPTION. The profits value represents the gains minus the losses thus giving the total proceeds.
    gains : float
        DESCRIPTION. The gains from all successful trades aggregated together.
    losses : float
        DESCRIPTION. The losses from all the unsuccessful trades aggregated together. 

    """
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
    """
    The Buy_Month_Comparison function is used to compare different purchase periods to identify efficient
    practices in comparing profit vs exposure.

    Parameters
    ----------
    data : TYPE DataFrame
        DESCRIPTION. 
    buy_cutoff : float, optional
        DESCRIPTION. The default buy point cutoff used for contract purchase. The default is .3.
    buy_month : list, optional
        DESCRIPTION. The list of timeframes used for comparison of purchase periods. The default is [5].
    spreads : float, optional
        DESCRIPTION. The default spread that will be uniformly used with all buy point cutoffs. The default 
        is .75.

    Returns
    -------
    profits : float
        DESCRIPTION. The profits value represents the gains minus the losses thus giving the total proceeds.
    gains : float
        DESCRIPTION. The gains from all successful trades aggregated together.
    losses : float
        DESCRIPTION. The losses from all the unsuccessful trades aggregated together. 

    """
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
    """
    The Comparison_Grapher function is used to produce graphs of the comparisons of buy_points, spreads, or purchase months.
    It calls on the specific functions for comparison defined above. Then using the results produces plots to better visualize
    this information. 

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    entries : list
        DESCRIPTION. The list of values for the input being compared.
    comparable : str, optional
        DESCRIPTION. The value of comparable determines which input element we are comparing. Values used are 'spreads', 'months',
        and 'buys'. The default is 'spreads'.
    spread : float, optional
        DESCRIPTION. The default is .75.
    buy_cutoff : float, optional
        DESCRIPTION. The default is .3.
    buy_month : int, optional
        DESCRIPTION. The default is 5.

    Returns
    -------
    None
        DESCRIPTION. Only plots are provided by this function.

    """
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx() # provides right side axis for losses
    ax1.yaxis.set_major_formatter(ff(dollar_format)) # provides formatting for the 2 y axes
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
# Sample analysis codes
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