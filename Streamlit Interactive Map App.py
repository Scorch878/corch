import pandas as pd
import streamlit as st
import plotly.express as px
import random
from pathlib import Path
import matplotlib.colors as mcolors
import numpy as np

if "random_css_colors" not in st.session_state:
    # Sample 13 unique CSS4 named colors (e.g., "coral", "teal", "gold", ...)
    st.session_state.random_css_colors = random.sample(
        list(mcolors.CSS4_COLORS.keys()), 13
    )

# Needed some help from Claude here to make the schools with identical lat and lon be distinguishable
def spread_duplicates(df, radius=0.003):
    df = df.copy()
    grp = df.groupby(["Latitude", "Longitude"])
    n = grp["School Name"].transform("size")
    i = grp.cumcount()
    angle = 2 * np.pi * i / n
    dup = n > 1
    df.loc[dup, "Latitude"] += radius * np.sin(angle[dup])
    df.loc[dup, "Longitude"] += radius * np.cos(angle[dup])
    return df

data = pd.read_csv("bd_british_council_exam_schools.csv", usecols=['School Name', 'City', 'Area', 'Latitude', 'Longitude'])
st.write("## Schools in Bangladesh")
with st.expander("School List: "):
    st.dataframe(data)

modes = ["All Cities", "Select a City(ies):"]
choice = st.sidebar.selectbox("Mode:", modes)

if choice == "All Cities":

    fig = px.scatter_map(data, 
                         lat ="Latitude", 
                         lon ="Longitude", 
                         hover_name = 'School Name', 
                         text='Area',
                         color="City",  
                         color_discrete_sequence=["magenta"], 
                         center = dict(lat=23.81, lon=90.41),
                         zoom=10)
    
    fig.update_layout(map_style="open-street-map")
    st.plotly_chart(fig)

elif choice == "Select a City(ies):":

    citylist = data["City"].unique().tolist()

    cityselect = st.sidebar.multiselect("City:",citylist)
    city_data = data[data["City"].isin(cityselect)]

    schoollist = city_data["School Name"].unique().tolist()
    schoolselect = st.sidebar.multiselect("School Name:",schoollist)
    school_data = city_data[city_data["School Name"].isin(schoolselect)]
    school_data = spread_duplicates(school_data)



    fig = px.scatter_map(school_data, 
                         lat ="Latitude", 
                         lon ="Longitude", 
                         hover_name = 'School Name', 
                         hover_data ='Area', 
                         color="City", 
                         color_discrete_sequence=["red"], 
                         center = dict(lat=23.81, lon=90.41),
                         zoom=10)
    
    fig.update_layout(map_style="open-street-map")
    st.plotly_chart(fig)



    



