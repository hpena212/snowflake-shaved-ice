# ICPE 2026 Data Challenge - Shaved Ice Dataset Analysis

**Project Deadline:** January 28, 2026  
**Status:** Ready for data exploration

## Overview
This project analyzes Snowflake's "Shaved Ice" VM demand dataset for the ICPE 2026 Data Challenge. We use **dbt + DuckDB** for data transformations and **Python** for forecasting analysis.

## Tech Stack
- **Data Engineering:** dbt-duckdb (SQL transformations)
- **Database:** DuckDB (local analytical database)
- **Analysis:** Python (pandas, statsmodels)
- **Visualization:** matplotlib, seaborn

## Quick Start

> **Important:** All commands should be run from the project root directory:
> `c:\Users\hecto\OneDrive\Documents\School\Data Science\AntiGravity\Python Projects\Shaved Ice`

### Step 1: Open Terminal in Project Folder
1. Open VS Code or your terminal
2. Navigate to the project:
   ```powershell
   cd "c:\Users\hecto\OneDrive\Documents\School\Data Science\AntiGravity\Python Projects\Shaved Ice"
   ```

### Step 2: Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
You'll see `(.venv)` in your prompt when activated.

### Step 3: Download Dataset
```powershell
cd data\raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ..\..
```

### Step 4: Run dbt Transformations
```powershell
dbt run --profiles-dir .
```
This creates clean tables in `data/processed/shaved_ice.duckdb`.

### Step 5: Start Jupyter
```powershell
jupyter notebook
```
Open `notebooks/01_data_exploration.ipynb` from the browser.

## Project Structure
```
Shaved Ice/
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

## Workflow
1. **dbt run** → Creates clean tables in DuckDB
2. **Python** → Loads tables for forecasting analysis
3. **Jupyter** → Interactive exploration and visualization

```python
# Load dbt output in Python
from src.duckdb_loader import load_mart_data
df = load_mart_data()  # Returns clean pandas DataFrame
```

## Research Questions
1. Can simple moving averages effectively forecast VM demand?
2. What safety stock levels minimize over/under-provisioning?
3. How do demand patterns vary by day of week?

## Key dbt Commands
```powershell
# Run all models
dbt run --profiles-dir .

# Run specific model
dbt run --select mart_forecast_input --profiles-dir .

# Test data quality
dbt test --profiles-dir .

# Generate documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

## Checkpoints
- [x] Project setup complete
- [x] dbt pipeline configured
- [ ] Dataset downloaded
- [ ] dbt models tested
- [ ] Exploratory data analysis
- [ ] Forecasting models
- [ ] Paper visualizations

## Contact
ICPE 2026 Data Challenge submission
