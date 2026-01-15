# 🚀 ICPE 2026: Shaved Ice Project Workflow

> **Your definitive Source of Truth** for all development on this project.  
> **Last Updated:** January 14, 2026  
> **Deadline:** January 25, 2026

---

## 🧭 Project Compass (Directory Map)

Use this to find your way around if you've been away from the project:

```
Shaved Ice/
├── data/
│   ├── raw/shavedice-dataset/   # Source data (cloned from Snowflake Labs)
│   └── processed/shaved_ice.duckdb  # Built by dbt
├── notebooks/                   # Interactive exploration & modeling
├── sql/models/                  # dbt project (staging → intermediate → marts)
├── src/                         # Python utilities (utils.py, plotting.py, duckdb_loader.py)
├── target/                      # dbt compilation artifacts
├── Dockerfile                   # Container definition
└── docker-compose.yml           # Container orchestration
```

---

## ⚡ Quick Start: Choose Your Environment

You have **two options** for running this project. Docker is recommended for consistency across devices.

| Method | Best For | Start Command |
|--------|----------|---------------|
| 🐳 **Docker** (Recommended) | Multi-device, no Python version issues | `docker-compose up -d` |
| 🐍 **Virtual Environment** | Quick local development | `.\.venv\Scripts\Activate.ps1` |

---

## 📅 The Daily Developer Loop

### 🐳 Docker Workflow (Recommended)

**Starting your day:**
```powershell
cd "Shaved Ice"
git pull origin main              # Get latest changes
docker-compose up -d              # Start container
# Open http://localhost:8888 for Jupyter
```

**Ending your day:**
```powershell
git add .
git commit -m "feat: your message"
git push origin main
docker-compose down               # Optional: free resources
```

### 🐍 Virtual Environment Workflow

**Starting your day:**
```powershell
cd "Shaved Ice"
git pull origin main
.\.venv\Scripts\Activate.ps1
jupyter notebook
```

**Ending your day:**
```powershell
git add .
git commit -m "feat: your message"
git push origin main
deactivate
```

---

## 🛠️ First-Time / Re-entry Setup

### Option A: Docker Setup (Recommended)

```powershell
# 1. Clone the project
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"

# 2. Clone raw dataset
cd data/raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ../..

# 3. Build and start Docker
docker-compose build
docker-compose up -d

# 4. Build DuckDB database
docker exec shaved-ice-project dbt run --profiles-dir .

# 5. Open Jupyter at http://localhost:8888
```

### Option B: Virtual Environment Setup

```powershell
# 1. Clone the project
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"

# 2. Create virtual environment (Python 3.10-3.13 only, NOT 3.14)
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Clone raw dataset
cd data/raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ../..

# 5. Build DuckDB database
mkdir data\processed -Force
.\.venv\Scripts\dbt run --profiles-dir .

# 6. Verify setup
$env:PYTHONIOENCODING='utf-8'; python verify_setup.py

# 7. Start Jupyter
jupyter notebook
```

---

## 🔧 Command Reference

### 🐳 Docker Commands

| Task | Command |
|------|---------|
| **Start container** | `docker-compose up -d` |
| **Stop container** | `docker-compose down` |
| **View logs** | `docker-compose logs -f` |
| **Run dbt** | `docker exec shaved-ice-project dbt run --profiles-dir .` |
| **Run specific model** | `docker exec shaved-ice-project dbt run --select model_name --profiles-dir .` |
| **Open shell** | `docker exec -it shaved-ice-project bash` |
| **Rebuild image** | `docker-compose build --no-cache` |

### 🐍 venv Commands

| Task | Command |
|------|---------|
| **Activate** | `.\.venv\Scripts\Activate.ps1` |
| **Deactivate** | `deactivate` |
| **Run dbt** | `.\.venv\Scripts\dbt run --profiles-dir .` |
| **Compile only** | `.\.venv\Scripts\dbt compile --profiles-dir .` |
| **Start Jupyter** | `jupyter notebook` |
| **Verify setup** | `$env:PYTHONIOENCODING='utf-8'; python verify_setup.py` |

---

## 🛠️ Phase 1: SQL & dbt Workflow

Use this when you need to add new metrics, filter data, or aggregate to new granularities.

### 1. Add/Modify a Model
- Create or edit a file in `sql/models/marts/` (e.g., `mart_new_metric.sql`).
- Always use the `{{ ref('...') }}` function to depend on other models.
- **Tip:** Keep logic clean in Common Table Expressions (CTEs).

### 2. Build and Test

**Docker:**
```powershell
# Compile only (check syntax)
docker exec shaved-ice-project dbt compile --profiles-dir .

# Run specific model
docker exec shaved-ice-project dbt run --select mart_stockout_events --profiles-dir .

# Run everything
docker exec shaved-ice-project dbt run --profiles-dir .
```

