import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🗺️ Interactive Crime Map")

@st.cache_data
def load_full():
    df = pd.read_csv('data/chicago_crime_cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Latitude', 'Longitude'])
    return df

df_full = load_full()

# Sidebar filters
selected_crimes = st.sidebar.multiselect(
    "Select Crime Types",
    options=sorted(df_full['Primary Type'].unique()),
    default=["HOMICIDE", "BURGLARY"]
)

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2022-12-31"))

# Filter
filtered = df_full[
    (df_full['Primary Type'].isin(selected_crimes)) &
    (df_full['Date'] >= pd.to_datetime(start_date)) &
    (df_full['Date'] <= pd.to_datetime(end_date))
]

st.write(f"Showing **{len(filtered):,}** incidents")

if not filtered.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered,
        get_position='[Longitude, Latitude]',
        get_color='[255, 0, 0, 140]',
        get_radius=100,
        pickable=True
    )
    view_state = pdk.ViewState(
        latitude=filtered['Latitude'].mean(),
        longitude=filtered['Longitude'].mean(),
        zoom=10
    )
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "{Primary Type}\n{Date}"}
    ))
else:
    st.warning("No crimes found for selected filters.")
