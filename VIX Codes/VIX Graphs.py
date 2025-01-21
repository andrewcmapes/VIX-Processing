import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Path to your CSV file
csv_file_path = 'C:\\Users\\andre\\spyder-env\\Projects\\Investment Algos\\VIX\\Data'
file_name = 'VIX Spreads 5 Months Out.csv'
file = os.path.join(csv_file_path, file_name)
# Read the CSV file into a DataFrame
df = pd.read_csv(file)


# Graphs
x = np.arange(0,len((df.iloc[:,1])))

for j in range(0,10):
    avg = pd.DataFrame(np.array([0.0]*len(df.iloc[:,1])))
    for k in range(0, len(df.iloc[:,1])):
            avg.iloc[k,0] = df.iloc[k,j*12:(j+1)*12].mean()
    for i in range(j*12, (j+1)*12):
        plt.plot(x, df.iloc[:,i])
    plt.plot(x, avg, color = 'black', linewidth = 3, label='Average')
    plt.axhline(y=0, color='black', linestyle='-', linewidth=2)
    plt.legend()
    plt.show()

