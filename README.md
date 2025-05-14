# COVID-19 Global Data Tracker

A Python script/notebook for importing, cleaning, analyzing, and visualizing global COVID-19 data. It walks through:

1. **Data Collection & Loading**
2. **Data Cleaning & Preparation**
3. **Exploratory Data Analysis (EDA)**
4. **Vaccination Progress Analysis**
5. **Choropleth Map Visualization**
6. **Insights & Reporting**

---

##  Data Source (Auto-load with Fallback)

* **Primary**: Our World in Data CSV (auto-downloaded):

  > `https://covid.ourworldindata.org/data/owid-covid-data.csv`

* **Fallback**: Local file `owid-covid-data.csv` in working directory

## Setup & Environment

1. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   # macOS/Linux:
   source venv/bin/activate
   # Windows:
   venv\\Scripts\\activate
   ```
2. **Install dependencies**

   ```bash
   pip install pandas matplotlib seaborn geopandas contextily requests
   ```
3. *(Optional)* **Jupyter**

   ```bash
   pip install jupyterlab
   jupyter lab
   ```

##  How to Run

* **As Python script**

  ```bash
  python covid_tracker.py
  ```

  This will:

  * Download (or load) the dataset
  * Clean and prepare data
  * Generate time-series plots, dual-axis charts, and a choropleth map
  * Print top 5 countries by cases and death rates

* **In Jupyter Notebook**

  1. Rename or open this file as `covid_tracker.ipynb`
  2. Copy code cells and run sequentially to view inline visualizations

##  Navigation

* Sections are delineated by comments, e.g.:

  ```python
  # --- 3. FILTERS: Countries & Date Range ---
  ```
* Jump to any numbered section to focus on that step.

##  ISO Codes

* Uses 3-letter ISO codes (`iso_code`) to merge with GeoPandas world geometries.

##  Features & Objectives

* **Import & clean** real-world COVID-19 data
* **Analyze time trends**: total & new cases, deaths, vaccinations
* **Compare metrics** across selected countries
* **Visualize** with line charts, dual-axis plots, and choropleth maps
* **Summarize insights**: death rates and top-performers
* **Produce assets**: script-based PNGs or inline notebook charts for reports

---

##  Further Customization

* Change the `countries` list to any set of countries
* Adjust `start_date` or date filters to focus on different periods
* Add correlation heatmaps or additional metrics as needed

---
