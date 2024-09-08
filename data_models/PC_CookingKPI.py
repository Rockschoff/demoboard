import streamlit as st
from data_models.app_state import KPIModel , KPIDataModel
import pandas as pd
from typing import Optional , List
from pydantic import BaseModel
from api.data_api import generate_customer_complaints , generate_real_time_temp , get_product_type_data, get_yield_data
import altair as alt




class PC_CookingKPIDataModel(KPIDataModel):


    temperature : Optional[pd.DataFrame] = None
    product_type : Optional[pd.DataFrame] = None
    customer_complaints : Optional[pd.DataFrame] = None
    yield_data : Optional[pd.DataFrame] = None

    correlation_graphs : Optional[List[str]] = ["Complaints vs Temperatures", "Yield vs Temperature"]

    def load_data(self):
        # Create a demo DataFrame with sample cooking KPI data
        self.temperature = generate_real_time_temp()
        self.product_type=get_product_type_data()
        self.customer_complaints=generate_customer_complaints(self.temperature)
        self.yield_data=get_yield_data(self.temperature)

        # self.compute_derived_data()


        return True
    
    def get_corr_chart(self , corr_chart_name)->alt.Chart:
        match corr_chart_name:
            case "Complaints vs Temperatures":
                # Resample the temperature data (as you already have)
                # print("Tank" , self.temperature)
                self.temperature['Timestamp'] = pd.to_datetime(self.temperature['Timestamp'])
                resampled = self.temperature.set_index("Timestamp")["Temperature"].resample("1D").mean().reset_index()
                # print("Dank", len(resampled) , resampled)
                # Group by the 'Timestamp' column and sum the 'Complaints_Count' column
                cc = self.customer_complaints.groupby('Timestamp')['Complaints_Count'].sum().reset_index()

                
                # Remove the time component from the `Timestamp` column in `self.customer_complaints` to match the resampled data
                cc['Timestamp'] = pd.to_datetime(cc['Timestamp']).dt.date
                print("Fank" , cc)
                # Also convert the `Timestamp` in the `resampled` data to just the date
                resampled['Timestamp'] = pd.to_datetime(resampled['Timestamp']).dt.date

                # Merge the resampled temperature data with the customer complaints
                merged = pd.merge(cc, resampled, on="Timestamp", how="left")
                merged.rename(columns={"Temperature" : "Avg_Temp"} , inplace=True)
                print(merged)
                corr_data = merged

                # Create a scatter plot to show the correlation between Complaints_Count and Temperature
                chart = alt.Chart(corr_data).mark_point().encode(
                    x=alt.X('Avg_Temp', scale=alt.Scale(domain=[corr_data['Avg_Temp'].min(), corr_data['Avg_Temp'].max()])),
                    y='Complaints_Count',
                    tooltip=['Avg_Temp', 'Complaints_Count']  # Adds tooltips with the values
                ).properties(
                    title='Correlation between Temperature and Complaints Count',
                    width=600,
                    height=400
                )

                ans = chart

            case "Yield vs Temperature":

                # Step 1: Resample the temperature data to 10-minute intervals
                # Assuming the 'timestamp' column in self.temperature is already a DateTime object
                self.temperature['Timestamp'] = pd.to_datetime(self.temperature['Timestamp'])



                # Resample to 10-minute intervals and take the mean of temperature for each line_id
                resampled_temp = self.temperature.set_index('Timestamp').groupby('Line_ID').resample('10T').mean().drop(columns=["Line_ID"])

                # Step 3: Print the resampled data to debug
                # print(resampled_temp)
                # # Step 2: Ensure 'timestamp' in yield_data is also a DateTime object
                self.yield_data['Timestamp'] = pd.to_datetime(self.yield_data['Timestamp'])
                resampled_yield = self.yield_data.set_index("Timestamp").groupby('Line_ID').resample('10T').mean().drop(columns=["Line_ID"])
                # print(resampled_yield)
                # # Step 3: Merge the resampled temperature data with the yield data on 'timestamp' and 'line_id'
                merged_data = pd.merge(resampled_yield, resampled_temp, on=['Timestamp', 'Line_ID'], how='left')
                # print(merged_data)
                # # Rename the columns for clarity
                merged_data.rename(columns={'Temperature': 'Avg_Temp'}, inplace=True)
                

                merged_data = merged_data.reset_index(level="Line_ID")
                merged_data = merged_data.resample("W").mean()
                # print(merged_data)

                corr_data=merged_data

                chart = alt.Chart(corr_data).mark_point().encode(
                    x = alt.X('Avg_Temp', scale=alt.Scale(domain=[corr_data['Avg_Temp'].min(), corr_data['Avg_Temp'].max()])),
                    y = alt.Y('Yield', scale=alt.Scale(domain=[corr_data['Yield'].min()-2, corr_data['Yield'].max()+2])),
                    tooltip=["Avg_Temp" , "Yield" , "Line_ID"]
                ).properties(
                    title='Correlation between Temperature and Yield',
                    width=600,
                    height=400
                )

                ans=chart

            case _ :
                ans=alt.Chart(pd.DataFrame({"x":[1,2,3] , "y":[1,2,3]}))
                   
        return ans
    

