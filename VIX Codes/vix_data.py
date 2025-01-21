# VIX Data Management Utility Functions

import numpy as np
import pandas as pd
import requests
from datetime import datetime
import os
from io import StringIO


code_month = {
    "F": "Jan",
    "G": "Feb",
    "H": "Mar",
    "J": "Apr",
    "K": "May",
    "M": "Jun",
    "N": "Jul",
    "Q": "Aug",
    "U": "Sep",
    "V": "Oct",
    "X": "Nov",
    "Z": "Dec"
            }
month_number = {
    "Jan": "01",
    "Feb": "02",
    "Mar": "03",
    "Apr": "04",
    "May": "05",
    "Jun": "06",
    "Jul": "07",
    "Aug": "08",
    "Sep": "09",
    "Oct": "10",
    "Nov": "11",
    "Dec": "12"
            }
number_code = {
    "01": "F",
    "02": "G",
    "03": "H",
    "04": "J",
    "05": "K",
    "06": "M",
    "07": "N",
    "08": "Q",
    "09": "U",
    "10": "V",
    "11": "X",
    "12": "Z"
    }


def Retriever(month: int, year: int, folder_out=r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Individual Data") -> None:
    """
    Retriever function communicates with the CBOE database to gather specific 
    VIX futures contracts data. The function extracts the daily high pricing
    and saves it as a .csv file.

    Parameters
    ----------
    month : int
        The parameter should be a 1-2 digit integer
    year : int
        The parameter should be a 2 or 4 digit integer
    folder_out : str
        The folder_out parameter sets the file destination for the .csv files gathered by the function.
        The default is r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Individual Data".

    """
    folder_out = folder_out
    base_url = 'https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/'
    
    # Converts dates to uniform format
    year = f'{str(year)[-2:]:02}'
    month = f'{month:02}'
    
    # Generating file format to match the monthly vix contract while ignoring weekly contracts by
    # checking the 15th-22nd date contracts
    output_files = [f"VX_20{year}-{month}-{day}.csv" for day in range(15, 23)]
    urls = [f"{base_url}{output_file}" for output_file in output_files]
        
    for url in urls: # Loops through all requested files in search of matching file from database
        try:
            response = requests.get(url)
            if response.status_code == 200: # Successful collection of data
                try:
                    data = pd.read_csv(StringIO(response.text)).replace(0, np.nan) # Reading data and eliminating zero entries
                    if len(data.iloc[:,0])>60:
                        # Next lines select desired columns while renaming pricing with contract name for merged files
                        table = data[['Trade Date', 'Close']].copy()
                        table.rename(columns={'Close':f'M:{month} Y:{year}'}, inplace=True)
                        
                        output_file = f'VX_{year}_{month}.csv'
                        file_path = os.path.join(folder_out, output_file)
                        table.to_csv(file_path, index=False)
                        print(f"Converted {output_file}")
                        break
    
                except Exception as e:
                    print(f"Failed to process data for {output_file}: {e}")
    
        except Exception as e:
            print(f"Error fetching data for {output_file}: {e}")         
            
            
def Merger() -> None:
    """
    Merger function compiles individual VIX Futures contract data and matches their
    dates to generate a single merged .csv file with correct indexing.

    """
    folder_in = r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Individual Data"
    folder_out = r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Processed Data"
    output_file = 'Merged.csv'
    
    dataframes = []
    for input_file in os.listdir(folder_in):
        if input_file.endswith('.csv'):
            data = pd.read_csv(os.path.join(folder_in, input_file))
            data['Trade Date'] = pd.to_datetime(data['Trade Date'])
            dataframes.append(data)
    
    # Generating merged DataFrame with Trade Date as index 
    table = pd.concat([data.set_index("Trade Date") for data in dataframes], axis=1)
    file_path = os.path.join(folder_out, output_file)
    table.to_csv(file_path, index=False)
    print(f'Successfully saved {output_file}')


def Update(full=False):
    """
    Update function is used to update the current folders of VIX Individual Data
    contracts. It calls on the retriever function and cycles through different 
    date ranges depending on its parameter.

    Parameters
    ----------
    full : TYPE, bool
        This parameter determines if the entire database of VIX 
        contracts should be updated through present. Default is set to false 
        which results in only current and next years contracts being updated.

    """
    date = datetime.now().date()
    if full == True: # Updating all VIX contracts from the start
        years = range(2013, date.year+2)
        months = range(1, 13)
    else: # Updates recent and new contract months
        years = range(date.year, date.year+2)
        months = range(1, 13)

    for year in years:
        for month in months:
            Retriever(month, year)
    Merger() # Updates merged.csv file as well


def Spreads(mo_spread=1, differential=True, save=True):
    """
    Spreads function obtains the VIX spread data from the separate price data
    of each months contracts. This obtains pricing information for volatility
    spread trading.

    Parameters
    ----------
    mo_spread : TYPE, int
        DESCRIPTION. Determines the number of months between spreads.
    differential : TYPE, bool
        DESCRIPTION. Generates daily price movement of spreads.
    save : TYPE, bool
        DESCRIPTION. Determines if data should be saved to .csv.

    Returns
    -------
    TYPE
        DESCRIPTION. Returns table of spread and differential data for use.

    """
    folder_in = r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Processed Data"
    folder_out = r"C:\\Users\\andre\\spyder-env\\Projects\\VIX\\VIX Processed Data"
    input_file = 'Merged.csv'
    data = pd.read_csv(os.path.join(folder_in, input_file))


    # Subtracts price data between contract months to obtain price spread.
    spreads = []
    for i in range(4, len(data.iloc[0,:])-9):
        spread = (data.iloc[:,i+mo_spread]-data.iloc[:,i]).dropna().reset_index(drop=True)
        
        # Data is reversed to create uniformness in respect to front contract
        # expiration for index value of 0. Length of data used is shortened for
        # greater month spreads.
        spreads.append(spread[::-1].reset_index(drop=True)[:(22*(8-mo_spread))])
    table = pd.concat(spreads,axis=1).reset_index(drop=True)
    
    if save == True:
        output_file = f'{mo_spread} Month Spreads.csv'
        table.to_csv(os.path.join(folder_out, output_file), index=False)
        print(f'Successfully saved {output_file}')
    
    if differential == True:
        # Daily price differentials are calculated from subtracting one days
        # price values from the next.
        differentials = []
        for i in range(len(table.iloc[:,0])-1):
            differential = table.iloc[i,:] - table.iloc[i+1,:]
            differentials.append(differential)
        table2 = pd.DataFrame(differentials).round(2) # Eliminating machine error in values
        output_file = f'{mo_spread} Month Differentials.csv'
        table2.to_csv(os.path.join(folder_out, output_file), index=False)
        print(f'Successfully saved {output_file}')
        return table, table2
    
    return table





