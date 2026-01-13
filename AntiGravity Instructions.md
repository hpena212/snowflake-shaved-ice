# ICPE 2026 Data Challenge - AntiGravity Agent Handoff

**TO:** Opus 4.5 (Planning Mode)  
**FROM:** User Project Documentation  
**PURPOSE:** Generate comprehensive project walkthrough and execution materials  
**DEADLINE:** January 28, 2026 (17 days remaining)

---

## Agent Mission Brief

You are being asked to create THREE deliverables that will guide a college student through completing their first academic research paper for the ICPE 2026 Data Challenge. The student has strong Python/SQL skills but limited time series forecasting and academic writing experience.

### Context Summary
- **Project:** Analyze Snowflake VM demand data using retail inventory management principles
- **Deliverable:** 4-page ACM-format research paper + code submission
- **Dataset:** 3 years of hourly Snowflake VM usage (Shaved Ice dataset)
- **Unique Angle:** Applying safety stock/service level concepts from retail to cloud capacity planning
- **Stakes:** Resume booster for Snowflake internship, published research, conference presentation

### What You Need to Produce

**OUTPUT 1: Project Walkthrough (Detailed Guide)**
- Comprehensive navigation document explaining each phase
- Clear explanations of technical concepts (time series, safety stock, forecasting)
- Troubleshooting guidance for common pitfalls
- Quality checkpoints throughout

**OUTPUT 2: Knowledge Bank (.md)**
- Centralized reference document containing:
  - Key formulas (safety stock, percentiles, moving averages)
  - Dataset specifications (columns, time range, granularity)
  - ACM submission requirements
  - Technical definitions (z-score, service level, volatility)
  - Important URLs and resources

**OUTPUT 3: Linear Task List**
- Ordered, actionable steps from Day 1 → Day 17
- Each task should be completable in one sitting (2-4 hours max)
- Clear success criteria for each task
- Dependencies explicitly noted

---

## Source Material Analysis

You have been provided with three planning documents:

1. **"Shave Ice Claude.md"** - Comprehensive master strategy (most detailed)
2. **"Shaved Ice.md"** - Project handoff with execution workflow
3. **"Snowflake Data Challenge Plan.md"** - Checkpoint-based execution plan

### Key Information to Extract

**From Master Strategy Document:**
- 4-phase execution plan (Ingestion → Analysis → Writing → Submission)
- Retail inventory framework explanation
- GitHub repository file descriptions
- Quality checklist
- Emergency contingencies

**From Project Handoff:**
- File-by-file repository guide (color-coded by priority)
- The "Hybrid Workflow" (SQL + Python approach)
- Submission constraints

**From Checkpoint Plan:**
- Week-by-week milestone structure
- Interview narrative focus
- Lab notebook approach
- "Done Means" success criteria

---

## Technical Requirements Context

### Student's Current Skillset
- Python (Pandas, NumPy) - Used in Credit Risk project
- Data Visualization - Created boxplots, time-series, heatmaps
- SQL - Database coursework
- Statistical Analysis - Linear regression background
- **GAPS:** Time series forecasting, academic paper writing, ACM LaTeX format

### Tools Available
- Python environment (Jupyter notebooks)
- SQL capability (DuckDB or SQLite recommended)
- Git/GitHub
- Access to the Shaved Ice dataset repository

### What Student Does NOT Need
- Advanced ML/deep learning
- R programming (Python version exists)
- Formal time series course
- Complex statistical models

---

## Critical Constraints & Rules

### Hard Deadlines
- January 28, 2026: Final submission deadline
- January 25, 2026: Recommended completion (3-day buffer)

### Paper Requirements
- 4 pages maximum (including figures/tables)
- +1 page for references
- ACM conference format template
- Double-blind submission (NO author names)
- HotCRP platform, "Data Challenge" track

### Analysis Philosophy
**DO:**
- Start simple (moving averages before complex models)
- Focus on clarity and explainability
- Use retail/operations analogies
- Visualize early and often

**DON'T:**
- Chase ML complexity
- Ignore data quality issues
- Use jargon without explanation
- Over-optimize metrics

---

## Core Analytical Framework to Explain

### The Retail Inventory Analogy
**Problem Statement:**
Cloud providers face the same challenge as retail stores:
- Too little capacity = Stockouts (crashes, latency)
- Too much capacity = Overstock (wasted money)

**Safety Stock Formula:**
```
Safety Stock = z-score × σ × √lead_time
```

**Translated to Cloud Context:**
- **z-score:** Desired service level (95% = 1.65, 99% = 2.33)
- **σ (sigma):** Standard deviation of VM demand (volatility)
- **lead_time:** Time to spin up new VMs (assume 1 hour for Snowflake)

