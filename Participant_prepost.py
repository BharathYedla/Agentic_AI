import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="Participant Dashboard", layout="wide")

# Load participant data
@st.cache_data

def load_data():
    df = pd.read_csv("participants.tsv", sep="\t")
    df["city_code"] = df["id_number"].astype(str).apply(lambda x: re.match(r"([A-Z]+)", x).group(1) if re.match(r"([A-Z]+)", x) else None)
    df["age"] = df["ss_child_chronological_age"].astype(str).apply(
        lambda x: float(x.split(" ")[0]) + float(x.split(" ")[2])/12 if "years" in x and "months" in x else None
    )
    return df.dropna(subset=["city_code", "age"])

df = load_data()

# City mapping
city_map = {
    "ATL": "Atlanta, GA",
    "BLT": "Baltimore, MD",
    "CHI": "Chicago, IL",
    "DLS": "Dallas, TX",
    "ISN": "Iselin, NJ",
    "LAX": "Los Angeles, CA",
    "ORL": "Orlando, FL",
    "STL": "St. Louis, MO"
}
df["City"] = df["city_code"].map(city_map)

# US city coordinates for map plot
city_coords = {
    "Atlanta, GA": (33.749, -84.388),
    "Baltimore, MD": (39.2904, -76.6122),
    "Chicago, IL": (41.8781, -87.6298),
    "Dallas, TX": (32.7767, -96.7970),
    "Iselin, NJ": (40.5754, -74.3221),
    "Los Angeles, CA": (34.0522, -118.2437),
    "Orlando, FL": (28.5383, -81.3792),
    "St. Louis, MO": (38.6270, -90.1994)
}
city_df = df["City"].value_counts().rename_axis("City").reset_index(name="Count")
city_df["lat"] = city_df["City"].map(lambda x: city_coords.get(x, (0, 0))[0])
city_df["lon"] = city_df["City"].map(lambda x: city_coords.get(x, (0, 0))[1])

# KPI Cards
st.title("Participant Overview Dashboard")
kpi1, kpi2 = st.columns(2)
kpi1.metric("Total Participants", len(df))
kpi2.metric("Total Cities", df["City"].nunique())

# US Map
st.subheader("Participants by Region (US Map)")
fig_map = px.scatter_geo(city_df, lat="lat", lon="lon", text="City",
                         size="Count", scope="usa",
                         color="Count", color_continuous_scale="Blues",
                         title="Participant Distribution Across Cities")
st.plotly_chart(fig_map, use_container_width=True)

# Age Distribution
st.subheader("Age Distribution")
fig_age = px.histogram(df, x="age", nbins=20, title="Age Distribution (Years)", color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig_age, use_container_width=True)

# Demographic Group
if "ss_demographic_groups" in df.columns:
    st.subheader("Participants by Demographic Group")
    demo_df = df["ss_demographic_groups"].value_counts().reset_index()
    demo_df.columns = ["Demographic Group", "Count"]
    fig_demo = px.bar(demo_df, x="Demographic Group", y="Count", color="Demographic Group",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_demo, use_container_width=True)

# Pre-QC Plot
st.subheader("Pre-QC Overall Eligibility")
pre_df = pd.read_excel("PRE_QC_SUMMARY.xlsx", sheet_name="All_Data")
pre_df['CityCode'] = pre_df['File Path'].apply(lambda x: re.search(r'/ds-([A-Z]{3})/', str(x)).group(1) if re.search(r'/ds-([A-Z]{3})/', str(x)) else None)
pre_df['FileName'] = pre_df['File Path'].apply(lambda x: str(x).split("/")[-1])
pre_df = pre_df.dropna(subset=['Eligible for Diarization', 'Spectral Bandwidth (Hz)'])
pre_df['SNR (dB)'] = pre_df['SNR (dB)'].replace([float('inf'), float('Inf')], 10)
pre_df['Eligible for Diarization'] = pre_df['Eligible for Diarization'].astype(str).str.strip().str.lower().map({
    'yes': 'Eligible', 'true': 'Eligible', '1': 'Eligible',
    'no': 'Not Eligible', 'false': 'Not Eligible', '0': 'Not Eligible'
})
pre_df = pre_df.reset_index(drop=True)
counts = pre_df['Eligible for Diarization'].value_counts()
count_text = f"Eligible: {counts.get('Eligible', 0)} | Not Eligible: {counts.get('Not Eligible', 0)}"
fig_pre = px.scatter(
    pre_df, x=pre_df.index, y="Spectral Bandwidth (Hz)",
    color="Eligible for Diarization",
    color_discrete_map={"Eligible": "green", "Not Eligible": "red"},
    hover_data={"FileName": True},
    title=f"Pre-QC Eligibility\n{count_text}", height=600
)
st.plotly_chart(fig_pre, use_container_width=True)

# Post-QC Plot
st.subheader("Post-QC Overall Eligibility")
post_df = pd.read_excel("Post_qc_summary.xlsx", sheet_name="All_data")
post_df['CityCode'] = post_df['Segment File'].apply(lambda x: re.search(r'ds-([A-Z]{3})', str(x)).group(1) if re.search(r'ds-([A-Z]{3})', str(x)) else None)
post_df['FileName'] = post_df['Segment File'].apply(lambda x: str(x).split("/")[-1])
thresholds = {
    'Signal Energy': (1e-6, 1e-1), 'SPL (dB)': (39, 70), 'LUFS': (-40, 40),
    'RMS Energy': (0.00001, 0.21), 'Relative Amplitude': (0.01, 1.7),
    'Spectral Centroid (Hz)': (900, 5000), 'Spectral Bandwidth (Hz)': (900, 6000),
    'Pitch Mean (Hz)': (250, 400), 'MFCC Mean': (-40, 40), 'MFCC Std Dev': (7, 141)
}
def is_eligible(row):
    for feat, (low, high) in thresholds.items():
        val = row.get(feat)
        if pd.isna(val) or val < low or val > high:
            return 'Not Eligible'
    return 'Eligible'
post_df['Eligible for Research'] = post_df.apply(is_eligible, axis=1)
post_df = post_df.dropna(subset=['Spectral Bandwidth (Hz)'])
post_df = post_df.reset_index(drop=True)
counts_post = post_df['Eligible for Research'].value_counts()
count_text_post = f"Eligible: {counts_post.get('Eligible', 0)} | Not Eligible: {counts_post.get('Not Eligible', 0)}"
fig_post = px.scatter(
    post_df, x=post_df.index, y="Spectral Bandwidth (Hz)",
    color="Eligible for Research",
    color_discrete_map={"Eligible": "green", "Not Eligible": "red"},
    hover_data={"FileName": True},
    title=f"Post-QC Eligibility\n{count_text_post}", height=600
)
st.plotly_chart(fig_post, use_container_width=True)