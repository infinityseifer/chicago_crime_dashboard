import streamlit as st
import pandas as pd 
import plotly.express as px

st.title("🏛️ Mayoral Crime Analysis")

@st.cache_data
def load_summary():
    df = pd.read_csv('../chicago_crime_dashboard/data/crime_pivot.csv', index_col=0)
    df.index = df.index.astype(str)
    return df

@st.cache_data
def load_full_data():
    df = pd.read_csv('data/chicago_crime_cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Arrest'] = df['Arrest'].astype(str)
    return df

# Load data
crime_pivot = load_summary()
df_full = load_full_data()

# Sidebar filters
crime_options = sorted(df_full['Primary Type'].dropna().unique())
selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_options, default=["HOMICIDE", "BATTERY", "ROBBERY"])

st.subheader("🏛️ Crime Totals by Mayor Term")

mayor_terms = {
    "Daley (2001–2011)": ("2001-01-01", "2011-05-15"),
    "Emanuel (2011–2019)": ("2011-05-16", "2019-05-19"),
    "Lightfoot (2019–2023)": ("2019-05-20", "2023-05-15"),
    "Johnson (2023–Present)": ("2023-05-16", "2025-12-31")  # Assuming current date for Johnson
}

# Display top 3 crimes per mayor
st.subheader("🥇 Top 3 Crimes by Mayor Term")

top_crimes_data = []

for mayor, (start, end) in mayor_terms.items():
    term_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'] >= pd.to_datetime(start)) &
        (df_full['Date'] <= pd.to_datetime(end))
    ]

    if term_df.empty:
        continue

    top_crimes = (
        term_df['Primary Type']
        .value_counts()
        .nlargest(3)
        .reset_index()
    )
    top_crimes.columns = ['Primary Type', 'Frequency']
    top_crimes["Mayor"] = mayor
    top_crimes["Rank"] = [1, 2, 3]
    top_crimes_data.append(top_crimes)

if top_crimes_data:
    top_crimes_df = pd.concat(top_crimes_data, ignore_index=True)

    st.dataframe(top_crimes_df[['Mayor', 'Rank', 'Primary Type', 'Frequency']])

    fig_top3 = px.bar(
        top_crimes_df,
        x='Mayor',
        y='Frequency',
        color='Primary Type',
        barmode='group',
        title="Top 3 Crimes per Mayor (Filtered Crimes)",
        text='Frequency'
    )
    fig_top3.update_layout(xaxis_tickangle=-30, yaxis_title="Crime Count")
    st.plotly_chart(fig_top3, use_container_width=True, key="mayor_top3")
else:
    st.info("No crime data available for selected mayors and filters.")

# Mayor-level total and violent crime metrics
st.subheader("📊 Overall Crime Metrics by Mayor")

selected_mayors = st.multiselect(
    "Select Mayors to Compare",
    list(mayor_terms.keys()),
    default=list(mayor_terms.keys())
)

violent_crimes = {
    "HOMICIDE", "CRIM SEXUAL ASSAULT", "ROBBERY", "AGGRAVATED ASSAULT", "BATTERY",
    "HUMAN TRAFFICKING", "KIDNAPPING", "ARSON"
}

mayor_data = []

for mayor, (start, end) in mayor_terms.items():
    if mayor not in selected_mayors:
        continue

    term_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'] >= pd.to_datetime(start)) &
        (df_full['Date'] <= pd.to_datetime(end))
    ]

    if term_df.empty:
        continue

    total_crimes = term_df.shape[0]
    years_in_office = pd.to_datetime(end).year - pd.to_datetime(start).year + 1
    avg_per_year = total_crimes / years_in_office if years_in_office > 0 else 0

    violent = term_df[term_df['Primary Type'].isin(violent_crimes)].shape[0]
    non_violent = total_crimes - violent

    mayor_data.append({
        "Mayor": mayor,
        "Total Crimes": total_crimes,
        "Avg per Year": round(avg_per_year),
        "Violent Crimes": violent,
        "Non-Violent Crimes": non_violent
    })

if mayor_data:
    mayor_df = pd.DataFrame(mayor_data)
    st.dataframe(mayor_df)

    fig_total = px.bar(
        mayor_df,
        x="Mayor",
        y="Total Crimes",
        text="Total Crimes",
        title="Total Crimes During Mayor Terms",
        labels={"Total Crimes": "Crime Count"}
    )
    fig_total.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_total.update_layout(xaxis_tickangle=-30, yaxis_tickformat=",")
    st.plotly_chart(fig_total, use_container_width=True, key="mayor_total")

    fig_avg = px.bar(
        mayor_df,
        x="Mayor",
        y="Avg per Year",
        text="Avg per Year",
        title="Average Crimes per Year by Mayor",
        labels={"Avg per Year": "Average Per Year"}
    )
    fig_avg.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_avg.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_avg, use_container_width=True, key="mayor_avg")

    stacked_df = mayor_df.melt(
        id_vars="Mayor",
        value_vars=["Violent Crimes", "Non-Violent Crimes"],
        var_name="Crime Type",
        value_name="Count"
    )

    fig_stack = px.bar(
        stacked_df,
        x="Mayor",
        y="Count",
        color="Crime Type",
        barmode="stack",
        title="Violent vs Non-Violent Crime per Mayor",
        labels={"Count": "Crime Count"}
    )
    fig_stack.update_layout(xaxis_tickangle=-30, yaxis_tickformat=",")
    st.plotly_chart(fig_stack, use_container_width=True, key="mayor_violent")
else:
    st.info("No comparative data for selected mayors.")