### Key Metrics to Calculate
1. **Mean Demand** - Baseline capacity needed
2. **Standard Deviation (σ)** - Volatility measure
3. **95th Percentile Demand** - Safety buffer calculation
4. **Peak Demand (99th percentile)** - Disaster planning
5. **Service Level** - % of time capacity meets demand

---

## Repository File Guide (What Student Will See)

### Essential Files (Day 1 Priority)
- `IntroAnalysis-py.ipynb` - Starter code, MUST RUN THIS FIRST
- `hourly_normalized.csv.gz` - The actual dataset (compressed)
- `README.md` - Column definitions and normalization explanation
- `timeseries.png` - Quality benchmark for visualizations

### Supporting Files
- `hourly_normalized.parquet` - Alternative data format (faster loading)
- `IntroAnalysis.Rmd` / `.pdf` - R version (can skip if using Python)
- `figures/` folder - Professional visualization templates
- `requirements.txt` - Python dependencies

### File They'll Create
- Project folder structure:
  ```
  icpe-2026/
  ├── notebooks/     (analysis work)
  ├── data/          (downloaded dataset)
  ├── figures/       (paper visualizations)
  ├── paper/         (LaTeX/Word draft)
  └── README.md      (process documentation)
  ```

---

## Success Criteria (What "Done" Looks Like)

### Minimum Viable Paper (Bronze Tier)
- Data loaded and validated (no errors)
- 1 clear finding with supporting evidence
- 3 publication-quality visualizations
- 4-page paper in ACM format
- Submitted before deadline

### Strong Submission (Silver Tier)
- Retail inventory framework clearly explained
- Safety stock calculation demonstrated
- Cost/reliability tradeoff quantified
- Code submitted with documentation
- Paper is readable by non-experts

### Exceptional Work (Gold Tier)
- Novel insight about Snowflake's workload patterns
- Multiple regions/VM types compared
- Reproducible analysis with clean code
- Discussion of business implications
- Could be cited by Snowflake engineers

---

## Common Pitfalls to Address in Walkthrough

### Technical Pitfalls
- Opening compressed .gz file in Excel (will fail)
- Missing data handling (gaps in hourly time series)
- Confusing "normalized" data scale
- Not installing requirements.txt dependencies
- Trying to load 3 years of hourly data into memory at once

### Analytical Pitfalls
- Using mean instead of percentiles for capacity planning
- Ignoring seasonality (weekly/monthly patterns)
- Over-fitting to historical data
- Not validating forecast on holdout period
- Forgetting to document assumptions

### Writing Pitfalls
- Using first person ("I analyzed..." → "We analyze...")
- Not citing the Snowflake paper
- Figures without captions or in-text references
- Forgetting to anonymize PDF metadata
- Exceeding 4-page limit

### Time Management Pitfalls
- Spending too long on data cleaning (diminishing returns)
- Trying to implement complex ML models
- Writing before analysis is complete
- Not leaving buffer time for formatting issues

---

## Recommended Walkthrough Structure

### Phase 1: Environment Setup & Data Validation (Days 1-3)
Focus on proving the data is accessible and understandable.

### Phase 2: Exploratory Analysis & Pattern Recognition (Days 4-7)
Focus on identifying volatility, seasonality, and regional differences.

### Phase 3: Forecasting & Safety Stock Calculation (Days 8-12)
Focus on implementing the retail inventory framework.

### Phase 4: Paper Writing & Visualization (Days 13-15)
Focus on translating analysis into clear narrative.

### Phase 5: Submission Preparation (Days 16-17)
Focus on formatting, anonymization, and final checks.

---

## Knowledge Bank Categories to Organize

### 1. Dataset Specifications
- Time range: 2/1/2021 to 1/30/2024
- Granularity: Hourly observations
- Key columns: timestamp, VM_type, region, demand_count
- What "normalized" means in this context

### 2. Formulas & Calculations
- Moving average: `df.rolling(window=7).mean()`
- Percentile: `df.quantile(0.95)`
- Standard deviation: `df.std()`
- Safety stock formula with examples

### 3. Submission Requirements
- ACM template download location
- HotCRP submission process
- Anonymization checklist
- File format requirements

### 4. Quality Benchmarks
- What makes a "publication-quality" figure
- Citation style examples
- Paper section length guidelines

### 5. Troubleshooting Guide
- Python environment issues
- Data loading errors
- Common Pandas operations
- LaTeX compilation problems

---

## Linear Task List Structure Guidelines

