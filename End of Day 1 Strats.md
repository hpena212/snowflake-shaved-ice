# End of Day 1 – Strategies & Reflections

## What We Accomplished Today
- **Loaded the shaved‑ice demand dataset** using the `duckdb_loader` utilities.
- **Explored basic statistics** (`head`, `info`, `describe`) and visualised demand vs. safety‑stock for a sample region/instance type.
- **Identified a concerning stock‑out scenario** where the safety‑stock line hugs zero while demand spikes to ~12 k.
- **Noted a structural break** around mid‑2022 (sharp demand drop) that could bias volatility calculations.
- **Switched the notebook kernel** to the project’s virtual environment (`.venv`).

## Immediate Tonight (🕒 19:00‑22:00)
1. **Add a moving‑average buffer** – compute a 7‑day rolling average of `demand` and add it to `safety_stock_95pct` to visualise true capacity requirements.
2. **Filter the structural break** – create a mask to exclude dates where demand falls below a threshold (e.g., < 5 k) or where a known client left.
3. **Re‑run volatility metrics** (standard deviation, coefficient of variation) on the cleaned series.
4. **Document findings** in the notebook markdown cells so the narrative stays clear.

## Next 2‑3 Days (📅)
- **Deep‑dive into key variables** – region, instance_type, date, demand, safety_stock_95pct, and any engineered features (rolling averages, lagged demand).
- **Feature engineering** – consider:
  - 7‑day and 30‑day rolling means/medians.
  - Day‑of‑week and month‑of‑year dummy variables.
  - Lag features (previous day/week demand).
- **Model‑ready preprocessing** – handle missing values, outliers, and encode categorical columns.
- **Prototype a forecasting model** (e.g., Prophet, ARIMA, or a simple linear regression) using the engineered features.

## Full Agenda (Weeks Ahead)
| Week | Focus |
|------|-------|
| **Week 1** | Data cleaning, exploratory analysis, structural break handling. |
| **Week 2** | Feature engineering, baseline forecasting models, evaluation metrics. |
| **Week 3** | Hyper‑parameter tuning, model comparison, uncertainty quantification. |
| **Week 4** | Deploy a reproducible pipeline (DuckDB → Python → Jupyter) and generate a final report. |

## Study / Preparation Checklist
- Review **time‑series forecasting** concepts (trend, seasonality, residuals).
- Read up on **inventory theory** – safety stock, service level, and order‑up‑to calculations.
- Familiarise yourself with **DuckDB SQL** for data extraction (see `sql/models` files).
- Brush up on **pandas rolling/window functions** and **matplotlib/seaborn** styling for clean visualisations.
- Explore **scikit‑learn pipelines** for preprocessing + modeling.

---

## Dataset Overview (as of today)
| Variable | Description | Typical Range / Notes |
|----------|-------------|-----------------------|
| `date` | Observation date (daily) | 2020‑01‑01 → 2024‑12‑31 |
| `region` | Geographic region of the VM fleet | Categorical (e.g., `us-east-1`, `eu-west-2`) |
| `instance_type` | VM type (e.g., `n1-standard-4`) | Categorical |
| `demand` | Actual concurrent VMs observed | 0 – ≈ 12 000 |
| `safety_stock_95pct` | Buffer calculated for 95 % service level | Often < 500; currently near 0 |
| `forecast` (future) | Model‑generated demand forecast (not yet built) | – |

**Potentially useful variables** (derived or existing):
- **Rolling averages** (`demand_7d_avg`, `demand_30d_avg`).
- **Day‑of‑week** (`dow`) and **month** (`month`).
- **Lagged demand** (`demand_lag_1`, `demand_lag_7`).
- **Binary flag** for the structural break period (`post_break`).

**Suggested transformations**:
1. **Create rolling‑average columns** using `df['demand'].rolling(7).mean()`.
2. **Add the safety‑stock buffer**: `df['total_capacity'] = df['demand_7d_avg'] + df['safety_stock_95pct']`.
3. **Encode categoricals** with one‑hot or ordinal encoding for modeling.
4. **Remove or down‑weight outliers** (e.g., demand spikes > 3 σ) after confirming they are not genuine.
5. **Impute missing values** (if any) with forward‑fill or median of the region/instance.

---

*Keep this document as a living checklist – update it each day as you progress.*
