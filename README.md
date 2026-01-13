# ICPE 2026 Data Challenge - Shaved Ice Dataset Analysis

**Deadline:** January 28, 2026  
**Status:** Ready for data exploration

## Overview
This project analyzes Snowflake's "Shaved Ice" VM demand dataset for the ICPE 2026 Data Challenge. It uses **dbt + DuckDB** for data transformations and **Python** for forecasting analysis.

## Tech Stack
- **Data Engineering:** dbt-duckdb (SQL transformations)
- **Database:** DuckDB (local analytical database)
- **Analysis:** Python (pandas, statsmodels)
- **Visualization:** matplotlib, seaborn

## Getting Started

> **Note:** Run all commands from the project root directory.

### 1. Clone and Navigate
```powershell
git clone https://github.com/hpena212/snowflake-shaved-ice.git
cd snowflake-shaved-ice
```

### 2. Set Up Your Environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
You'll see `(.venv)` in your prompt when the environment is active.

### 3. Download the Dataset
```powershell
cd data\raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ..\..
```

### 4. Run dbt Transformations
```powershell
dbt run --profiles-dir .
```
This creates clean tables in `data/processed/shaved_ice.duckdb`.

### 5. Launch Jupyter
```powershell
jupyter notebook
```
Open `notebooks/01_data_exploration.ipynb` from your browser.

## Project Structure
```
snowflake-shaved-ice/
├── dbt_project.yml           # dbt configuration
├── profiles.yml              # DuckDB connection
├── sql/models/               # dbt SQL models
│   ├── staging/              # Raw data loading
│   ├── intermediate/         # Daily aggregations
│   └── marts/                # Analysis-ready tables
├── src/                      # Python modules
│   └── duckdb_loader.py      # Load dbt output → pandas
├── notebooks/                # Jupyter analysis
└── data/
    ├── raw/                  # Downloaded dataset
    └── processed/            # DuckDB database
```

## How It Works
1. **dbt run** → Creates clean tables in DuckDB
2. **Python** → Loads tables for forecasting analysis
3. **Jupyter** → Interactive exploration and visualization

```python
# Load dbt output in your Python scripts
from src.duckdb_loader import load_mart_data
df = load_mart_data()  # Returns a clean pandas DataFrame
```

## Research Questions
1. Can simple moving averages effectively forecast VM demand?
2. What safety stock levels minimize over/under-provisioning?
3. How do demand patterns vary by day of week?

## Useful dbt Commands
```powershell
# Run all models
dbt run --profiles-dir .

# Run a specific model
dbt run --select mart_forecast_input --profiles-dir .

# Test data quality
dbt test --profiles-dir .

# Generate and view documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

## Progress
- [x] Project setup
- [x] dbt pipeline configured
- [x] Dataset downloaded
- [x] dbt models tested
- [x] Exploratory data analysis
- [x] Forecasting models
- [x] Paper visualizations

## Links
- [ICPE 2026 Data Challenge](https://icpe2026.spec.org/tracks-and-submissions/data-challenge-track/)
- [Shaved Ice Dataset (Snowflake Labs)](https://github.com/Snowflake-Labs/shavedice-dataset)
