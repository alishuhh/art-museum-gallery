from urllib import response
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

url = "https://api.artic.edu/api/v1/artworks"

response = requests.get(url)

if response.status_code == 200:
    print(response.json())

    jsonData = response.json()
    data = pd.json_normalize(jsonData['data'])
    columns_to_save = ['artist_title', 'title', 'place_of_origin', 'date_start', 'date_end', 'medium_display',
                       'dimensions', 'credit_line', 'main_reference_number', 'category_titles',
                       'style_title',
                       'description']
    data[columns_to_save].to_csv('artworks.csv', index=False)
else:
    print(f'failed to fetch data:{response.status_code}')

st.sidebar.header("Search The Collection")
search_query = st.sidebar.text_input("Search for an artwork or artist")
st.sidebar.header("Filter")
artist_selection = st.sidebar.selectbox("Artist", ["", "Picasso", "Delacroix", "Monet"])
origin_selection = st.sidebar.selectbox("Place of Origin", ["", "United States", "France", "India"])
type_selection = st.sidebar.selectbox("Artwork Type", ["", "Metalwork", "Painting", "Glass"])
style_selection = st.sidebar.selectbox("Art Style", ["", "Impressionist", "Modernist", "Renaissance"])
department_selection = st.sidebar.selectbox("Department", ["", "1", "2", "3"])

st.title("Art Museum Gallery")
st.header("Explore your favorite museum's collection")

museum_choice = st.selectbox("Select a museum", ["", "Art Institute of Chicago"])

if museum_choice == "Art Institute of Chicago":
    st.subheader(f"Showing results: *{search_query}*")
    # rest of app

else:
    st.image('misc/Charles Van den Eycken.jpg', width=700, caption="Kittens At Play By Charles Van Den Eycken")
