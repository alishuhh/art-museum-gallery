import streamlit as st
import requests
import os

st.set_page_config(layout="wide")

css_file = os.path.abspath('style.css')
with open(css_file) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)



met_page = os.path.abspath('pages/metapi.py')
aci_page = os.path.abspath('pages/aciapi.py')
st.sidebar.write("#")
st.sidebar.write("#")
st.sidebar.image(os.path.abspath("misc/Group 2button1.png"))
st.sidebar.page_link(met_page, label="Metropolitan Museum of Art")
st.sidebar.page_link(aci_page, label="Art Institute of Chicago")
st.sidebar.divider()


if st.checkbox('Cats?'):
    st.image(os.path.abspath('misc/Group 5catslogo.png'), width=1300, caption="Meow")
else:
    st.image(os.path.abspath('misc/Group 4largermainlogo.png'), width=1300)

