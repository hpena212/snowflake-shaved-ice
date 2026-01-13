# 🚀 ICPE 2026: Project Workflow Guide

This document is your definitive "Source of Truth" for the development lifecycle of the Shaved Ice project. It covers everything from environment setup to dbt modeling and GitHub synchronization.

---

## 🧭 Project Compass (Directory Map)
Use this to find your way around if you've been away from the project:
- `data/` : All raw data (ignored by Git) and the processed DuckDB database.
- `notebooks/` : Interactive data exploration and modeling experiments.
- `sql/` : The dbt project. Contains `models`, `seeds`, and `tests`.
- `src/` : Custom Python utility library (`utils.py`, `plotting.py`, `duckdb_loader.py`).
- `target/` : dbt compilation artifacts and generated documentation.

---

## 🛠️ First-Time / Re-entry Setup
If you are moving to a new machine or haven't worked on this in months:

1.  **Clone and Navigate:**
    `cd "Shaved Ice"`
2.  **Create & Activate Virtual Environment:**
    `python -m venv .venv`
    `.\.venv\Scripts\Activate.ps1`
3.  **Install Dependencies:**
    `pip install -r requirements.txt` (or ensure dbt-duckdb, pandas, matplotlib, seaborn are installed)
4.  **Restore Data:** 
    Ensure `shaved_ice_data.csv` is in `data/` and run:
    `dbt seed` (if using seeds) or `dbt run` to rebuild the DuckDB database.

---

## 📅 The Daily Developer Loop
Follow these steps every time you start your work session:

1.  **Activate Environment:**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
2.  **Verify Data State:**
    Check if your `data/processed/shaved_ice.duckdb` exists and is up to date.
3.  **Run dbt Fresh (Optional):**
    ```powershell
    .\.venv\Scripts\dbt run --profiles-dir .
    ```

---

## 🛠️ Phase 1: SQL & dbt Workflow
Use this when you need to add new metrics, filter data, or aggregate to new granularities.

### 1. Add/Modify a Model
- Create or edit a file in `sql/models/marts/` (e.g., `mart_new_metric.sql`).
- Always use the `{{ ref('...') }}` function to depend on other models.
- **Tip:** Keep logic clean in Common Table Expressions (CTEs).

### 2. Build and Test
- **Compile only** (to check syntax):
  ```powershell
  .\.venv\Scripts\dbt compile --profiles-dir .
  ```
- **Run specific model** (Fastest way):
  ```powershell
  .\.venv\Scripts\dbt run --select mart_stockout_events --profiles-dir .
  ```
- **Run everything:**
  ```powershell
  .\.venv\Scripts\dbt run --profiles-dir .
  ```

---

## 🐍 Phase 2: Python & Jupyter Integration
Use this to bring your materialized dbt tables into your analysis environment.

### 1. Connecting to DuckDB
**Inside a Notebook:**
Always use the relative path `../data/processed/shaved_ice.duckdb`. 

**Crucial Tip:** Use `read_only=True` in your connection string to prevent locking the database. This allows you to run `dbt docs generate` or `dbt compile` while your notebook is still open.

```python
import duckdb
# Safe, non-locking connection
con = duckdb.connect('../data/processed/shaved_ice.duckdb', read_only=True)
df = con.execute("SELECT * FROM mart_forecast_input").df()
```

### 2. Using the Helper Library
We built `src/duckdb_loader.py` which uses `read_only=True` by default:
```python
import sys
sys.path.append('../src')
from duckdb_loader import load_mart_data, run_query
from utils import data_audit

# Load and audit in two lines
df = load_mart_data()
data_audit(df)
```

---

## 🧪 Phase 3: Feature Engineering Standards
Deciding where to put your logic is key for a clean project.

### When to use SQL (dbt)?
> **Rule:** Use SQL for heavy lifting, aggregations, and window functions that transform the entire dataset.
- Rolling averages (`AVG(...) OVER(...)`)
- Date/Time extraction (Day of week, is_weekend)
- Lags and Leads (Previous day's demand)
- Static thresholds (High severity flags)

### When to use Python (`src/utils.py`)?
> **Rule:** Use Python for complex math, ML-specific scaling, or ad-hoc column transformations needed right before modeling.
- One-hot encoding (`encode_categorical`)
- Z-score scaling (`scale_numeric`)
- Custom smoothing functions (`rolling_mean`)
- Final data filtering for a specific plot

---

## 🆘 Troubleshooting & Common Issues

### 🔒 DuckDB "Database is Locked"
**Cause:** You are trying to run `dbt run` while a Jupyter notebook or DuckDB CLI has a write-connection open.
**Fix:** 
1. Use `read_only=True` in notebooks for exploration.
2. Shutdown the notebook kernel before running `dbt run` (as it needs write access).
3. If errors persist, run `Stop-Process -Id <PID> -Force` in PowerShell using the PID shown in the error.

### 📁 File Not Found / Path Errors
**Cause:** Your terminal is not in the project root, or your notebook `sys.path` isn't updated.
**Fix:**
- Always `cd` to the project root before running `dbt`.
- Use `Path(__file__).parent` in Python scripts for robust path handling.

---

## 💡 Pro Tips for ICPE 2026
- **Resume Point:** Document every dbt model you build in `sql/models/schema.yml`. It shows you care about data governance.
- **Visual Excellence:** Use our `plotting.py` library and call `setup_plot_style()` at the top of your notebook to ensure all charts look consistent.
- **Modularity:** Use `data_audit(df)` from `utils.py` for a standard, professional inspection report.

---

## 🌐 GitHub Milestone Loop
Use these commands to sync your work with the cloud. Always run these from the project root.

1.  **Check Status:**
    `git status`
2.  **Stage Changes:**
    `git add .` (Our `.gitignore` safely handles data exclusion)
3.  **Commit with a Clear Message:**
    `git commit -m "feat: [Feature Name] - Brief description of changes"`
4.  **Push to GitHub:**
    `git push origin main`

---

## 🏁 The Path to Jan 25th (Next Steps)
Current Date: Jan 12th | Deadline: **Jan 25th**

| Milestone | Target Date | Status |
| :--- | :--- | :--- |
| **Data Audit & dbt Prep** | Jan 12th | ✅ Complete |
| **Exploratory Data Analysis** | Jan 15th | ⏳ Pending |
| **Baseline Forecasting Model** | Jan 18th | ⏳ Pending |
| **Model Optimization & Tuning** | Jan 21st | ⏳ Pending |
| **Final ICPE 2026 Report** | Jan 25th | ⏳ Pending |

### 🎯 Roadmap Items:
- **Phase 4: Advanced EDA**: Investigate the "Buffer Check" discrepancy between average demand and safety stock percentiles.
- **Phase 5: Baseline Modeling**: Implement a Simple Exponential Smoothing or Prophet model using `mart_forecast_input`.
- **Phase 6: Severity Analysis**: Use `mart_stockout_events` to quantify the financial impact of missed demand.
