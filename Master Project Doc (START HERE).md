# 🧊 ICPE 2026 Shaved Ice: Master Project Document

> **Deadline:** January 28, 2026 | **Current Date:** January 12, 2026 | **Days Remaining:** 16

---

## 🎯 The Core Philosophy

> "I learned that in retail. Now I'm applying it to cloud infrastructure."

### The Variance Problem

| Domain | What Averages Hide | What Variance Reveals |
|--------|-------------------|----------------------|
| **Retail** | "We sell 100 units/day" | The Tuesday spike that empties shelves before noon |
| **Cloud** | "We need 5,000 VMs on average" | The 2pm burst that crashes production |

**The insight:** In capacity planning, the outliers *are* the problem. A forecast that nails the mean but misses the variance is a forecast that causes downtime or wastes money.

### Project Goal

Build a **variance-aware forecast** for VM demand that:
1. Quantifies demand uncertainty (not just point predictions)
2. Calculates safety stock buffers using percentile-based methods
3. Measures the cost of under/over-provisioning
4. Produces interpretable results for capacity planners

---

## 📊 Current Project State (End of Day 1)

### ✅ Infrastructure Complete
- **dbt + DuckDB pipeline** configured and tested
- **Data loaded:** `shaved_ice.duckdb` with staging, intermediate, and mart models
- **Python environment:** Full utility library in `src/` (loader, plotting, forecasting modules)
- **Notebook:** `01_data_exploration.ipynb` with initial EDA

### 🔍 Key Discoveries So Far
1. **Concerning safety stock scenario:** Buffer near zero while demand spikes to ~12k
2. **Structural break detected:** Sharp demand drop mid-2022 (possible client departure)
3. **Data shape:** Daily observations from 2020-2024 across multiple regions/instance types

### 📁 Project Architecture
```
Shaved Ice/
├── sql/models/           # dbt transformations (the "kitchen")
│   ├── staging/          # Raw data → Clean columns
│   ├── intermediate/     # Daily aggregations
│   └── marts/            # Analysis-ready tables
├── src/                  # Python utility library
│   ├── duckdb_loader.py  # Load dbt output → pandas
│   ├── utils.py          # Data audit, encoding
│   ├── plotting.py       # Consistent visualizations
│   └── forecasting.py    # Model implementations
├── notebooks/            # Interactive analysis
└── data/                 # Raw + processed DuckDB
```

---

## 🗓️ Day 2 Action Plan (January 13, 2026)

### Morning Block (2-3 hours): Variance Exploration

| Priority | Task | Deliverable |
|:--------:|------|-------------|
| 🔴 | Implement rolling volatility metrics | New columns: `rolling_std_7d`, `coef_of_variation` |
| 🔴 | Handle the structural break | Boolean flag `is_post_break` for mid-2022 and onward |
| 🟡 | Create demand percentile bands | 5th, 50th, 95th percentile by region |

**Specific actions:**
1. Open `01_data_exploration.ipynb`
2. Add a new section: "## Variance Deep-Dive"
3. Compute: `df['rolling_std_7d'] = df.groupby(['region', 'instance_type'])['demand'].transform(lambda x: x.rolling(7).std())`
4. Visualize variance over time to confirm the structural break

### Afternoon Block (2-3 hours): Feature Engineering

| Priority | Task | Why It Matters |
|:--------:|------|----------------|
| 🔴 | Add lag features | Yesterday's demand predicts today's |
| 🔴 | Add day-of-week encoding | Weekday/weekend patterns drive demand |
| 🟡 | Create `total_capacity` metric | `demand_7d_avg + safety_stock_95pct` |

**SQL vs Python decision:**
- **In dbt (SQL):** Rolling averages, lags, date extraction (these transform the whole dataset)
- **In Python:** One-hot encoding, scaling (these are model-specific)

### Evening Block (1-2 hours): Documentation & Commit

| Task | Command |
|------|---------|
| Document findings in notebook markdown cells | — |
| Update `lab_notebook.md` with today's learnings | — |
| Commit progress to GitHub | `git add . && git commit -m "feat: variance analysis + feature engineering"` |

---

## 📈 Week-by-Week Roadmap

