import os
import streamlit as st
import requests
import pandas as pd
import numpy as np

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# Function to fetch artworks from the API
def fetch_artworks(url):
    response = requests.get(url)
    if response.status_code == 200:
        jsonData = response.json()
        data = jsonData['data']
        return data
    else:
        st.error(f'Failed to fetch data: {response.status_code}')
        return None

# Function to fetch a single artwork by ID
def fetch_artwork_by_id(artwork_id):
    artwork_url = f"https://api.artic.edu/api/v1/artworks/{artwork_id}"
    return fetch_artworks(artwork_url)

# Function to search artworks
def search_artworks(query):
    search_url = f"https://api.artic.edu/api/v1/artworks/search?q={query}"
    return fetch_artworks(search_url)

# Main app logic
st.sidebar.header("Search The Collection")
search_query = st.sidebar.text_input("Search for an artwork or artist")
search_button = st.sidebar.button("Search")

# Filtering options
st.sidebar.header("Filter")

# Additional choices for art style
art_style_choices = ["", "Japanese (culture or style)", "21st Century", "19th century", "20th Century",
                     "Chinese (culture or style)", "Modernism", "Arts of the Americas", "Americas", "Impressionism"]
style_selection = st.sidebar.selectbox("Art Style", art_style_choices)

# Additional choices for artwork type
artwork_type_choices = ["", "Print", "Photograph", "Drawing and Watercolor", "Textile", "Painting",
                        "Architectural Drawing", "Vessel", "Book"]
type_selection = st.sidebar.selectbox("Artwork Type", artwork_type_choices)

# Additional choices for place of origin
place_choices = ["", "United States", "France", "Japan", "England", "Italy", "Germany", "China", "Netherlands"]
origin_selection = st.sidebar.selectbox("Place of Origin", place_choices)

# Additional choices for artists
artist_choices = ["", "Utagawa Hiroshige", "Unknown Maker", "Unknown", "Ancient Roman", "James McNeill Whistler",
                  "Ancient Egyptian", "Jasper Johns", "Unknown artist", "Pablo Picasso"]
artist_selection = st.sidebar.selectbox("Artist", artist_choices)

# Additional choices for departments
department_choices = ["", "Applied Arts of Europe", "Architecture and Design", "Arts of Africa", "Arts of Asia",
                       "Arts of the Americas", "Arts of the Ancient Mediterranean and Byzantium", "Contemporary Art",
                       "Modern Art", "Modern and Contemporary Art", "Painting and Sculpture of Europe",
                       "Photography and Media", "Prints and Drawings", "Research Center", "Textiles"]
department_selection = st.sidebar.selectbox("Department", department_choices)

# Checkboxes for "On view"
show_only_on_view = st.sidebar.checkbox("Show Pieces On View")


st.title("Art Museum Gallery")
st.header("Explore your favorite museum's collection")

museum_choice = st.selectbox("Select a museum", ["", "Art Institute of Chicago"])

if museum_choice == "Art Institute of Chicago":
    st.subheader("Location")
    # Coordinates of the Art Institute of Chicago
    latitude = 41.8796
    longitude = -87.6224

    # Create a DataFrame with the coordinates
    location = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})

    # Display the map centered on the Art Institute of Chicago
    st.map(data=location, zoom=15)

    
    if search_button:
        if search_query:
            search_results = search_artworks(search_query)
            if search_results is not None:
                for artwork in search_results:  # Iterate over search_results list
                    artwork_details = fetch_artwork_by_id(artwork['id'])
                    if artwork_details is not None:
                        image_id = artwork_details.get('image_id')
                        if image_id:
                            image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/400,/0/default.jpg"
                            st.image(image_url, width=200)
                        st.write(f"**{artwork_details.get('title', '')}**")
                        st.write(artwork_details.get('artist_title', ''))
                        st.write(artwork_details.get('place_of_origin', ''))
                        st.write("Medium:", artwork_details.get('medium_display', ''))
                        st.write("------------")
               
            else:
                st.info("No artworks found. Please refine your search criteria.")
        else:
            st.info("Please enter a search query.")
    else:
        default_results = fetch_artworks("https://api.artic.edu/api/v1/artworks")

        if default_results is not None:
            default_df = pd.DataFrame(default_results)
            columns_to_save = ['artist_title', 'title', 'place_of_origin', 'medium_display',
                                'category_titles','style_title', 'image_id', 'department_title', 'is_on_view']
            default_df[columns_to_save].to_csv('artworks.csv', index=False)

            for index, artwork in default_df.iterrows():
                # Filter based on user selections
                if (style_selection == "" or artwork['style_title'] == style_selection) and \
                   (type_selection == "" or artwork['type'] == type_selection) and \
                   (origin_selection == "" or artwork['place_of_origin'] == origin_selection) and \
                   (artist_selection == "" or artwork['artist_title'] == artist_selection) and \
                   (department_selection == "" or artwork['department_title'] == department_selection) and \
                   (not show_only_on_view or artwork['is_on_view']):
                    image_id = artwork['image_id']
                    image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/400,/0/default.jpg"
                    st.image(image_url, width=200)
                    st.write(f"**{artwork['title']}**")
                    st.write(artwork['artist_title'])
                    st.write(artwork['place_of_origin'])
                    st.write("Medium:", artwork['medium_display'])
                    st.write("------------")
        else:
            st.info("No artworks found at the moment.")


else:
    st.image(os.path.abspath('misc/Charles Van den Eycken.jpg'), width=700, caption="Kittens At Play By Charles Van Den Eycken")
