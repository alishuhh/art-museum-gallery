import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px


css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

csv_file = os.path.abspath('misc/MetObjects.csv')
df = pd.read_csv(csv_file)

accession_data = df.groupby('AccessionYear').size().reset_index(name='Count')

culture_data = df.groupby('Culture').size().reset_index(name='Count')
culture_data_sorted = culture_data.sort_values(by='Count', ascending=False)
top_10_cultures = culture_data_sorted.head(10)

# Base endpoint
BASE_ENDPOINT = "https://collectionapi.metmuseum.org/public/collection/v1/"
# Search endpoint
SEARCH_ENDPOINT = BASE_ENDPOINT + "search"


# Search artworks function
def search_artworks(query):
    params = {
        "q": query,
    }
    response = requests.get(SEARCH_ENDPOINT, params=params)
    data = response.json()
    return data["objectIDs"]


# Retrieve artworks by ID
def get_artwork_by_id(artwork_id):
    url = BASE_ENDPOINT + "objects/" + str(artwork_id)
    response = requests.get(url)
    data = response.json()
    return data


# Display images
def display_image(image_url):
    st.image(image_url)


# Streamlit Code

met_image1 = os.path.abspath('misc/The_Metropolitan_Museum_of_Art_Logo.svg.png')
# met_image2 = os.path.abspath("misc/The-Met_2018_GettyImages-541359628.webp")

placeholder_img = st.image(met_image1)
placeholder_txt = st.header("Metropolitan Museum of Art Collection")
# st.image(met_image2, width=800)

st.sidebar.header("The Met Collection")

query = st.sidebar.text_input("Search for an artwork")

if st.sidebar.button("Search"):
    object_ids = search_artworks(query)
    placeholder_img.empty()
    placeholder_txt.empty()
    st.header(f"Showing results for {query}...")

    if object_ids:
        st.sidebar.text(f"Found {len(object_ids)} artworks")

        for object_id in object_ids[:5]:
            artwork_data = get_artwork_by_id(object_id)

            if artwork_data:
                st.subheader(artwork_data.get("title", "Untitled"))

                primary_image = artwork_data.get("primaryImage")
                if primary_image:
                    display_image(primary_image)
                else:
                    st.warning("Image unavailable.")

                st.text(f"Artist: {artwork_data.get('artistDisplayName', 'Unknown')}")
                st.text(f"Date: {artwork_data.get('objectDate', 'No information')}")
                if artwork_data.get('culture'):
                        st.text(f"Culture: {artwork_data.get('culture', 'No information')}")
                st.text(f"Medium: {artwork_data.get('medium', 'No information')}")


    else:
        st.warning("No artworks found.")


if st.sidebar.button("Collection Data"):
    placeholder_img.empty()
    placeholder_txt.empty()

    # parameter = st.radio("Select a parameter",
    #                      ["AccessionYear", "Period", "Culture"])

    # Sample data for number of artworks acquired each year (replace with actual data)
    fig = px.bar(
        accession_data,  # Data Frame
        x='AccessionYear',  # Columns from the data frame
        y='Count',
        title='Accession Year'
    )
    fig.update_traces(marker_color="#D30000")

    fig.update_layout(height=800)
    fig.update_layout(width=1000)
    st.plotly_chart(fig, width=1000, height=800)

    fig2 = px.bar(
        top_10_cultures,  # Data Frame
        y='Culture',  # Columns from the data frame
        x='Count',
        title='Culture'
    )
    fig2.update_traces(marker_color="#D30000")

    fig2.update_layout(height=800)
    st.plotly_chart(fig2, use_container_width=True, height=800)

