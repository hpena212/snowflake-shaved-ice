-- Model 3: Mart - Final table ready for Python forecasting
-- Clean, analysis-ready dataset with all features needed for modeling
--
-- Resume talking point: "Created a mart layer as the single source of truth
-- for forecasting models, decoupling data engineering from data science"

{{ config(materialized='table') }}

WITH daily_data AS (
    SELECT * FROM {{ ref('int_daily_demand') }}
),

forecast_ready AS (
    SELECT
        -- Key dimensions
        date,
        year,
        month,
        day_of_week,
        week_of_year,
        is_weekend,
        
        -- Target variable
        daily_demand_total AS demand,
        
        -- Features for forecasting
        daily_demand_avg,
        daily_demand_max,
        daily_demand_min,
        daily_demand_stddev,
        peak_hours_max,
        
        -- Lag features
        demand_lag_1d,
        demand_lag_7d,
        demand_rolling_7d_avg,
        
        -- Safety stock metrics
        daily_demand_stddev * 1.65 AS safety_stock_90pct,  -- 90% service level
        daily_demand_stddev * 1.96 AS safety_stock_95pct,  -- 95% service level
        daily_demand_stddev * 2.58 AS safety_stock_99pct,  -- 99% service level
        
        -- Data quality
        hourly_records,
        CASE WHEN hourly_records = 24 THEN 1 ELSE 0 END AS complete_day_flag

    FROM daily_data
    -- Only include days with valid lag features
    WHERE demand_lag_7d IS NOT NULL
)

SELECT * FROM forecast_ready
ORDER BY date
