import numpy as np
from vix_backtesting import load
import scipy.stats as sps

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




# In progress, want to test daily % changes for gaussian behavior



spread_data, diff_data = load()
data = spread_data[0]
percentage_changes = []
for i in range(len(data.iloc[0,:])):
    per_diffs = []
    for j in range(len(data.iloc[:,0])):
        value = (data.iloc[j+1,i]-data.iloc[j,i])/data.iloc[j,i]
        per_diffs.append(value)
        pass



for i in range(len(data.iloc[:,0])):
    Anderson_Darling(data.iloc[i,:])