### Task Format
Each task should include:
1. **Task Name** (action-oriented, e.g., "Load and validate dataset")
2. **Estimated Time** (realistic, e.g., 2-3 hours)
3. **Prerequisites** (e.g., "Must complete Task #3 first")
4. **Success Criteria** (concrete, e.g., "Plot displays without errors")
5. **Deliverable** (tangible output, e.g., "working notebook file")
6. **Common Issues** (what might go wrong)

### Task Dependencies
Clearly mark which tasks are:
- **Sequential** (must be done in order)
- **Parallel** (can be done simultaneously)
- **Optional** (nice-to-have but not required)

### Milestone Markers
Group tasks into checkpoints:
- ✅ Checkpoint 1: Data is loaded (Days 1-3)
- ✅ Checkpoint 2: Analysis complete (Days 4-12)
- ✅ Checkpoint 3: Paper drafted (Days 13-15)
- ✅ Checkpoint 4: Submitted (Days 16-17)

---

## Specific Guidance for Agent Output

### For the Walkthrough Document:
- Write in second person ("You will now...")
- Include code snippets where helpful
- Anticipate questions and address them proactively
- Use clear section headers with emoji markers for skimmability
- Include "If this fails..." troubleshooting branches

### For the Knowledge Bank:
- Organize by topic, not chronologically
- Include examples for every formula
- Create a "Quick Reference" section at the top
- Use tables for comparing options (e.g., Parquet vs CSV)
- Link to external resources (documentation, tutorials)

### For the Linear Task List:
- Number tasks 1-50+ (whatever is needed)
- Use checkbox format [ ] for tracking
- Estimate REALISTIC time (students underestimate)
- Bold the deliverable for each task
- Group by day if possible (Day 1: Tasks 1-5)

---

## Emergency Context (If Student Gets Stuck)

### Week 1 Crisis: "Data won't load"
- Provide step-by-step environment setup
- Alternative data formats (Parquet vs CSV)
- Sample code that WILL work

### Week 2 Crisis: "Don't understand time series"
- Simplify to daily aggregates instead of hourly
- Use only ONE region to reduce complexity
- Focus on volatility (std dev) instead of forecasting

### Week 3 Crisis: "Running out of time"
- Reduce scope to one strong finding
- Provide paper outline template with bullet points
- Prioritize the "money chart" (demand + forecast + buffer)

---

## Final Instructions for Agent

### Tone and Style
- **Walkthrough:** Encouraging but realistic. Acknowledge difficulty but emphasize achievability.
- **Knowledge Bank:** Clinical and precise. This is a reference document, not a tutorial.
- **Task List:** Direct and actionable. Use imperative verbs (Load, Calculate, Plot, Write).

### Assumptions You Can Make
- Student has Jupyter Notebook working
- Student has Git installed
- Student can read Python/SQL code
- Student does NOT have prior research paper experience
-  Student has used LaTeX before but needs help

### Assumptions You Cannot Make
- Student knows what "ACM format" means
- Student understands time series terminology and typical EDA practices
- Student knows how to cite papers properly

### Critical Success Factors to Emphasize
1. **Start immediately** (Day 1 actions must be crystal clear)
2. **Visualize early** (plots reveal patterns faster than tables)
3. **Simple beats complex** (moving average > LSTM)
4. **Document assumptions** (paper quality depends on this)
5. **Submit on time** (late = disqualified)

---

## Your Deliverables Checklist

When you complete your analysis, ensure you have generated:

- [x] **Walkthrough Document** (10-15 pages, comprehensive) ✅ 2026-01-12
  - Covers all 4 phases
  - Includes code examples
  - Addresses common pitfalls
  - Has quality checkpoints

- [x] **Knowledge Bank** (.md format, 5-8 pages) ✅ 2026-01-12
  - Quick reference section at top
  - Organized by category
  - Includes all formulas with examples
  - Links to external resources

- [x] **Linear Task List** (50+ numbered tasks) ✅ 2026-01-12
  - Day-by-day breakdown
  - Clear success criteria for each
  - Dependencies marked
  - Time estimates included

---

## Recommended Planning Mode Approach

1. **First Pass:** Read all three source documents completely
2. **Second Pass:** Extract all unique information (deduplicate)
3. **Third Pass:** Organize by workflow phase
4. **Fourth Pass:** Identify gaps and add clarifying content
5. **Fifth Pass:** Create the three deliverables with cross-references

Use your planning mode to structure this logically. The student needs to feel like they have a clear path forward, not just a pile of information.

Good luck, Agent. This project matters for the student's career trajectory.