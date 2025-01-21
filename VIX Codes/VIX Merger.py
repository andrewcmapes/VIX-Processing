import pandas as pd
import numpy as np
import os
import subprocess
import time

folder_path_in = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Individual Data"
dataframes = []
for file_name in os.listdir(folder_path_in):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path_in, file_name)
        data = pd.read_csv(file_path)
        data['Trade Date'] = pd.to_datetime(data['Trade Date'])
        dataframes.append(data)
        
merged_df = pd.concat(
    [df.set_index("Trade Date") for df in dataframes],
    axis=1).replace(0, np.nan
                    )

folder_path_out = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data"
file_path = os.path.join(folder_path_out, 'Merged.csv')
merged_df.to_csv(file_path, index=False)

