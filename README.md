The repository folders contain the following:

The VIX Codes folder contain two different .py files. One is for processing data extracted from the CBOE website, the other is for analysing the data for gathering insight. 

The VIX Individual Data folder contains the individual files scraped from the website trimmed to the close price and trade dates.

The VIX Processed Data folder contains the Merged.csv file which contains the master file of all individual price data files merged while respecting the trade dates. It also
contains the spread and differential data. The spread data is calculated from subtracting price data across different future contracts for the same day's close price. The differential
data then looks at the difference in prices from one day to the next for SDE modeling. 

The ultimate goal of this project is to generate a .py file which makes use of the developed codes to extract and analyze the VIX data then generate a report. However, it is currently
designed to allow the user to play with the data making use of various provided functions. 
