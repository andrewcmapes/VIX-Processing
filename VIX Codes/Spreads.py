import os
import pandas as pd
folder = r"C:\Users\andre\spyder-env\Projects\VIX\VIX Processed Data"
input_file = 'Merged.csv'
data = pd.read_csv(os.path.join(folder, input_file))

for j in range(1, 4):
    spreads = []
    for i in range(0, len(data.iloc[0,:])-10):
        spread = (data.iloc[:,i+j]-data.iloc[:,i]).dropna().reset_index(drop=True)
        spreads.append(spread[::-1].reset_index(drop=True)[:(21*(8-j))])
    
    table = pd.concat(spreads,axis=1).reset_index(drop=True)
    output_file = f'{j} Month Spreads.csv'
    table.to_csv(os.path.join(folder, output_file), index=False)
    print(f'Successfully saved {output_file}')