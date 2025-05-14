#!/usr/bin/env python3
"""
📄 COVID-19 Global Data Tracker

This script/notebook walks through:
 1️⃣ Data Collection & Loading
 2️⃣ Data Cleaning & Preparation
 3️⃣ Exploratory Data Analysis (EDA)
 4️⃣ Vaccination Progress Analysis
 5️⃣ Choropleth Map Visualization
 6️⃣ Insights & Reporting

💾 **Data Source (Auto-load with Fallback)**:
  - Primary: Our World in Data CSV URL
    https://covid.ourworldindata.org/data/owid-covid-data.csv
  - Fallback: Local `owid-covid-data.csv` in working directory

🔧 **Setup & Environment**:
 1. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```
 2. Install dependencies:
    ```bash
    pip install pandas matplotlib seaborn geopandas contextily requests
    ```
 3. (Optional) If using Jupyter:
    ```bash
    pip install jupyterlab
    jupyter lab
    ```

🚀 **How to Run**:
  - **As Python Script**:
    ```bash
    python covid_tracker.py
    ```
  - **In Jupyter Notebook**:
    1. Open this file as a notebook or copy cells.
    2. Run cells to load and visualize inline.

🔍 **Navigation**:
  - Jump to numbered sections via comments (e.g., `# --- 3. FILTERS ---`).

🔑 **ISO Codes**:
  - 3-letter ISO (`iso_code`) used for consistent merges with GeoPandas.

✅ **Follows Project Objectives**:
  - Import & clean data
  - Analyze time trends (cases, deaths, vaccinations)
  - Compare metrics across countries
  - Visualize charts & maps
  - Produce visuals for notebook or PDF report
"""

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as ctx

# --- 1. DATA COLLECTION & LOADING ---
DATA_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
LOCAL_PATH = "owid-covid-data.csv"

def load_data():
    """Attempt to load remote data with fallback to local file."""
    try:
        print("Downloading data from OWID...")
        resp = requests.get(DATA_URL, timeout=10)
        resp.raise_for_status()
        with open(LOCAL_PATH, 'wb') as f:
            f.write(resp.content)
        print(f"Saved remote CSV to {LOCAL_PATH}")
        df = pd.read_csv(LOCAL_PATH, parse_dates=['date'], low_memory=False)
    except Exception as e:
        print(f"Remote load failed ({e}). Trying local file...")
        if os.path.exists(LOCAL_PATH):
            df = pd.read_csv(LOCAL_PATH, parse_dates=['date'], low_memory=False)
        else:
            raise FileNotFoundError(
                f"Local file {LOCAL_PATH} not found. Download manually from {DATA_URL}"
            )
    return df

# Load the data
df = load_data()
print(f"Loaded {len(df)} rows with columns: {df.columns.tolist()}")

# --- 2. DATA CLEANING & PREPARATION ---
cols = [
    'iso_code', 'location', 'date',
    'total_cases', 'new_cases',
    'total_deaths', 'new_deaths',
    'total_vaccinations', 'people_vaccinated_per_hundred'
]
available = [c for c in cols if c in df.columns]
# Subset and drop critical missing values
df = df[available].dropna(subset=['date', 'location'])
# Sort & forward-fill per country
df = df.sort_values(['location', 'date'])
df = df.groupby('location').apply(lambda g: g.fillna(method='ffill')).reset_index(drop=True)

# --- 3. FILTERS: Countries & Date Range ---
countries = ['United States', 'India', 'Brazil']  # customize
start_date = pd.to_datetime('2021-01-01')
end_date = df['date'].max()
mask = (
    df['location'].isin(countries) &
    (df['date'] >= start_date) &
    (df['date'] <= end_date)
)
df_filt = df.loc[mask]
print(f"Filtering {len(countries)} countries from {start_date.date()} to {end_date.date()}")

# --- 4. EXPLORATORY DATA ANALYSIS (EDA) ---
sns.set_style("whitegrid")
plt.rcParams.update({'figure.figsize': (10,6), 'axes.titlesize':14})

def plot_time_series(data, metric, title):
    """Line chart for specified metric and countries."""
    plt.figure()
    for loc, grp in data.groupby('location'):
        plt.plot(grp['date'], grp[metric], label=loc)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_time_series(df_filt, 'total_cases', 'Total Cases Over Time')
plot_time_series(df_filt, 'total_deaths', 'Total Deaths Over Time')

# --- 5. VACCINATION PROGRESS ANALYSIS ---
def plot_dual_axis(data, m1, m2, name1, name2):
    fig, ax1 = plt.subplots()
    for loc, grp in data.groupby('location'):
        ax1.plot(grp['date'], grp[m1], label=f"{loc} {name1}")
    ax1.set_xlabel('Date'); ax1.set_ylabel(name1)
    ax2 = ax1.twinx()
    for loc, grp in data.groupby('location'):
        ax2.plot(grp['date'], grp[m2], linestyle='--', label=f"{loc} {name2}")
    ax2.set_ylabel(name2)
    plt.title(f"{name1} & {name2}")
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.tight_layout()
    plt.show()

if 'total_vaccinations' in df_filt.columns:
    plot_dual_axis(df_filt, 'new_cases', 'total_vaccinations', 'Daily New Cases', 'Total Vaccinations')

# --- 6. CHOROPLETH MAP VISUALIZATION ---
latest = df.groupby('location').apply(lambda g: g[g['date'] == g['date'].max()])
latest = latest.set_index('iso_code')
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
map_df = world.merge(latest.reset_index(), left_on='iso_a3', right_on='iso_code', how='left')
fig, ax = plt.subplots(figsize=(12,6))
map_df.plot(
    column='total_cases', cmap='OrRd', legend=True,
    legend_kwds={'label': 'Total Cases', 'shrink': 0.5}, ax=ax
)
ax.set_title('Global COVID-19 Total Cases')
ax.axis('off')
ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)
plt.tight_layout()
plt.show()

# --- 7. INSIGHTS & REPORTING ---
latest['death_rate'] = latest['total_deaths'] / latest['total_cases']
top5 = latest.sort_values('total_cases', ascending=False).head(5)
print("Top 5 countries by total cases and death rates:")
print(top5[['location', 'total_cases', 'total_deaths', 'death_rate']])

def plot_death_vs_infection(data):
    """Plot death and infection rates on the same graph."""
    plt.figure()
    for loc, grp in data.groupby('location'):
        plt.plot(grp['date'], grp['new_cases'], label=f"{loc} New Cases")
        plt.plot(grp['date'], grp['new_deaths'], linestyle='--', label=f"{loc} New Deaths")
    plt.title("New Cases vs New Deaths Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.show()

def navigation_menu():
    """Menu-driven navigation for different graphs."""
    while True:
        print("\nGraph Navigation Menu:")
        print("1. Total Cases Over Time")
        print("2. Total Deaths Over Time")
        print("3. New Cases vs Total Vaccinations")
        print("4. New Cases vs New Deaths")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            plot_time_series(df_filt, 'total_cases', 'Total Cases Over Time')
        elif choice == '2':
            plot_time_series(df_filt, 'total_deaths', 'Total Deaths Over Time')
        elif choice == '3' and 'total_vaccinations' in df_filt.columns:
            plot_dual_axis(df_filt, 'new_cases', 'total_vaccinations', 'Daily New Cases', 'Total Vaccinations')
        elif choice == '4':
            plot_death_vs_infection(df_filt)
        elif choice == '5':
            print("Exiting navigation menu.")
            break
        else:
            print("Invalid choice. Please try again.")

# Call the navigation menu to start
navigation_menu()
# End of COVID-19 Global Data Tracker Script
