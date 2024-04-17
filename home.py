import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np

st.title("Art Museum Gallery")
st.header("Explore your favorite museum's collection")

# st.image("art-museum-gallery\misc\Charles Van den Eycken.jpg", width = 700)

museum_choice = st.selectbox("Select a museum", ["", "Art Institute of Chicago"])

if museum_choice == "Art Institute of Chicago":
    st.image("art-museum-gallery\misc\Art-Institute-of-Chicago_2018_Ryerson_Library.webp")
    st.text_input("Search for an artwork or artist")
    # rest of app

else:
    st.image("art-museum-gallery\misc\Charles Van den Eycken.jpg", width = 700, caption = "Kittens At Play By Charles Van Den Eycken")


