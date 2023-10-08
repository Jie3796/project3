import streamlit as st
import plotly.express as px
import json
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import altair as alt
import plotly.figure_factory as ff
import numpy as np
import os

def make_heatmap(geojson_data, data, gdf, feature):
    columns = ['County_FIPS_str']
    columns.append(feature)
    # Create a base map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    
    # Create a choropleth map
    feature_name = f"{feature}(%)" if feature not in ['Number of Dentists', 'Overall SVI'] else feature
    folium.Choropleth(
        geo_data=geojson_data,
        name='choropleth',
        data=data,
        columns=columns,
        key_on='feature.properties.GEO_ID',
        fill_color='YlOrRd',  # Changed color scheme to red
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=feature_name
    ).add_to(m)
    
    # Adding a GeoJson layer with a tooltip to display the percentage value on hover
    style_function = lambda x: {'fillColor': '#ffffff', 
                                'color':'#000000', 
                                'fillOpacity': 0.1, 
                                'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.50, 
                                    'weight': 0.1}
    
    fields=['GEO_ID', 'County', 'State']
    aliases=['GEO_ID:', 'County:', 'State:']
    fields.append(feature)
    aliases.append(feature+":")

    tooltip = folium.features.GeoJsonTooltip(
        fields=fields,
        aliases=aliases,
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"),
        sticky=True
    )

    geojson = folium.features.GeoJson(
        gdf,
        style_function=style_function, 
        control=False,
        highlight_function=highlight_function, 
        tooltip=tooltip
    )
    m.add_child(geojson)
    m.keep_in_front(geojson)
    folium_static(m)

def make_histogram(df, feature):
    base = alt.Chart(df)
    bin_step = (df[feature].max() - df[feature].min()) / 15

    hist = base.mark_bar().encode(
        x=alt.X(feature + ':Q', bin=alt.BinParams(step=bin_step)), # 
        y='count()'
    )

    # 中线
    median_line = base.mark_rule().encode(
        x=alt.X('mean(' + feature + '):Q', title=feature),
        size=alt.value(5)
    )

    st.altair_chart(hist + median_line, use_container_width=True)

def make_cat_histogram(df, feature):
    base = alt.Chart(df)

    risk_mapping = {0: 'Low risk', 1: 'Medium risk', 2: 'High risk'}
    df['Risk'] = df[feature].map(risk_mapping)

    hist = base.mark_bar().encode(
        x=alt.X('Risk:O', 
                sort=['Low risk', 'Medium risk', 'High risk'], 
                title='Risk Level'),  # 使用Risk列作为x轴，并且指定排序和标题
        y='count()'
    )

    st.altair_chart(hist, use_container_width=True)

def make_scatter_plot_census_tracts(df, feature_1, feature_2 = 'Diagnosed Diabetes Percentage',
                                    category_feature = "Risk Category"):
    category_mapping = {0: 'Low Risk', 1: 'Medium Risk', 2: 'High Risk'}
    df[category_feature] = df[category_feature].replace(category_mapping)
    scatter = alt.Chart(df).mark_point() \
        .encode(x=feature_1 + ':Q', y=feature_2 + ':Q',
                color=alt.Color(
                    category_feature + ':N',
                    ),
                tooltip=[feature_1, feature_2, category_feature]).interactive()
    st.altair_chart(scatter, use_container_width=True)

def county_data_explorer(data):
    
    st.write(r"We perform visual and statistical analysis on diabetes data to understand its characteristics, structure, and anomalies. The features of the diabetes data include **'Diagnosed Diabetes Percentage', 'Access to Exercise Opportunities,' 'Children in Poverty,' 'Food Insecurity,' 'Households with No Internet Service,' 'Number of Dentists,' 'Overall SVI,' and 'Severe Housing Cost Burden.'** Among them, we have transformed 'Diagnosed Diabetes Percentage' into the target: high risk, medium risk, and low risk.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Regional Feature Heatmap")
    st.write("Visualizes differences or trends in specific features between different regions or locations.")
    st.markdown("<br>", unsafe_allow_html=True)
    feature = st.selectbox('Select feature', ['Diagnosed Diabetes Percentage', 
                                              'Access to Exercise Opportunities',
                                              'Children in Poverty',
                                              'Food Insecurity',
                                              'Household with No Internet Service',
                                              'Number of Dentists',
                                              'Overall SVI',
                                              'Severe Housing Cost Burden'], 0)
    st.markdown("<br>", unsafe_allow_html=True)
    data['County_FIPS_str'] = data['County_FIPS'].astype(int).astype(str).str.zfill(5)
    data['County_FIPS_str'] = '0500000US' + data['County_FIPS_str']
    
    # Merge the GeoJSON data with the diabetes percentage data
    cur_path = os.getcwd()
    with open(cur_path + '/data/gz_2010_us_050_00_20m.json', encoding='latin-1') as f:
        geojson_data = json.load(f)
        geojson_str = json.dumps(geojson_data)

    # Now use geopandas to read the GeoJSON string
    gdf = gpd.read_file(geojson_str)
    gdf = gdf.merge(data, left_on='GEO_ID', right_on='County_FIPS_str')
    make_heatmap(geojson_data, data, gdf, feature)
    st.markdown("<br>", unsafe_allow_html=True)
    

    st.subheader(f"{feature} Distribution")
    st.write("Using a histogram to analyze data distribution helps understand the shape of the distribution and identify anomalies in the data.")
    st.markdown("<br>", unsafe_allow_html=True)
    make_histogram(data, feature)
    st.markdown("<br>", unsafe_allow_html=True)

    if feature == 'Diagnosed Diabetes Percentage':
        st.subheader("Target Variable Distribution")
        st.write("'Diagnosed Diabetes Percentage' has been transformed into the target: high risk, medium risk, and low risk.")
        st.markdown("<br>", unsafe_allow_html=True)
        make_cat_histogram(data, "Risk Category")
        st.write(r"**Note that**: 'Diagnosed Diabetes Percentage' feature will be removed after transformed into categorical target")
        st.markdown("<br>", unsafe_allow_html=True)

    st.subheader(f"Relation Between {feature} and Target.")
    st.write("By plotting two-dimensional charts of feature values and the target variable, you can determine whether there is a linear relationship between them.")
    st.markdown("<br>", unsafe_allow_html=True)
    make_scatter_plot_census_tracts(data, feature)
    st.markdown("<br>", unsafe_allow_html=True)

   