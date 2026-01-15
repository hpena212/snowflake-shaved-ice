# 🔄 Shaved Ice Project Handoff Guide

> **Purpose:** Seamless migration of the ICPE 2026 Shaved Ice project from Laptop → PC  
> **Last Updated:** January 14, 2026  
> **Estimated Setup Time:** ~5 minutes (Docker) | ~15 minutes (venv)

---

## 📋 Pre-Flight Checklist

Before you begin, verify your PC has:
- [x] Git installed and configured
- [x] ~500MB free disk space (for data + dependencies)

**Choose ONE setup method:**

| Method | Additional Requirements | Best For |
|--------|------------------------|----------|
| 🐳 **Docker (Recommended)** | Docker Desktop installed | Multi-device workflow, consistent environments |
| 🐍 **Virtual Environment** | Python 3.10-3.13 installed | Quick local development, no Docker available |

---

## 🐳 Docker Setup (Recommended)

Docker provides a consistent environment across all devices without Python version conflicts.

### Step 1: Clone the Repository

```powershell
# Clone the project
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"
```

### Step 2: Clone the Raw Dataset

```powershell
# Create data directories and clone dataset
mkdir -p data/raw
cd data/raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ../..
```

### Step 3: Build and Start Docker

```powershell
# Build the Docker image (first time takes ~2-3 minutes)
docker-compose build

# Start the container in background
docker-compose up -d
```

### Step 4: Run dbt to Build Database

```powershell
# Run dbt inside the container to create DuckDB tables
docker exec shaved-ice-project dbt run --profiles-dir .
```

**Expected output:**
```
Running with dbt=1.11.x
1 of 4 OK created sql table model main.stg_shaved_ice
2 of 4 OK created sql table model main.int_daily_demand
3 of 4 OK created sql table model main.mart_forecast_input
4 of 4 OK created sql table model main.mart_stockout_events
Completed successfully
Done. PASS=4 WARN=0 ERROR=0 SKIP=0 TOTAL=4
```

### Step 5: Access Jupyter Notebook

