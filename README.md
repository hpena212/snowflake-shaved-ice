# ICPE 2026 Data Challenge - Shaved Ice Dataset Analysis

**Deadline:** January 28, 2026  
**Status:** Submitted 🎉

 # Weekly Seasonality in Cloud Demand: Lessons from Snowflake's Shaved Ice Dataset
      2
      3 **ICPE 2026 Data Challenge Submission** | Under Peer Review
      4
      5 ## The Problem
      6
      7 Cloud providers offer steep discounts for long-term capacity commitments — but under-forecasting demand is **2.1x more expensiv
        e** than over-forecasting. Most capacity planning teams use rolling averages as their baseline forecast. We asked a simple ques
        tion: *do those rolling averages actually capture what's happening in the data?*
      8
      9 They don't. Snowflake's VM demand drops ~25% every weekend like clockwork — a pattern rolling averages structurally cannot capt
        ure.

## Overview

This project analyzes Snowflake's "Shaved Ice" VM demand dataset for the ICPE 2026 Data Challenge. It uses **dbt + DuckDB** for data transformations and **Python** for variance-aware forecasting analysis.

The core insight: In capacity planning, the outliers *are* the problem. A forecast that nails the mean but misses the variance causes downtime or wastes money.

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Containerization** | Docker + Docker Compose |
| **Data Engineering** | dbt-duckdb (SQL transformations) |
| **Database** | DuckDB (local analytical database) |
| **Analysis** | Python 3.13 (pandas, statsmodels) |
| **Visualization** | matplotlib, seaborn |
| **Notebooks** | Jupyter |

---

## 🚀 Quick Start

### Option A: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"

# 2. Clone the dataset
mkdir -p data/raw && cd data/raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ../..

# 3. Build and start Docker
docker-compose build
docker-compose up -d

# 4. Run dbt to build the database
docker exec shaved-ice-project dbt run --profiles-dir .

# 5. Open Jupyter
# Navigate to: http://localhost:8888
```

### Option B: Virtual Environment

```powershell
# 1. Clone the repository
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"

# 2. Create virtual environment (Python 3.10-3.13)
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Clone the dataset
mkdir data\raw -Force && cd data\raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ..\..

# 4. Run dbt
mkdir data\processed -Force
dbt run --profiles-dir .

# 5. Launch Jupyter
jupyter notebook
```

---

## 📁 Project Structure

```
Shaved Ice/
├── data/
│   ├── raw/shavedice-dataset/   # Downloaded dataset
│   └── processed/shaved_ice.duckdb  # Built by dbt
├── notebooks/
│   └── 01_data_exploration.ipynb
├── sql/models/                  # dbt SQL models
│   ├── staging/                 # Raw → Clean columns
│   ├── intermediate/            # Daily aggregations
│   └── marts/                   # Analysis-ready tables
├── src/                         # Python modules
│   ├── data_loader.py
│   ├── duckdb_loader.py
│   ├── forecasting.py
│   ├── plotting.py
│   └── utils.py
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Container orchestration
├── dbt_project.yml              # dbt configuration
├── profiles.yml                 # DuckDB connection
├── requirements.txt             # Python dependencies
└── verify_setup.py              # Setup verification script
```

---

## 🔧 Commands Reference

### Docker Commands

| Task | Command |
|------|---------|
| Start container | `docker-compose up -d` |
| Stop container | `docker-compose down` |
| Run dbt | `docker exec shaved-ice-project dbt run --profiles-dir .` |
| Open shell | `docker exec -it shaved-ice-project bash` |
| View logs | `docker-compose logs -f` |
| Rebuild | `docker-compose build --no-cache` |

### dbt Commands

| Task | Command |
|------|---------|
| Run all models | `dbt run --profiles-dir .` |
| Run specific model | `dbt run --select mart_forecast_input --profiles-dir .` |
| Test data quality | `dbt test --profiles-dir .` |
| Generate docs | `dbt docs generate --profiles-dir .` |

---

## 📊 How It Works

1. **dbt run** → Transforms raw parquet data into clean DuckDB tables
2. **Python** → Loads tables for forecasting analysis
3. **Jupyter** → Interactive exploration and visualization

```python
# Load dbt output in your Python scripts
from src.duckdb_loader import load_mart_data
df = load_mart_data()  # Returns a clean pandas DataFrame
```

---

## 🎯 Research Focus

**Core Question:** Do simple seasonal time-series models provide materially better demand forecasts than rolling-average baselines for aggregated cloud infrastructure?

---

## ✅ Progress

- [x] Project setup with Docker support
- [x] dbt pipeline configured (4 models)
- [x] Dataset integration
- [x] Multi-device workflow documented
- [x] Variance analysis
- [x] Forecasting models
- [x] Paper visualizations
- [x] ICPE 2026 submission


## 🔗 Links

- [ICPE 2026 Data Challenge](https://icpe2026.spec.org/tracks-and-submissions/data-challenge-track/)
- [Shaved Ice Dataset (Snowflake Labs)](https://github.com/Snowflake-Labs/shavedice-dataset)

---

## License

This project is for the ICPE 2026 Data Challenge submission.
