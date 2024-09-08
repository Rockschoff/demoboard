import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@st.cache_data
def generate_real_time_temp()->pd.DataFrame:
    # Define start and end time range for each day
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) - timedelta(weeks=20)
    end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0) - timedelta(days=1)

    time_range = pd.date_range(start=start_time, end=end_time, freq='2T')
    # Filter the time range to only include times between 6 AM and 6 PM
    time_range = time_range[time_range.indexer_between_time('06:00', '18:00')]

    # Generate base temperatures with a slight upward trend
    base_temps = np.linspace(170, 178, num=len(time_range))
    
    # Add some random fluctuations
    temperature_data_line1 = base_temps + np.random.normal(0, 5, size=len(time_range))
    temperature_data_line2 = base_temps + np.random.normal(-4, 1, size=len(time_range))
    temperature_data_line3 = base_temps + np.random.normal(0, 1, size=len(time_range))

    # Prepare the data: repeat each timestamp 3 times, one for each line
    repeated_time_range = np.repeat(time_range, 3)
    line_ids = np.tile([1, 2, 3], len(time_range))
    temperatures = np.concatenate([temperature_data_line1, temperature_data_line2, temperature_data_line3])

    
    # Create the final DataFrame
    temperature_df = pd.DataFrame({
        'Timestamp': repeated_time_range,
        'Line_ID': line_ids,
        'Temperature': temperatures
    })

    # Adjust Line 1: Randomly pick 4 values each day and shoot them to a random temp between 180 and 183
    for date in pd.date_range(start=start_time, end=end_time, freq='D'):
        daily_line1_idx = temperature_df[(temperature_df['Line_ID'] == 1) & (temperature_df['Timestamp'].dt.date == date.date())].index
        if len(daily_line1_idx) > 4:
            random_idx = np.random.choice(daily_line1_idx, size=4, replace=False)
            temperature_df.loc[random_idx, 'Temperature'] = np.random.uniform(180, 183, size=4)

    # Line 2 temperatures remain as is (no changes needed)

    # Adjust Line 3: Only the last 7 values drop to a random value between 155 and 160
    for date in pd.date_range(start=start_time, end=end_time, freq='D'):
        daily_line3_idx = temperature_df[(temperature_df['Line_ID'] == 3) & (temperature_df['Timestamp'].dt.date == date.date())].index
        if len(daily_line3_idx) >= 7:
            last_7_idx = daily_line3_idx[-7:]
            temperature_df.loc[last_7_idx, 'Temperature'] = np.random.uniform(155, 160, size=7)
    temperature_df["Timestamp"]=pd.to_datetime(temperature_df["Timestamp"])
    print( "WwWwwwwwwwwwwwwwww",temperature_df)
    return temperature_df


@st.cache_data
def get_product_type_data()->pd.DataFrame:

    product_type_df = pd.DataFrame({
        "Product_type" : ["Product_1" , "Product_2" , "Product_3"],
        "Line" :[[1 , 2] , [2 , 3] , [3]] 
    })
    return product_type_df


@st.cache_data
def generate_customer_complaints(temp_df: pd.DataFrame) -> pd.DataFrame:
    start_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) - timedelta(weeks=52)
    end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0) - timedelta(days=1)
    time_range = pd.date_range(start=start_time, end=end_time, freq='1W')
    
    # Resample temp_df to weekly frequency
    weekly_temps = temp_df.set_index('Timestamp').resample('W')['Temperature'].mean()
    
    complaints = []
    for week in time_range:
        # Find the closest week in weekly_temps
        closest_week = weekly_temps.index[np.abs(weekly_temps.index - week).argmin()]
        avg_temp = weekly_temps[closest_week]
        
        if avg_temp < 172 or avg_temp > 176:
            complaints.extend(np.random.choice([0, 1, 2], size=3, p=[0.5, 0.3, 0.2]))
        else:
            complaints.extend(np.random.choice([0, 1, 2], size=3, p=[0.8, 0.15, 0.05]))
    
    repeated_time_range = np.repeat(time_range, 3)
    product_ids = np.tile(["Product_1", "Product_2", "Product_3"], len(time_range))
    
    # Ensure all arrays have the same length
    min_length = min(len(repeated_time_range), len(product_ids), len(complaints))
    
    ans = pd.DataFrame({
        "Timestamp": repeated_time_range[:min_length],
        "Product": product_ids[:min_length],
        'Complaints_Count': complaints[:min_length]
    })
    
    # print("MIN", min_length)
    # print("ANSWER", ans)
    
    return ans


@st.cache_data
def get_yield_data(temp_df: pd.DataFrame) -> pd.DataFrame:
    # Resample temperature data to 10-minute intervals
    # print(temp_df)
    resampled_temp = temp_df.set_index('Timestamp').groupby('Line_ID').resample('10T').mean().drop(columns=["Line_ID"]).reset_index()
    # print(resampled_temp)
    def temp_to_yield(temp):
        # Optimal temperature range: 173-175
        if 173 <= temp <= 175:
            return np.random.randint(130, 151)  # High yield
        elif 171 <= temp < 173 or 175 < temp <= 177:
            return np.random.randint(90, 131)   # Medium yield
        else:
            return np.random.randint(50, 91)    # Low yield

    # Calculate yield based on temperature
    resampled_temp['Yield'] = resampled_temp['Temperature'].apply(temp_to_yield)
    
    # Ensure the  DataFrame has the same structure as the original function
    result_df = resampled_temp.rename(columns={'level_1': 'Timestamp'})
    result_df = result_df[['Timestamp', 'Line_ID', 'Yield']]

    return result_df







        

        

        


"""
time
line_id
temp
"""

"""
product_type
line_id
"""

"""
time
customer_complaints_count
product_type
"""

"""
time
line_id
yield
"""


