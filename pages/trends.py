import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Crime Trends Over Time")

@st.cache_data
def load_summary():
    df = pd.read_csv('../chicago_crime_dashboard/data/crime_pivot.csv', index_col=0)
    df.index = df.index.astype(str)
    return df

@st.cache_data
def load_full_data():
    df = pd.read_csv('data/raw/chicago_crime_2001_2025.csv')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Arrest'] = df['Arrest'].astype(str)
    return df

crime_pivot = load_summary()
df_full = load_full_data()

# Sidebar filters
crime_options = sorted(crime_pivot.columns)
select_all = st.sidebar.checkbox("Select All Crime Types", value=True)

if select_all:
    selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_options, default=crime_options)
else:
    selected_crimes = st.sidebar.multiselect("Select Crime Types", crime_options, default=["HOMICIDE", "BURGLARY"])

start_year = st.sidebar.selectbox("Start Year", sorted(df_full['Date'].dt.year.dropna().unique()), index=21)
end_year = st.sidebar.selectbox("End Year", sorted(df_full['Date'].dt.year.dropna().unique()), index=24)

# Tabs: Crime Trends, Arrest Rates, Seasonal Trends
# Tabs: Crime Trends, Arrest Rates, Seasonal Trends, Mayor Analysis
tab1, tab2, tab3 = st.tabs([
    "📈 Crime Trends", 
    "🔒 Arrest Rates", 
    "🌦️ Seasonal Trends"
])


with tab1:
    if selected_crimes:
        fig = px.line(
            crime_pivot[selected_crimes],
            labels={'value': 'Crime Count', 'index': 'Year', 'variable': 'Primary Type'},
            title="Crime Trends Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one crime type.")