**venv:**
```powershell
# Compile only
.\.venv\Scripts\dbt compile --profiles-dir .

# Run specific model
.\.venv\Scripts\dbt run --select mart_stockout_events --profiles-dir .

# Run everything
.\.venv\Scripts\dbt run --profiles-dir .
```

---

## 🐍 Phase 2: Python & Jupyter Integration

### Connecting to DuckDB

**Inside a Notebook:**
Always use the relative path `../data/processed/shaved_ice.duckdb`. 

**Crucial Tip:** Use `read_only=True` to prevent locking the database:

```python
import duckdb
# Safe, non-locking connection
con = duckdb.connect('../data/processed/shaved_ice.duckdb', read_only=True)
df = con.execute("SELECT * FROM mart_forecast_input").df()
```

### Using the Helper Library

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

## 🌐 GitHub Workflow

### Quick Sync (Direct to Main)
```powershell
git status
git add .
git commit -m "feat: [Feature Name] - Brief description"
git push origin main
```

### Feature Branch Workflow (Recommended for Larger Changes)
```powershell
# 1. Create a branch for your work
git checkout -b feature/day-2-variance

# 2. Make changes, commit
git add .
git commit -m "feat: add rolling volatility metrics"

# 3. Push your branch
git push origin feature/day-2-variance

# 4. Go to GitHub → Open a Pull Request → Merge it
```

---

## 🆘 Troubleshooting & Common Issues

### 🐳 Docker Issues

**"Cannot connect to Docker daemon"**
- Ensure Docker Desktop is running
- On Windows, check that WSL 2 is properly installed

**Container won't start**
```powershell
docker-compose down
docker-compose up -d
docker-compose logs
```

**Port 8888 already in use**
```powershell
# Edit docker-compose.yml: change "8888:8888" to "8889:8888"
docker-compose down
docker-compose up -d
# Access http://localhost:8889
```

### 🔒 DuckDB "Database is Locked"
**Cause:** You are trying to run `dbt run` while a Jupyter notebook has a write-connection open.
**Fix:** 
1. Use `read_only=True` in notebooks for exploration.
2. Shutdown the notebook kernel before running `dbt run`.
3. If errors persist, run `Stop-Process -Id <PID> -Force` in PowerShell.

### 📁 File Not Found / Path Errors
**Cause:** Your terminal is not in the project root, or your notebook `sys.path` isn't updated.
**Fix:**
- Always `cd` to the project root before running `dbt`.
- Use `Path(__file__).parent` in Python scripts for robust path handling.

### 🐍 Python Version Too New (3.14+)
dbt-duckdb is not yet compatible with Python 3.14. Use Python 3.10-3.13.

---

## 💡 Pro Tips for ICPE 2026

- **Resume Point:** Document every dbt model you build in `sql/models/schema.yml`. It shows you care about data governance.
- **Visual Excellence:** Use our `plotting.py` library and call `setup_plot_style()` at the top of your notebook for consistent charts.
- **Modularity:** Use `data_audit(df)` from `utils.py` for a standard, professional inspection report.
- **Docker First:** Prefer Docker for consistency — same environment on every device, no Python version headaches.
- **dbt Docs:** Run `dbt docs generate` then `dbt docs serve` to view interactive documentation.

---

## 🏁 The Path to Jan 25th

Current Date: Jan 14th | Deadline: **Jan 25th**

| Milestone | Target Date | Status |
| :--- | :--- | :--- |
| **Data Audit & dbt Prep** | Jan 12th | ✅ Complete |
| **Docker Multi-Device Setup** | Jan 14th | ✅ Complete |
| **Exploratory Data Analysis** | Jan 15th | ⏳ Pending |
| **Baseline Forecasting Model** | Jan 18th | ⏳ Pending |
| **Model Optimization & Tuning** | Jan 21st | ⏳ Pending |
| **Final ICPE 2026 Report** | Jan 25th | ⏳ Pending |

### 🎯 Roadmap Items:
- **Phase 4: Advanced EDA**: Investigate the "Buffer Check" discrepancy between average demand and safety stock percentiles.
- **Phase 5: Baseline Modeling**: Implement a Simple Exponential Smoothing or Prophet model using `mart_forecast_input`.
- **Phase 6: Severity Analysis**: Use `mart_stockout_events` to quantify the financial impact of missed demand.

---

## 📞 Quick Recovery

### Docker Reset
```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker exec shaved-ice-project dbt run --profiles-dir .
```

### venv Reset
```powershell
Remove-Item -Recurse -Force .venv, target, logs, data\processed -ErrorAction SilentlyContinue
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdir data\processed -Force
.\.venv\Scripts\dbt run --profiles-dir .
```

---

**Happy coding!** 🎉
