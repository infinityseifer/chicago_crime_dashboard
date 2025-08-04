import streamlit as st

st.set_page_config(page_title="Chicago Crime Dashboard", layout="wide")

st.title("👋 Welcome to the Chicago Crime Dashboard")
st.markdown("""
Explore Chicago crime data (2001–2025) by navigating to the pages in the sidebar:
- 📊 Overview: View crime totals and bar charts
- 📈 Trends: See how crime types change over time
- 🗺️ Map: Explore crime locations on an interactive map
""")

st.markdown("""
🔍 About This Dashboard
Welcome to the Chicago Crime Data Explorer, an interactive dashboard designed 
to help you analyze crime trends across Chicago from 2001 to 2025. This tool is 
powered by publicly available data from the City of Chicago and allows users to 
explore crime patterns over time, across seasons, and under different mayoral administrations.

- 📊 What You Can Expect
- 📈 Crime Trends
Visualize how different types of crimes have increased or decreased across years.

- 🔒 Arrest Analysis
Compare arrest rates for selected crimes, including differences before and after COVID-19, with benchmark comparisons.

- 🌦️ Seasonal Trends
See how crime patterns shift by season and month, with tooltips showing the most common crimes per season.

- 🏛️ Crime by Mayor
Analyze how crime counts and types varied under the leadership of Mayors Daley, Emanuel, and Lightfoot, including violent vs. non-violent breakdowns.

⚙️ Filters & Features
- Select specific crime types and years

- Compare arrest rates

- Identify top 3 crimes per mayor

- View metrics such as average annual crime counts

- Interactive charts powered by Plotly

""")

# Footer
st.markdown("""
&copy; 2025 Chicago Crime Dashboard. All rights reserved. A. Seifer is licensed under the [MIT License](https://opensource.org/license/mit/).
""")