with tab2:
    st.subheader("Arrest Distribution & Rates")

    # Arrest Pie Chart (Filtered by selected year range)
    filtered_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'].dt.year >= start_year) &
        (df_full['Date'].dt.year <= end_year)
    ].copy()

    filtered_df['Arrest'] = filtered_df['Arrest'].astype(str).map({'True': True, 'False': False})

    arrest_counts = filtered_df['Arrest'].value_counts().reset_index()
    arrest_counts.columns = ['Arrested', 'Count']

    total_crimes = filtered_df.shape[0]
    arrests = filtered_df['Arrest'].sum()
    overall_rate = (arrests / total_crimes) * 100 if total_crimes > 0 else 0

    if not arrest_counts.empty:
        fig_pie = px.pie(
            arrest_counts,
            names='Arrested',
            values='Count',
            title=f"Arrest Outcomes for Selected Crimes ({start_year}–{end_year})",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data found for selected filters.")

    # --- Pre/Post-COVID Data (Standalone)
    pre_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'] < pd.to_datetime("2020-01-01"))
    ].copy()

    post_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'] >= pd.to_datetime("2020-01-01"))
    ].copy()

    pre_df['Arrest'] = pre_df['Arrest'].astype(str).map({'True': True, 'False': False})
    post_df['Arrest'] = post_df['Arrest'].astype(str).map({'True': True, 'False': False})

    def arrest_rate_chart(df, label, key, benchmark_rate=None):
        if df.empty:
            return None
        rates = df.groupby('Primary Type')['Arrest'].agg(['count', 'sum']).rename(columns={'count': 'Total', 'sum': 'Arrests'})
        rates['Arrest Rate (%)'] = (rates['Arrests'] / rates['Total']) * 100
        rates = rates.reset_index()

        fig = px.bar(
            rates,
            x='Primary Type',
            y='Arrest Rate (%)',
            text='Arrest Rate (%)',
            title=f"Arrest Rate by Crime Type — {label}",
            labels={'Arrest Rate (%)': 'Arrest Rate (%)'},
            range_y=[0, 100]
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(xaxis_tickangle=-45)

        if benchmark_rate is not None:
            fig.add_shape(
                type='line',
                x0=-0.5,
                x1=len(rates['Primary Type']) - 0.5,
                y0=benchmark_rate,
                y1=benchmark_rate,
                line=dict(color='red', dash='dash'),
            )
            fig.add_annotation(
                x=len(rates['Primary Type']) - 1,
                y=benchmark_rate,
                text=f"Filtered Avg: {benchmark_rate:.1f}%",
                showarrow=False,
                yshift=10,
                font=dict(color='red')
            )

        return fig

    st.subheader("Pre-COVID Arrest Rates (2001–2019)")
    fig_pre = arrest_rate_chart(pre_df, "Pre-COVID (2001–2019)", key="arrest_rate_pre", benchmark_rate=overall_rate)
    if fig_pre:
        st.plotly_chart(fig_pre, use_container_width=True)
    else:
        st.info("No data for Pre-COVID period.")

    st.subheader("Post-COVID Arrest Rates (2020–2025)")
    fig_post = arrest_rate_chart(post_df, "Post-COVID (2020–2025)", key="arrest_rate_post", benchmark_rate=overall_rate)
    if fig_post:
        st.plotly_chart(fig_post, use_container_width=True)
    else:
        st.info("No data for Post-COVID period.")

with tab3:
    st.subheader("📅 Seasonal Crime Trends")

    # Add month & season columns if not already added
    df_full['Month'] = df_full['Date'].dt.month
    df_full['Month Name'] = df_full['Date'].dt.strftime('%B')

    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    df_full['Season'] = df_full['Month'].apply(get_season)

    # Filter using the selected year and crime type
    filtered_df = df_full[
        (df_full['Primary Type'].isin(selected_crimes)) &
        (df_full['Date'].dt.year >= start_year) &
        (df_full['Date'].dt.year <= end_year)
    ]

    # --- 🧮 Show seasonal metrics
    seasonal_totals = (
        filtered_df.groupby('Season')
        .size()
        .reindex(['Winter', 'Spring', 'Summer', 'Fall'])
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("❄️ Winter", f"{seasonal_totals['Winter']:,}" if pd.notna(seasonal_totals['Winter']) else "0")
    col2.metric("🌱 Spring", f"{seasonal_totals['Spring']:,}" if pd.notna(seasonal_totals['Spring']) else "0")
    col3.metric("☀️ Summer", f"{seasonal_totals['Summer']:,}" if pd.notna(seasonal_totals['Summer']) else "0")
    col4.metric("🍁 Fall", f"{seasonal_totals['Fall']:,}" if pd.notna(seasonal_totals['Fall']) else "0")

    # --- 🔘 Toggle chart type
    chart_type = st.radio(
        "Select Trend Visualization",
        ["📈 Monthly Line Chart", "📊 Seasonal Bar Chart"],
        horizontal=True
    )

    if chart_type == "📈 Monthly Line Chart":
        monthly_counts = (
            filtered_df.groupby(['Month Name', 'Primary Type'])
            .size()
            .reset_index(name='Count')
        )

        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly_counts['Month Name'] = pd.Categorical(monthly_counts['Month Name'], categories=month_order, ordered=True)
        monthly_counts = monthly_counts.sort_values('Month Name')

        fig_month = px.line(
            monthly_counts,
            x='Month Name',
            y='Count',
            color='Primary Type',
            markers=True,
            title=f"Monthly Crime Trends ({start_year}–{end_year})"
        )
        fig_month.update_layout(xaxis_title="Month", yaxis_title="Crime Count")
        st.plotly_chart(fig_month, use_container_width=True)

    elif chart_type == "📊 Seasonal Bar Chart":
        seasonal_counts = (
            filtered_df.groupby(['Season', 'Primary Type'])
            .size()
            .reset_index(name='Count')
        )
        seasonal_counts['Season'] = pd.Categorical(seasonal_counts['Season'],
                                                categories=['Winter', 'Spring', 'Summer', 'Fall'],
                                                ordered=True)
        seasonal_counts = seasonal_counts.sort_values('Season')

        # 🔍 Find most common crime per season
        if seasonal_counts.empty:
            st.warning("No seasonal data available for the selected year and crimes.")
        else:
            # Get top crime per season safely
            top_crimes_list = []
            for season in ['Winter', 'Spring', 'Summer', 'Fall']:
                season_data = seasonal_counts[seasonal_counts['Season'] == season]
                if not season_data.empty:
                    top_row = season_data.loc[season_data['Count'].idxmax()]
                    top_crimes_list.append(top_row)

            # Convert to DataFrame
            top_crimes = pd.DataFrame(top_crimes_list)



            # 🧠 Tooltip summary
            tooltip_text = "Most Common Crimes by Season:\n"
            for _, row in top_crimes.iterrows():
                tooltip_text += f"• {row['Season']}: {row['Primary Type']} ({row['Count']:,})\n"

            st.caption("🛈 Hover for season's top crime:")
            st.info(tooltip_text.strip())

            # 📊 Plot the grouped bar chart
            fig_season = px.bar(
                seasonal_counts,
                x='Season',
                y='Count',
                color='Primary Type',
                barmode='group',
                title=f"Seasonal Crime Totals ({start_year}–{end_year})"
            )
            fig_season.update_layout(xaxis_title="Season", yaxis_title="Crime Count")
            st.plotly_chart(fig_season, use_container_width=True, key="seasonal_bar_chart")