Open your browser to: **[http://localhost:8888](http://localhost:8888)**

Navigate to `notebooks/01_data_exploration.ipynb` and run all cells to confirm everything works.

---

### 🐳 Docker Commands Reference

| Task | Command |
|------|---------|
| **Start container** | `docker-compose up -d` |
| **Stop container** | `docker-compose down` |
| **View Jupyter logs** | `docker-compose logs -f` |
| **Run dbt** | `docker exec shaved-ice-project dbt run --profiles-dir .` |
| **Run dbt (specific model)** | `docker exec shaved-ice-project dbt run --select model_name --profiles-dir .` |
| **Open shell in container** | `docker exec -it shaved-ice-project bash` |
| **Run Python script** | `docker exec shaved-ice-project python script.py` |
| **Rebuild image** | `docker-compose build --no-cache` |
| **Check container status** | `docker-compose ps` |

### 🐳 Docker Validation Checklist

After setup, verify each capability:

- [ ] `docker-compose ps` shows container running
- [ ] [http://localhost:8888](http://localhost:8888) opens Jupyter
- [ ] `docker exec shaved-ice-project dbt run --profiles-dir .` completes with PASS=4
- [ ] Notebook `01_data_exploration.ipynb` runs all cells successfully
- [ ] `docker exec shaved-ice-project python -c "import duckdb; print('DuckDB OK')"` works

---

## 🐍 Virtual Environment Setup (Alternative)

Use this method if Docker is not available or you prefer local Python development.

### Step 1: Clone the Repository

```powershell
git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"
cd "Shaved Ice"
```

### Step 2: Create Virtual Environment

```powershell
# Create fresh virtual environment (use Python 3.10-3.13, NOT 3.14)
py -3.13 -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1
```

> [!TIP]
> You'll see `(.venv)` prefix in your terminal when activated.

> [!WARNING]
> If activation fails, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

> [!NOTE]
> This takes 2-3 minutes. `dbt-duckdb` pulls several dependencies.

### Step 4: Clone the Raw Dataset

```powershell
mkdir data\raw -Force
cd data\raw
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ..\..
```

### Step 5: Create Processed Directory and Run dbt

```powershell
mkdir data\processed -Force
.\.venv\Scripts\dbt run --profiles-dir .
```

### Step 6: Verify Setup

```powershell
$env:PYTHONIOENCODING='utf-8'; python verify_setup.py
```

**All checks should pass:**
```
✅ PASS    Dependencies
✅ PASS    Folder Structure
✅ PASS    dbt Setup
✅ PASS    Python Modules
✅ PASS    Dataset
```

### Step 7: Launch Jupyter

```powershell
jupyter notebook
```

---

### 🐍 venv Commands Reference

| Task | Command |
|------|---------|
| **Activate venv** | `.\.venv\Scripts\Activate.ps1` |
| **Deactivate venv** | `deactivate` |
| **Install deps** | `pip install -r requirements.txt` |
| **Run dbt** | `.\.venv\Scripts\dbt run --profiles-dir .` |
| **Start Jupyter** | `jupyter notebook` |
| **Verify setup** | `$env:PYTHONIOENCODING='utf-8'; python verify_setup.py` |

### 🐍 venv Validation Checklist

- [ ] Virtual environment activates without errors
- [ ] `python verify_setup.py` shows all green checkmarks
- [ ] `dbt run --profiles-dir .` completes with PASS=4
- [ ] Jupyter notebook opens and runs cells
- [ ] Git status shows branch info

---

## 🗂️ What Gets Transferred

### ✅ Files in Git (Automatically Transferred)
| Category | Files/Folders |
|----------|---------------|
| **Config** | `dbt_project.yml`, `profiles.yml`, `requirements.txt` |
| **Code** | `src/` (5 Python modules), `sql/` (dbt models) |
| **Notebooks** | `notebooks/01_data_exploration.ipynb` |
| **Docker** | `Dockerfile`, `docker-compose.yml`, `.dockerignore` |
| **Verification** | `verify_setup.py` |

### ⚠️ Files to Regenerate (NOT in Git)
| Category | How to Regenerate |
|----------|-------------------|
| `.venv/` | `py -3.13 -m venv .venv` (venv method only) |
| `data/raw/shavedice-dataset/` | `git clone https://github.com/Snowflake-Labs/shavedice-dataset.git` |
| `data/processed/shaved_ice.duckdb` | `dbt run --profiles-dir .` |
| `target/`, `logs/` | Regenerated by dbt |

---

## 📁 Project Structure Reference

```
Shaved Ice/
├── data/
│   ├── raw/
│   │   └── shavedice-dataset/  # ← CLONE from GitHub
│   └── processed/
│       └── shaved_ice.duckdb   # ← BUILT BY dbt
├── notebooks/
│   └── 01_data_exploration.ipynb
├── sql/
│   └── models/
│       ├── staging/stg_shaved_ice.sql
│       ├── intermediate/int_daily_demand.sql
│       └── marts/
│           ├── mart_forecast_input.sql
│           └── mart_stockout_events.sql
├── src/
│   ├── data_loader.py
│   ├── duckdb_loader.py
│   ├── forecasting.py
│   ├── plotting.py
│   └── utils.py
├── dbt_project.yml
├── profiles.yml
├── requirements.txt
├── verify_setup.py
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker orchestration
└── .dockerignore           # Docker build exclusions
```

---

## 🆘 Troubleshooting

### Docker Issues

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
# Stop other Jupyter instances or change port in docker-compose.yml
docker-compose down
# Edit docker-compose.yml: change "8888:8888" to "8889:8888"
docker-compose up -d
# Then access http://localhost:8889
```

### venv Issues

**"dbt: command not found"**
```powershell
.\.venv\Scripts\dbt run --profiles-dir .
```

**"Database is locked" error**
1. Close any Jupyter notebooks connected to the database
2. Kill any lingering Python processes
3. Re-run dbt

**Virtual environment won't activate**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python version too new (3.14+)**
dbt-duckdb is not yet compatible with Python 3.14. Use Python 3.10-3.13.

---

## 💡 Pro Tips for Multi-Device Workflow

1. **Always commit before switching devices**
   ```powershell
   git add .
   git commit -m "chore: checkpoint before device switch"
   git push origin main
   ```

2. **Prefer Docker for consistency**
   - Same environment on every device
   - No Python version management needed

3. **Use relative paths everywhere**
   - Notebooks: `../data/processed/shaved_ice.duckdb`
   - Scripts: `Path(__file__).parent / 'data'`

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
dbt run --profiles-dir .
```

---

## 🤖 Agent Instructions

For AI agents (Antigravity, Claude, etc.) setting up this project:

### Docker Path (Preferred)
1. Verify Docker: `docker --version`
2. Clone repo: `git clone https://github.com/hpena212/snowflake-shaved-ice.git "Shaved Ice"`
3. Clone data: `cd "Shaved Ice/data/raw" && git clone https://github.com/Snowflake-Labs/shavedice-dataset.git`
4. Build: `docker-compose build`
5. Start: `docker-compose up -d`
6. Run dbt: `docker exec shaved-ice-project dbt run --profiles-dir .`
7. Verify: `docker exec shaved-ice-project python -c "import duckdb; conn = duckdb.connect('data/processed/shaved_ice.duckdb'); print(conn.execute('SELECT COUNT(*) FROM mart_forecast_input').fetchone())"`

### venv Path (Fallback)
1. Verify Python: `py -3.13 --version` (must be 3.10-3.13, NOT 3.14)
2. Clone repo and data (same as above)
3. Create venv: `py -3.13 -m venv .venv`
4. Activate: `.\.venv\Scripts\Activate.ps1`
5. Install: `pip install -r requirements.txt`
6. Create dirs: `mkdir data\processed -Force`
7. Run dbt: `dbt run --profiles-dir .`
8. Verify: `$env:PYTHONIOENCODING='utf-8'; python verify_setup.py`

---

**You're all set!** 🎉 Your project should now work identically on any device.
