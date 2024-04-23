import os
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

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

accession_csv = os.path.abspath('misc/accession_year_data.csv')
culture_csv = os.path.abspath('misc/culture_data.csv')

accession_data = pd.read_csv(accession_csv)
culture_data = pd.read_csv(culture_csv)

culture_data_sorted = culture_data.sort_values(by='Count', ascending=False)
top_10_cultures = culture_data_sorted.head(10)

st.header("Artwork Grouped by Accession Year")

radio1 = st.radio("Data Type", ["Graphical Data", "Raw Data"], key=1)
if radio1 == "Graphical Data":
    fig = px.area(
        accession_data,  # Data Frame
        x='AccessionYear',  # Columns from the data frame
        y='Count'
    )

    color = st.color_picker("Change color", value="#B61C2E", key=3)
    fig.update_traces(line_color=color)
    fig.for_each_trace(lambda trace: trace.update(fillcolor=color))
    fig.update_layout(height=600)
    fig.update_layout(width=900)
    st.plotly_chart(fig, width=900, height=600)
if radio1 == "Raw Data":
    st.dataframe(accession_data)

st.divider()
st.header("Artwork Grouped by Culture")

radio2 = st.radio("Data Type", ["Graphical Data (Highest 10)", "Raw Data"], key=2)
if radio2 == "Graphical Data (Highest 10)":
    fig2 = px.bar(
        top_10_cultures,  # Data Frame
        y='Culture',  # Columns from the data frame
        x='Count'
    )

    color = st.color_picker("Change color", value="#B61C2E", key=4)
    fig2.update_traces(marker_color=color)
    fig2.update_layout(height=800)
    st.plotly_chart(fig2, use_container_width=True, height=800)
if radio2 == "Raw Data":
    st.dataframe(culture_data_sorted)
