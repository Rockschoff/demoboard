import streamlit as st
from app_data.app_data import app

st.set_page_config(layout="wide")
st.header("InnovaQ")

if "app" not in st.session_state:
    st.session_state.app = app



st.session_state.app.render()