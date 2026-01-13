# ICPE 2026 Data Challenge - Shaved Ice Dataset Analysis

**Project Deadline:** January 28, 2026  
**Status:** Setup in progress

## Overview
This project analyzes Snowflake's "Shaved Ice" VM demand dataset for the ICPE 2026 Data Challenge. The goal is to develop simple, explainable forecasting models for cloud resource provisioning and produce a 4-page ACM conference paper.

## Dataset
- **Source:** [Snowflake Labs Shaved Ice Dataset](https://github.com/Snowflake-Labs/shavedice-dataset)
- **Description:** ~3 years of hourly VM demand data (2021-2024)
- **Format:** Compressed CSV / Parquet

## Research Questions
1. Can simple moving averages effectively forecast VM demand?
2. What safety stock levels minimize over/under-provisioning?
3. How do demand patterns vary across regions and instance types?

## Setup Instructions

### 1. Activate Virtual Environment
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or using Command Prompt
.venv\Scripts\activate.bat
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Download Dataset
```powershell
cd data/raw/
git clone https://github.com/Snowflake-Labs/shavedice-dataset.git
cd ../../
```

### 4. Verify Setup
```powershell
python verify_setup.py
```

## Project Structure
```
Shaved Ice/
├── data/                     # Data files (gitignored)
│   ├── raw/                  # Original dataset
│   └── processed/            # Cleaned data
├── notebooks/                # Jupyter analysis
├── src/                      # Reusable Python modules
├── figures/                  # Publication-ready plots
├── paper/                    # ACM paper drafts
└── sql/                      # SQL transformations
```

## Checkpoints
- [x] Project setup complete
- [ ] Dataset downloaded and validated
- [ ] Exploratory data analysis
- [ ] Baseline forecasting model
- [ ] Safety stock analysis
- [ ] Visualizations for paper
- [ ] Draft paper sections
- [ ] Final submission ready

## Key Principles
- **Simplicity over complexity:** Explainable models preferred
- **Reproducibility:** All analysis in Jupyter notebooks + scripts
- **Documentation:** Research decisions logged in `lab_notebook.md`
- **Speed:** Deadline-driven iteration

## Contact
ICPE 2026 Data Challenge submission for [Your Name]
