import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

# Set custom page config
st.set_page_config(page_title="Beijing Air Quality Dashboard", layout="wide")

# Load cleaned dataset
df = pd.read_csv("fixData_air_quality.csv", parse_dates=['datetime'])

# Load station coordinates
station_coords = {
    "Aotizhongxin": [40.040833, 116.408056],
    "Changping": [40.2186, 116.2219],
    "Dingling": [40.292, 116.227],
    "Dongsi": [39.929, 116.417],
    "Guanyuan": [39.929, 116.339],
    'Gucheng': [39.9289, 116.1633],
    'Huairou': [40.3283, 116.6374],
    'Nongzhanguan': [39.9336, 116.4617],
    'Shunyi': [40.1250, 116.6564],
    'Tiantan': [39.8836, 116.4122],
    'Wanliu': [39.9747, 116.3033],
    'Wanshouxigong': [39.8783, 116.3525]
}

# Custom CSS style
st.markdown("""
    <style>
    .main { background-color: #f7f7f7; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .css-1d391kg { background-color: #ffffff; border-radius: 10px; padding: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); }
    h1, h2, h3 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("\U0001F30E Beijing Air Quality Dashboard")
st.markdown("""
    Explore the air quality trends, pollution distribution, and correlations with meteorological factors
    across various monitoring stations in Beijing from 2013 to 2017.
""")

# Sidebar Filters
with st.sidebar:
    st.header("\U0001F50D Filter Options")
    station = st.selectbox("Select Monitoring Station", df['station'].unique())
    date_range = st.date_input("Select Date Range", [df['datetime'].min(), df['datetime'].max()])
    date_range = pd.to_datetime(date_range)

# Filtered DataFrame
df_filtered = df[(df['station'] == station) & (df['datetime'].between(date_range[0], date_range[1]))]

# Tabs
tabs = st.tabs(["Summary", "Trends", "Spatial Map"])

# Summary Tab
with tabs[0]:
    st.subheader(f"Data Summary for {station}")
    st.write(df_filtered.describe())

    # PM2.5 Distribution
    st.subheader("Distribution of PM2.5")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df_filtered['PM2.5'], bins=30, kde=True, ax=ax, color='salmon')
    st.pyplot(fig)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    wind_dir_mapping = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
        'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
        'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }
    if 'wind_direction' in df_filtered.columns:
        df_filtered['wind_direction_numeric'] = df_filtered['wind_direction'].map(wind_dir_mapping)
    df_filtered_numeric = df_filtered.select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_filtered_numeric.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    st.pyplot(fig)

# Trends Tab
with tabs[1]:
    st.subheader("PM2.5 Trend Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=df_filtered, x='datetime', y='PM2.5', ax=ax, color='teal')
    ax.set_xlabel("Date")
    ax.set_ylabel("PM2.5 (µg/m³)")
    st.pyplot(fig)

    st.subheader("Average PM2.5 by Hour")
    hourly_avg = df_filtered.groupby(df_filtered['datetime'].dt.hour)['PM2.5'].mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', color='darkorange', ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Avg PM2.5 (µg/m³)")
    st.pyplot(fig)

    st.subheader("Yearly Trend")
    df_filtered['year'] = df_filtered['datetime'].dt.year
    yearly = df_filtered.groupby('year')['PM2.5'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=yearly, x='year', y='PM2.5', marker='o', ax=ax)
    ax.set_title("PM2.5 Yearly Trend")
    st.pyplot(fig)

# Spatial Map Tab
with tabs[2]:
    st.subheader("PM2.5 Distribution Map")
    m = folium.Map(location=[39.9, 116.4], zoom_start=10)

    avg_pm25 = df.groupby("station")["PM2.5"].mean().reset_index()

    def get_color(pm):
        if pm < 50:
            return "green"
        elif pm < 100:
            return "orange"
        elif pm < 150:
            return "red"
        else:
            return "purple"

    for _, row in avg_pm25.iterrows():
        name = row['station']
        pm = row['PM2.5']
        if name in station_coords:
            folium.CircleMarker(
                location=station_coords[name],
                radius=10,
                color=get_color(pm),
                fill=True,
                fill_opacity=0.7,
                popup=f"{name}: {pm:.2f} µg/m³"
            ).add_to(m)

    folium_static(m)
    st.markdown("""
    Green Marks indicate PM2.5 Distribution is less than 50 µg/m³ <p>
    Orange Marks indicate PM2.5 Distribution is less than 100 µg/m³ <p>
    Red Marks indicate PM2.5 Distribution is less than 150 µg/m³ <p>
    Purple Marks indicate PM2.5 Distribution is more than 150 µg/m³
""", unsafe_allow_html=True)


st.markdown("""
    <hr>
    <small>Developed by MhdFrhn | Powered by Streamlit & Folium | 2025</small>
""", unsafe_allow_html=True)
