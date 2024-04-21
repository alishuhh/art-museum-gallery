import streamlit as st
import requests
import os

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Define the base URL for the Met API
BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1/"

# Define the search endpoint
SEARCH_ENDPOINT = BASE_URL + "search"

# Function to search for artworks based on a query (either name or artist)
def search_artworks(query):
    # Define the parameters for the search
    params = {
        "q": query,
    }

    # Add artist filtering if specified
    # if is_artist:
    #     params["artistOrCulture"] = "true"

    # Make a GET request to the search endpoint
    response = requests.get(SEARCH_ENDPOINT, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data["objectIDs"]
    else:
        # Handle the error
        st.error(f"Failed to search artworks: {response.status_code}")
        return None

# Function to retrieve artwork by its ID
def get_artwork_by_id(artwork_id):
    # Define the URL for the specific artwork
    url = BASE_URL + "objects/" + str(artwork_id)

    # Make a GET request to the API
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Handle the error
        st.error(f"Failed to retrieve artwork: {response.status_code}")
        return None

# Function to display an image from a URL
def display_image(image_url):
    st.image(image_url)

# Streamlit app starts here
st.sidebar.header("The Met Collection")

# Input: Search query
query = st.sidebar.text_input("Search for an artwork")

# Checkbox to indicate if the search query is for an artist
# is_artist_search = st.sidebar.checkbox("Search by artist")

# Button to search and display the results
if st.sidebar.button("Search"):
    # Search for artworks based on the query
    object_ids = search_artworks(query)

    # Check if object IDs were retrieved
    if object_ids:
        # Display the total number of results
        st.sidebar.text(f"Found {len(object_ids)} artworks")

        # Loop through the object IDs and display each artwork
        for object_id in object_ids[:5]:  # Displaying only first 5 results for demonstration
            artwork_data = get_artwork_by_id(object_id)

            # Check if artwork data was retrieved
            if artwork_data:
                st.subheader(artwork_data.get("title", "Untitled"))

                # Get the image URL
                primary_image = artwork_data.get("primaryImage")
                if primary_image:
                    # Display the image
                    display_image(primary_image)
                else:
                    st.warning("No image available for this artwork.")

                # Display the artwork information

                st.text(f"Artist: {artwork_data.get('artistDisplayName', 'Unknown')}")
                st.text(f"Date: {artwork_data.get('objectDate', 'N/A')}")
                if artwork_data.get('culture'):
                        st.text(f"Culture: {artwork_data.get('culture', 'N/A')}")
                st.text(f"Medium: {artwork_data.get('medium', 'N/A')}")


    else:
        st.warning("No artworks found for the query.")
