import streamlit as st
import requests
import os

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

home_page = os.path.abspath('homepage.py')
met_page = os.path.abspath('pages/metapi.py')
collection_page = os.path.abspath('pages/MetCollectionData.py')
st.sidebar.write("#")
if st.sidebar.button("HOME"):
    st.switch_page(home_page)
st.sidebar.header("Metropolitan Museum of Art")
st.sidebar.page_link(met_page, label="Search Collection")
st.sidebar.page_link(collection_page, label="Collection Data")
st.sidebar.divider()
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)


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
    st.image(image_url, width=500)


# Streamlit Code
met_image1 = os.path.abspath('misc/The_Metropolitan_Museum_of_Art_Logo.svg.png')
placeholder_img = st.image(met_image1, width=200)
placeholder_txt = st.header("Metropolitan Museum of Art Collection")

query = st.sidebar.text_input("Search for an artwork")


if st.sidebar.button("Search"):
    object_ids = search_artworks(query)
    placeholder_img.empty()
    placeholder_txt.empty()
    st.header(f"Showing results for {query}...")

    if object_ids:
        st.sidebar.text(f"Found {len(object_ids)} artworks")

        for object_id in object_ids[:15]:
            artwork_data = get_artwork_by_id(object_id)

            if artwork_data:

                primary_image = artwork_data.get("primaryImage")
                if primary_image:
                    display_image(primary_image)
                else:
                    st.warning("Image unavailable.")

                st.write(f"**{artwork_data.get("title", "Untitled")}**")

                st.write(f"Artist: {artwork_data.get('artistDisplayName', 'Unknown')}")
                st.write(f"Date: {artwork_data.get('objectDate', 'No information')}")
                if artwork_data.get('culture'):
                        st.write(f"Culture: {artwork_data.get('culture', 'No information')}")
                st.write(f"Medium: {artwork_data.get('medium', 'No information')}")
                st.divider()
    else:
        st.error("No artworks found.")
else:
    select_box = st.select_slider("Museum Photos", options=["Image 1", "Image 2", "Image 3"])
    if select_box == "Image 1":
        st.image(os.path.abspath('misc/METIMG.webp'), width=700)
    elif select_box == "Image 2":
        st.image(os.path.abspath('misc/The-Met_2018_GettyImages-541359628.webp'), width=700)
    elif select_box == "Image 3":
        st.image(os.path.abspath('misc/Petrie-Court_Brett-Beyer_2048x2048.jpg'), width=700)

