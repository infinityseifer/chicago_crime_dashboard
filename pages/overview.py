import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Crime Overview")

@st.cache_data
def load_summary():
    df = pd.read_csv('data/crime_pivot.csv', index_col=0)
    df.index = df.index.astype(str)
    return df

crime_pivot = load_summary()

# Sidebar filters
filter_years = st.sidebar.radio(
    "Select Time Period",
    ["All Years", "Pre-COVID (2001–2019)", "Post-COVID (2020–2025)"]
)

# Filter year range based on selection
if filter_years == "Pre-COVID (2001–2019)":
    year_options = [y for y in crime_pivot.index if int(y) <= 2019]
elif filter_years == "Post-COVID (2020–2025)":
    year_options = [y for y in crime_pivot.index if int(y) >= 2020]
else:
    year_options = crime_pivot.index.tolist()

selected_year = st.sidebar.selectbox("Select Year", year_options)

# Crime type filter with Select All
crime_options = sorted(crime_pivot.columns)
select_all = st.sidebar.checkbox("Select All Crime Types", value=True)

if select_all:
    selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_options, default=crime_options)
else:
    selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_options, default=["HOMICIDE", "BURGLARY"])

# Filtered Data
year_df = crime_pivot.loc[selected_year, selected_crimes].sort_values(ascending=False).reset_index()
year_df.columns = ['Primary Type', 'Count']

st.metric("Total Selected Crimes", value=f"{year_df['Count'].sum():,}")

fig1 = px.bar(
    year_df,
    x='Primary Type',
    y='Count',
    title=f"Selected Crimes in {selected_year} ({filter_years})"
)
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)








# --------------------------
# Pre vs Post-COVID Summary
# --------------------------

st.subheader("🧮 Pre vs Post-COVID Crime Totals")

# Separate the pivot table
pre_years = [y for y in crime_pivot.index if int(y) <= 2019]
post_years = [y for y in crime_pivot.index if int(y) >= 2020]

# Sum totals for selected crimes
pre_total = crime_pivot.loc[pre_years, selected_crimes].sum().sum()
post_total = crime_pivot.loc[post_years, selected_crimes].sum().sum()

# Prepare bar chart data
summary_df = pd.DataFrame({
    'Period': ['Pre-COVID (2001–2019)', 'Post-COVID (2020–2025)'],
    'Total Crimes': [pre_total, post_total]
})

fig_summary = px.bar(
    summary_df,
    x='Period',
    y='Total Crimes',
    text='Total Crimes',
    title=f"Total {', '.join(selected_crimes)} Crimes: Pre vs Post-COVID",
    labels={'Total Crimes': 'Crime Count'}
)
fig_summary.update_traces(texttemplate='%{text:,}', textposition='outside')
fig_summary.update_layout(yaxis_tickformat=',', yaxis_title='Crime Count')

st.plotly_chart(fig_summary, use_container_width=True)