class PC_CookingKPIModel(KPIModel):

    main_chart : Optional[any] = None

    def get_info(self , duration="1D"):
        main_chart_info= {
                "line_1": {
                    "crossing_upper_threshold": {
                        "value": 20,
                        "description": "number of times the upper threshold of the baking process was crossed in the last 3 days",
                        "significance": "This is a quality issue and is worthy of being noted. The process must be regulated, and the issue addressed according to FDA LAW."
                    },
                    "crossing_lower_threshold": {
                        "value": 0,
                        "description": "number of times the lower threshold of the baking process was crossed in the last 3 days",
                        "significance": "No critical issue detected, as the lower threshold was not crossed. Normal operation can continue."
                    },
                    "average_temperature": {
                        "value": 175,
                        "description": "the average temperature of the baking line in the past 3 days in Celsius",
                        "significance": "This is a normal reading. The ideal temperature is around 174 Celsius, so it is close to the expected range."
                    }
                },
                "line_2": {
                    "crossing_upper_threshold": {
                        "value": 20,
                        "description": "number of times the upper threshold of the baking process was crossed in the last 3 days",
                        "significance": "This is a quality issue and is worthy of being noted. The process must be regulated, and the issue addressed according to FDA LAW."
                    },
                    "crossing_lower_threshold": {
                        "value": 0,
                        "description": "number of times the lower threshold of the baking process was crossed in the last 3 days",
                        "significance": "No critical issue detected, as the lower threshold was not crossed. Normal operation can continue."
                    },
                    "average_temperature": {
                        "value": 175,
                        "description": "the average temperature of the baking line in the past 3 days in Celsius",
                        "significance": "This is a normal reading. The ideal temperature is around 174 Celsius, so it is close to the expected range."
                    }
                },
                "line_3": {
                    "crossing_upper_threshold": {
                        "value": 20,
                        "description": "number of times the upper threshold of the baking process was crossed in the last 3 days",
                        "significance": "This is a quality issue and is worthy of being noted. The process must be regulated, and the issue addressed according to FDA LAW."
                    },
                    "crossing_lower_threshold": {
                        "value": 20,
                        "description": "number of times the lower threshold of the baking process was crossed in the last 3 days",
                        "significance": "This is a HYPER CRITICAL ISSUE. This must be reported to everyone, and a procedure for a recall must be investigated as per requirements."
                    },
                    "average_temperature": {
                        "value": 175,
                        "description": "the average temperature of the baking line in the past 3 days in Celsius",
                        "significance": "This is just a good-to-know metric. The ideal calculation is about 174 Celsius."
                    }
                }
            }
        
        corr_chart_info = {
            "Complaints vs Temperatures" : {
                "insight" : "The range of 173.5 degree Celcius and 174.5 degree celcius of weekly average oven temperature have the lowest average product complaints "
            },
            "Yield vs Temperature" : {
                "insight" : "The range of 173.5 degree Celcius and 174.5 degree celcius of weekly average oven temperature have the highest average yeild"
            }

        }
        
        return {
            "Main_Chart" : main_chart_info,
            "Correlation_Chart" : corr_chart_info
        }

    
    def render(self):

        self.data.load_data()
        # st.write(f"Rendering this {self.name}")
        # st.table(self.data.product_type)


        max_date = self.data.temperature['Timestamp'].max()
        start_date = max_date - pd.Timedelta(hours=1)

        main_charts : List[alt.Chart] = self.create_main_chart(start_date, max_date)
        # st.altair_chart(main_chart , use_container_width=True)
        cols = st.columns([1 for chart in main_charts])
        for i in range(len(cols)):
            with cols[i]:
                
                if main_charts[i]["alert"]:
                    st.error("Emergency")
                elif main_charts[i]["warning"]:
                    st.warning("Warning")
                else:
                    st.success("Under Control")
                st.altair_chart(main_charts[i]["chart"] , use_container_width=True)


        if st.checkbox("View Correlations"):
            selectbox = st.selectbox( "Choose a graph", options=self.data.correlation_graphs)
            corr_chart : alt.Chart = self.data.get_corr_chart(selectbox)
            st.altair_chart(corr_chart)

    
        
        

    def create_main_chart(self, start_timestamp, end_timestamp) -> alt.Chart:
        # Filter the temperature data within the given start and end timestamp
        temperature_data = self.data.temperature
        filtered_data = temperature_data[
            (temperature_data['Timestamp'] >= start_timestamp) & 
            (temperature_data['Timestamp'] <= end_timestamp)
        ]
        
        # Define a base chart for reuse with line-specific filtering
        def create_line_chart(line_id, lower_threshold=170, upper_threshold=180, look_back='15T'):
            # Filter the data for the given line_id
            line_data = filtered_data[filtered_data['Line_ID'] == line_id]
            
            # Ensure 'Timestamp' is datetime to enable rolling
            line_data['Timestamp'] = pd.to_datetime(line_data['Timestamp'])

            # Set 'Timestamp' as the index for rolling calculation
            line_data = line_data.set_index('Timestamp')

            # Calculate rolling average for the Temperature column
            rolling_window = pd.to_timedelta(look_back).total_seconds() / 60
            line_data['Rolling_Avg'] = line_data['Temperature'].rolling(f'{int(rolling_window)}T').mean()

            # Reset index for plotting
            line_data = line_data.reset_index()

            # Create the base line chart for Temperature
            line_chart = alt.Chart(line_data).mark_line().encode(
                x='Timestamp:T',
                y=alt.Y('Temperature:Q', scale=alt.Scale(domain=[155, line_data['Temperature'].max() + 10])),
                tooltip=['Timestamp:T', 'Temperature:Q']
            ).properties(
                title=f'Line {line_id} Temperature',
                width="container",
            )

            # Create the rolling average chart
            rolling_avg_chart = alt.Chart(line_data).mark_line(color='blue').encode(
                x='Timestamp:T',
                y=alt.Y('Rolling_Avg:Q'),
                tooltip=['Timestamp:T', 'Rolling_Avg:Q']
            ).properties(
                title=f'Line {line_id} Rolling Avg Temperature (Look-back: {look_back})',
            )
            
            # Create rule for lower threshold with dashed line
            lower_threshold_rule = alt.Chart(pd.DataFrame({'y': [lower_threshold]})).mark_rule(
                color='red', strokeDash=[5, 5]  # Dashed line pattern
            ).encode(
                y='y:Q'
            )
            
            # Create rule for upper threshold with dashed line
            upper_threshold_rule = alt.Chart(pd.DataFrame({'y': [upper_threshold]})).mark_rule(
                color='red', strokeDash=[5, 5]  # Dashed line pattern
            ).encode(
                y='y:Q'
            )

            # Combine the line chart, rolling average, and threshold lines
            combined_chart = alt.layer(line_chart, rolling_avg_chart, lower_threshold_rule, upper_threshold_rule)

            return combined_chart
                    
        # Create charts for each line (Line_ID 1, 2, and 3)
        chart_line1 = create_line_chart(1)
        chart_line2 = create_line_chart(2)
        chart_line3 = create_line_chart(3)
        
        # Display the charts side by side
        # combined_chart = alt.hconcat(chart_line1, chart_line2, chart_line3).resolve_scale(y='shared')
        
        return [{"chart" : chart_line1 , "warning" : ["qualty issues"], "alert":[]},
                {"chart" : chart_line2 , "warning" : [], "alert":[]},
                {"chart" : chart_line3 , "warning" : [], "alert":["critical emerguncy"]}]