import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
import re

# Set default plotly template
pio.templates.default = "plotly_white"

# Load Excel data
df = pd.read_excel("PRE_QC_SUMMARY.xlsx", sheet_name="All_Data")

# Map short codes to city names
city_map = {
    "ATL": "Atlanta, GA",
    "BLT": "Baltimore, MD",
    "DLS": "Dallas, TX",
    "ISN": "Iselin, NJ",
    "LAX": "Los Angeles, CA",
    "ORL": "Orlando, FL",
    "STL": "St. Louis, MO"
}

# Extract city short code from file path using improved regex
def extract_city_code(path):
    match = re.search(r'/ds-([A-Z]{3})/', path)
    return match.group(1) if match else None

df['CityCode'] = df['File Path'].apply(extract_city_code)
df = df[df['CityCode'].isin(city_map.keys())]
df['City'] = df['CityCode'].map(city_map)

# Extract file name from full path
df['FileName'] = df['File Path'].apply(lambda x: x.split("/")[-1])

# Thresholds
thresholds = {
    'Duration (s)': 60,
    'Spectral Centroid (Hz)': 1000,
    'Spectral Bandwidth (Hz)': 1000,
    'Pitch Mean (Hz)': 100,
    'SNR (dB)': 10
}
features = list(thresholds.keys())

# Drop rows with missing values in key columns
df = df.dropna(subset=features + ['City'])

# Streamlit App
st.title("Pre-QC Feature Threshold Dashboard")

# City selector
city_selection = st.selectbox("Select City:", sorted(df['City'].unique()))
filtered_df = df[df['City'] == city_selection]

# Plot each feature
for feature in features:
    threshold = thresholds[feature]
    filtered_df['Threshold Exceeded'] = filtered_df[feature] > threshold

    fig = px.scatter(
        filtered_df,
        x=filtered_df.index,
        y=feature,
        color='Threshold Exceeded',
        hover_data={'FileName': True, feature: True},
        title=f"{feature} in {city_selection}",
        labels={'index': 'Sample Index'},
        template="plotly_white"
    )

    fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text="Threshold")
    st.plotly_chart(fig, use_container_width=True)
