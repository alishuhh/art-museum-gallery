import requests
import os
import streamlit as st

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

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
home_page = os.path.abspath('homepage.py')
aci_page = os.path.abspath('pages/aciapi.py')
aci_data = os.path.abspath('pages/AciCollectionData.py')

st.sidebar.write("#")
if st.sidebar.button("HOME"):
    st.switch_page(home_page)
st.sidebar.header("Art Institute of Chicago")
st.sidebar.page_link(aci_page, label="Search Collection")
st.sidebar.page_link(aci_data, label="Collection Data")
st.sidebar.divider()
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)


aci_logo_file = os.path.abspath('misc/Art_Institute_of_Chicago_logo.svg.png')
aci_logo = st.image(aci_logo_file, width=300)
aci_header = st.header("Art Institute of Chicago Collection")

# select_box = st.slider("Museum Photos",min_value=1, max_value=3)
# if select_box == 1:
#     st.image(os.path.abspath('misc/image.jpg'), width=700)
# elif select_box == 2:
#     st.image(os.path.abspath('misc/Hero. Mobile App_Nighthawks_WEB72dpi.jpg'), width=700)
# elif select_box == 3:
#     st.image(os.path.abspath('misc/Art-Institute-of-Chicago_2018_Ryerson_Library.webp'), width=700)

search_query = st.sidebar.text_input("Search for an artwork or artist")
search_button = st.sidebar.button("Search")

if search_button:
    aci_logo.empty()
    aci_header.empty()
    if search_query:
        search_results = search_artworks(search_query)
        st.header(f"Showing results for {search_query}...")
        if search_results is not None:
            for artwork in search_results:  # Iterate over search_results list
                artwork_details = fetch_artwork_by_id(artwork['id'])
                if artwork_details is not None:
                    image_id = artwork_details.get('image_id')
                    if image_id:
                        image_url = f"https://www.artic.edu/iiif/2/{image_id}/full/400,/0/default.jpg"
                        st.image(image_url, width=500)
                    st.write(f"**{artwork_details.get('title', '')}**")
                    st.write(artwork_details.get('artist_title', ''))
                    st.write(artwork_details.get('place_of_origin', ''))
                    st.write("Medium:", artwork_details.get('medium_display', ''))
                    st.write("------------")


        else:
            st.warning("No artworks found. Please refine your search criteria.")
    else:
        st.warning("Please enter a search query.")
else:
    select_box = st.slider("Museum Photos", min_value=1, max_value=3)
    if select_box == 1:
        st.image(os.path.abspath('misc/image.jpg'), width=700)
    elif select_box == 2:
        st.image(os.path.abspath('misc/Hero. Mobile App_Nighthawks_WEB72dpi.jpg'), width=700)
    elif select_box == 3:
        st.image(os.path.abspath('misc/Art-Institute-of-Chicago_2018_Ryerson_Library.webp'), width=700)