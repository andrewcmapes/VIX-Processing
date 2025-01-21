import pandas as pd
import numpy as np
import os
import subprocess
import time

# Run Matlab to collect data
directory_path = 'C:\\Users\\andre\\spyder-env\\Projects\\Investment Algos\\VIX\\Individual CSV'
file_name = 'MatToCSV.m'
matlab_script_path = os.path.join(directory_path, file_name)
matlab_executable_path = r'C:\Program Files\MATLAB\R2023b\bin\matlab.exe' 
command = [matlab_executable_path, '-r', f"run('{matlab_script_path}'); exit;"]
process = subprocess.Popen(command)
process.wait()
time.sleep(16*60)
print('Data extracted')

# Deleting small files
folder_path = 'C:\\Users\\andre\\spyder-env\\Projects\\Investment Algos\\VIX\\Individual CSV'
files = os.listdir(folder_path)
for file in files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        file_size = os.path.getsize(file_path)
        if file_size < 13000:  
            os.remove(file_path)  
print('Small Files Deleted')

# Deleting extra columns
def DelExtraColumns(folder_path, columns_to_keep):
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)
            df = df[columns_to_keep]
            new_file_name = os.path.splitext(file)[0] + '.csv'
            new_file_path = os.path.join(folder_path, new_file_name)
            df.to_csv(new_file_path, index=False)
columns_to_keep = ['TradeDate', 'Settle']
DelExtraColumns(folder_path, columns_to_keep)
print('Extra Columns deleted')

# Dates need to be uniform in format
files = os.listdir(folder_path)
for file in files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        if not df.empty:
            first_column = df.columns[0]
            try:
                df[first_column] = pd.to_datetime(df[first_column])
                df[first_column] = df[first_column].dt.strftime('%A, %B %d, %Y')
                df.to_csv(file_path, index=False)
            except ValueError:
                a=1
files = os.listdir(folder_path)
for file in files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        if not df.empty:
            first_column = df.columns[0]
            try:
                df[first_column] = pd.to_datetime(df[first_column], format='%d-%b-%Y')
                df[first_column] = df[first_column].dt.strftime('%A, %B %d, %Y')
                df.to_csv(file_path, index=False)
            except ValueError as e:
                a=1
print("Dates are uniform")

# Combining csv files to one
dfs = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        dfs.append(df)
combined_df = pd.concat(dfs, axis=1, join='outer')
print('CSVs combined')
folder_path2 = 'C:\\Users\\andre\\spyder-env\\Projects\\Investment Algos\\VIX\\Data' 
file_name2 = 'Vix_combined_data.csv'
combined_df.to_csv(f'{folder_path2}/{file_name2}', index=False)
# Obtaining Differentials
data = combined_df
dif = np.full((len(data.iloc[:,1]), len(data.iloc[1,:])), np.nan)
dif = pd.DataFrame(dif)
for c in range(0,(len(data.iloc[1,:])-1)):
    k=0
    for r in range(1, len(data.iloc[:,1])):
        if str(data.iloc[r,c+1]) == str(data.iloc[1,20]):
            k=k
        else:
            dif.iloc[k,c] = data.iloc[r,c+1]-data.iloc[r,c]
            k = k+1

# Reducing to usable data
reduced = dif.iloc[2:250,:]
new = pd.DataFrame(np.full((155,121), np.nan))

# Orienting rows to go from last trading days to 
for c in range (0, len(new.iloc[1,:])):
    k=1
    r=1
    while k<154:
        if str(reduced.iloc[-r,c]) == str(data.iloc[1,20]):
            r += 1
        else:
            new.iloc[-k,c] = reduced.iloc[-r,c]
            k += 1
            r += 1
print(new)           
VIX_Spreads = new.iloc[2:,:]
folder_path = 'C:\\Users\\andre\\spyder-env\\Projects\\Investment Algos\\VIX\\Data' 
file_name = 'VIX Spreads 5 Months Out.csv'
VIX_Spreads.to_csv(f'{folder_path}/{file_name}', index=False)
print('Successfully processed data')
