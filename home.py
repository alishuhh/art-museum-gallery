import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

st.sidebar.header("Search The Collection")
search_query = st.sidebar.text_input("Search for an artwork or artist")
st.sidebar.header("Filter")
artist_selection = st.sidebar.selectbox("Artist", ["","Picasso","Delacroix","Monet"])
origin_selection = st.sidebar.selectbox("Place of Origin", ["","United States","France","India"])
type_selection = st.sidebar.selectbox("Artwork Type", ["","Metalwork","Painting","Glass"])
style_selection = st.sidebar.selectbox("Art Style", ["","Impressionist","Modernist","Renaissance"])
department_selection = st.sidebar.selectbox("Department", ["","1","2","3"])



st.title("Art Museum Gallery")
st.header("Explore your favorite museum's collection")

museum_choice = st.selectbox("Select a museum", ["", "Art Institute of Chicago"])

if museum_choice == "Art Institute of Chicago":    
    st.subheader(f"Showing results: *{search_query}*")
    # rest of app

else:
    st.image('C:/Users/alish/Desktop/ArtApp/art-museum-gallery/misc/Charles Van den Eycken.jpg', width = 700, caption = "Kittens At Play By Charles Van Den Eycken")


