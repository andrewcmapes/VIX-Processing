import os
import requests
import pandas as pd
from io import StringIO
from datetime import datetime

# Base URL for the data
base_url = 'https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/'

# Define the range of years and months
years = range(2014, 2025)
months = range(1, 13)
days = range(1, 32)

# Create output directory if not exists
output_dir = os.getcwd()

for year in years:
    for month in months:
        for day in days:
            try:
                # Format month and day to ensure two digits
                m = f"{month:02d}"
                d = f"{day:02d}"

                # Construct filename and URL
                filename = f"VX_{year}-{m}-{d}.csv"
                url = f"{base_url}{filename}"
                
                # Make request to URL
                response = requests.get(url)
                
                # Check if the request was successful
                if response.status_code == 200:
                    # Convert response text to a pandas DataFrame
                    try:
                        data = pd.read_csv(StringIO(response.text))
                        
                        # Generate the output CSV filename
                        output_file = os.path.join(output_dir, filename)

                        # Save DataFrame to a CSV file
                        data.to_csv(output_file, index=False)
                        print(f"Converted {filename}")

                    except Exception as e:
                        print(f"Failed to process data for {filename}: {e}")

            except Exception as e:
                print(f"Error fetching data for {year}-{m}-{d}: {e}")
