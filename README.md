# 🗭 Chicago Crime Data Explorer (2001–2025)

This interactive Streamlit dashboard provides an in-depth look at crime trends in Chicago using data from 2001 to 2025. With intuitive filtering and interactive charts, users can explore how crime has changed over time, across seasons, and under different city mayors.

---

## 📌 Features

### 🔍 Crime Trends

* Visualize how different crime types have evolved year by year.
* Select one or multiple crimes to explore patterns over time.

### 🔒 Arrest Analysis

* View arrest rates for selected crimes over a custom year range.
* Compare arrest performance **pre- and post-COVID-19** with visual benchmarks.
* Explore arrest distribution via dynamic pie and bar charts.

### 🌦️ Seasonal Crime Trends

* See how crime shifts by **season (Winter, Spring, Summer, Fall)** and **month**.
* Get insight into the **most common crime per season** via tooltip summaries.
* Toggle between monthly line charts and seasonal bar charts.

### 🏩 Crime by Mayor

* Analyze total crime counts under mayors **Daley, Emanuel, and Lightfoot**.
* View top 3 crimes per mayor and compare **violent vs. non-violent crime**.
* Compare annual averages and total counts across administrations.

---

## 📁 Project Structure

```
chicago_crime_dashboard/
├── data/
│   ├── raw/
│   │   └── chicago_crime_2001_2025.csv
│   └── crime_pivot.csv
├── pages/
│   ├── trends.py
│   └── mayor.py
|   |__ overview.py
|   |__ maps.py
├── app.py
├── README.md
└── requirements.txt
```

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/infinityseifer/chicago_crime_dashboard.git
cd chicago_crime_dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard

```bash
streamlit run app.py
```

---

## 📊 Data Source

* Data provided by the [City of Chicago’s public crime data portal](https://data.cityofchicago.org/).
* Covers crimes from **2001 through 2025**, including primary type, arrest status, location, and more.

---

## 📌 Requirements

* Python 3.8+
* Streamlit
* pandas
* plotly

Install with:

```bash
pip install streamlit pandas plotly
```

---

## ✍️ Author

**Arnell Seifer**
[GitHub Portfolio](https://github.com/yourusername) | [Tableau Public](https://public.tableau.com/profile/yourprofile)

---

## 📃 License

This project is open-source and free to use under the [MIT License](LICENSE).