### Week 1: Foundation (Jan 12-15) ✅ You are here
| Day | Focus |
|-----|-------|
| Day 1 (Done) | Environment setup, data loading, initial EDA |
| Day 2 (Tomorrow) | Variance analysis, structural break handling, feature engineering |
| Day 3 | Complete `mart_forecast_input` with all engineered features |
| Day 4 | Data quality tests, documentation checkpoint |

### Week 2: Baseline Models (Jan 16-19)
| Day | Focus |
|-----|-------|
| Day 5 | Simple Moving Average forecast |
| Day 6 | Exponential Smoothing (capture trend + seasonality) |
| Day 7 | Implement proper train/test split (time-based) |
| Day 8 | Establish baseline metrics: MAE, MAPE, Coverage |

### Week 3: Variance-Aware Forecasting (Jan 20-24)
| Day | Focus |
|-----|-------|
| Day 9-10 | Quantile regression or Conformal Prediction for prediction intervals |
| Day 11 | Safety stock optimization: What buffer minimizes cost? |
| Day 12 | Stockout severity analysis using `mart_stockout_events` |
| Day 13 | Final model selection and tuning |

### Week 4: Deliverable (Jan 25-28)
| Day | Focus |
|-----|-------|
| Day 14 | Generate all paper visualizations |
| Day 15 | Write ICPE 2026 submission |
| Day 16 | Final review, polish, submit |

---

## 🧠 The Retail-to-Cloud Translation Guide

This section maps your 7 years of operations intuition to cloud concepts:

| Retail Concept | Cloud Equivalent | In This Dataset |
|---------------|------------------|-----------------|
| SKU | Instance Type | `instance_type` (e.g., `n1-standard-4`) |
| Store | Region | `region` (e.g., `us-east-1`) |
| Daily Sales | Demand | `demand` (concurrent VMs observed) |
| Safety Stock | Capacity Buffer | `safety_stock_95pct` |
| Stockout | Downtime | When `demand > capacity_limit` |
| Overstock | Wasted Spend | When `capacity >> demand` |
| Service Level | SLA | 95th percentile fulfillment target |

### The Tradeoff You Already Know

```
            Low Buffer                    High Buffer
               ↓                              ↓
        More Stockouts              Less Stockouts
        Lower Holding Cost          Higher Holding Cost
        Angry Customers             Wasted Capital
               ↓                              ↓
           (Downtime)                    (Overspend)
```

**Your job:** Find the sweet spot where the cost of downtime equals the cost of over-provisioning.

---

## 📚 Learning Resources Queue

Since you're learning time series by doing, here's a curated list:

### Concepts to Review (Prioritized)
1. **Rolling statistics** (mean, std, percentiles) — You'll use these immediately
2. **Coefficient of Variation (CV)** — Normalize variance across different scales
3. **Prediction Intervals** — The variance around your point forecast
4. **Quantile Regression** — Predict the 95th percentile directly

### Optional Deep-Dives (For Later)
- Prophet (Facebook's forecasting library)
- Conformal Prediction (distribution-free uncertainty)
- ARIMA decomposition (trend + seasonality + residual)

---

## 🔧 Quick Reference Commands

### 🐳 Docker (Recommended)
```powershell
# Start container (Jupyter available at http://localhost:8888)
docker-compose up -d

# Run dbt
docker exec shaved-ice-project dbt run --profiles-dir .

# Run specific model
docker exec shaved-ice-project dbt run --select mart_forecast_input --profiles-dir .

# Stop container
docker-compose down

# Git commit
git add . && git commit -m "feat: description"
```

### 🐍 venv (Alternative)
```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run dbt
dbt run --profiles-dir .

# Start Jupyter
jupyter notebook
```

---

## ✅ Success Criteria for ICPE 2026

Your submission should demonstrate:

1. **Data Engineering Rigor:** Clean dbt pipeline from raw → analysis-ready
2. **Variance Awareness:** Not just point forecasts, but prediction intervals
3. **Business Translation:** Connect statistical metrics to cost/downtime tradeoffs
4. **Reproducibility:** Anyone can clone, run `dbt run`, and replicate results
5. **Interpretability:** A capacity planner can understand and act on outputs

![[Master Project.png]]
---

*Last Updated: January 12, 2026*  
*Next Review: End of Day 2*
