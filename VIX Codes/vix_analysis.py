import numpy as np
from vix_backtesting import load
import scipy.stats as sps
import pandas as pd
from statsmodels.tsa.stattools import kpss

spread_data, diff_data = load()
data = spread_data[0]

# # # # #
# Goal: Testing for Gaussianity
# Conclusion: Non-Gaussian 
#
#

def Anderson_Darling(data):
    result = sps.anderson(data, dist='norm')
    print("Anderson-Darling Statistic:", result.statistic)
    print("Critical Values:", result.critical_values)
    print("Significance Levels:", result.significance_level)
    for i in range(len(result.critical_values)):
        sig_level = result.significance_level[i]
        crit_value = result.critical_values[i]
        if result.statistic > crit_value:
            print(f"At {sig_level}% significance level: Reject normality (not Gaussian)")
        else:
            print(f"At {sig_level}% significance level: Fail to reject normality (likely Gaussian)")

def percentage_changes(data):
    percentage_changes = []
    for i in range(len(data.iloc[0,:])):
        per_diffs = []
        for j in range(len(data.iloc[:,0])-1):
            value = (data.iloc[j+1,i]-data.iloc[j,i])/abs(data.iloc[j,i])
            per_diffs.append(value)
        percentage_changes.append(per_diffs)
    percentage_changes = pd.DataFrame(percentage_changes).fillna(0)
    percentage_changes.replace([np.inf, -np.inf], 0, inplace=True)
    return percentage_changes.T

def gaussianity_checker(data, check='rows'):
    if check=='rows':
        for i in range(len(percentage_changes.iloc[:,0])):
            Anderson_Darling(percentage_changes.iloc[i,:])
    if check=='columns':
        for i in range(len(percentage_changes.iloc[0,:])):
            Anderson_Darling(percentage_changes.iloc[:,i])



# # # # #
# Testing Stationarity in percentage changes
#
#
#
def stationarity_checker(data, check='rows'):
    if check=='rows':
        for i in range(len(data.iloc[:,0])):
            kpss(data.iloc[i,:])
    if check=='columns':
        for i in range(len(data.iloc[0,:])):
            kpss(data.iloc[:,i])


per_data = percentage_changes(data)



# # # # #
# Attempt modeling via ARIMA
#
#
#





# # # # #
# attempt modeling via GARCH
#
#
#





# # # # #
# attempt modeling via PCA
#
#
#




