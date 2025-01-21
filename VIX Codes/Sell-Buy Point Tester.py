import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
file_1 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\1 Month Spreads.csv"
file_2 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\2 Month Spreads.csv"
file_3 = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data\3 Month Spreads.csv"
data_sets = []
data_sets.append(pd.read_csv(file_1))
data_sets.append(pd.read_csv(file_2))
data_sets.append(pd.read_csv(file_3))




def Spread_Strategy(data, spread, buy_point = .15):
    multiplier = 1000
    
    gains = 0
    losses = 0
    for i in range(0, len(data.iloc[0,:])):
        col = data.iloc[:,i]
        buy = col[140:145].mean()
        if buy < buy_point:
            sell = buy + spread
            if max(col[0:99]) > sell:
                gains += spread*multiplier
            else:
                if (col[0]-buy)>0:
                    gains += (col[0]-buy)*multiplier
                else:
                    losses += (col[0]-buy)*multiplier
    return gains, losses
def Spread_Grapher(data, buy_point=.15):
    gains = []
    losses = []
    profits = []
    spreads = [.1*i for i in range(40)]
    for spread in spreads:
        x, y = Spread_Strategy(data = data, spread=spread, buy_point=buy_point)
        gains.append(x)
        losses.append(-y)
        profits.append(x+y)
    return profits, gains, losses, spreads

buy_points = [0.05*i for i in range(7,8)]
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for buy in buy_points:
    for i in range(0,1):
        data = data_sets[i].iloc[:,80:]
        profits, gains, losses, spreads = Spread_Grapher(data=data, buy_point = buy)
        
        ax2.plot(spreads, profits, label=f'${np.round(buy,2)} Profits')
        ax1.plot(spreads, losses, label=f'${np.round(buy,2)} Losses')
        ax2.plot(spreads, gains, label=f'${np.round(buy,2)} Gains')
        
fig1.legend()     
fig2.legend()
plt.show()