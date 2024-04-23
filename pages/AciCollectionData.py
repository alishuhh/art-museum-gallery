import os
import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

home_page = os.path.abspath('homepage.py')
aci_page = os.path.abspath('pages/aciapi.py')
collection_page = os.path.abspath('pages/AciCollectionData.py')
st.sidebar.write("#")
if st.sidebar.button("HOME"):
    st.switch_page(home_page)
st.sidebar.header("Art Institute of Chicago")
st.sidebar.page_link(aci_page, label="Search Collection")
st.sidebar.page_link(collection_page, label="Collection Data")
st.sidebar.divider()



st.subheader("Location")
# Coordinates of the Art Institute of Chicago
latitude = 41.8796
longitude = -87.6224

# Create a DataFrame with the coordinates
location = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})

# Display the map centered on the Art Institute of Chicago
a_map = st.map(data=location, zoom=15)