import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data
from app_data.app_data import app

st.set_page_config(layout="wide")
st.header("InnovaQ")

if "app" not in st.session_state:
    st.session_state.app = app




# Generate random coordinates and past scores
np.random.seed(42)
data_points = pd.DataFrame({
    'latitude': np.random.uniform(30, 48, 5),  # Latitude range for USA
    'longitude': np.random.uniform(-125, -70, 5),  # Longitude range for USA
    'past_score': np.random.randint(50, 100, 5),
    'current_score': np.random.randint(50, 100, 5),
    'future_score': np.random.randint(50, 100, 5)  # Random past scores between 50 and 100
})

# Load US states data
states = alt.topo_feature(data.us_10m.url, 'states')

# Create selection for points
selection = alt.selection_single(fields=['longitude', 'latitude'], on='click')

# Create base map with darker colors
base = alt.Chart(states).mark_geoshape(
    fill='black',  # Dark fill for map
    stroke='gray'  # Light gray for state borders
).project('albersUsa').properties(
)

# Create points with selection
points = alt.Chart(data_points).mark_circle(size=100).encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    tooltip=[ 'past_score:Q' , 'current_score:Q' , 'future_score:Q'],
    color=alt.condition(selection, alt.value('lightblue'), alt.value('gray'))  # Highlight selected point
).add_selection(
    selection  # Add click selection
)

# Combine base map and points
chart = (base + points).properties(
    title='Your Plants',
    background='#0E1117',  # Dark background for the chart
    padding={'left': 20, 'right': 20, 'top': 20, 'bottom': 20}
)

# Render the chart in Streamlit
with st.expander("Summary of you plants"):
    st.altair_chart(chart , use_container_width=True)


st.session_state.app.render()
