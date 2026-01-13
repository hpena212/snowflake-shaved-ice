-- Model 2: Intermediate - Daily aggregations with time features
--
-- Resume talking point: "Built intermediate transformations with 
-- window functions and date/time feature engineering for time series analysis"

{{ config(materialized='table') }}

WITH hourly_data AS (
    SELECT * FROM {{ ref('stg_shaved_ice') }}
),

daily_agg AS (
    SELECT
        -- Time dimension
        DATE_TRUNC('day', timestamp) AS date,
        region,
        instance_type,
        
        -- Demand aggregations
        SUM(demand) AS daily_demand_total,
        AVG(demand) AS daily_demand_avg,
        MAX(demand) AS daily_demand_max,
        MIN(demand) AS daily_demand_min,
        COUNT(*) AS hourly_records,
        
        -- Variance for safety stock calculations
        STDDEV(demand) AS daily_demand_stddev

    FROM hourly_data
    GROUP BY DATE_TRUNC('day', timestamp), region, instance_type
),

with_time_features AS (
    SELECT
        *,
        -- Time features for forecasting
        EXTRACT(YEAR FROM date) AS year,
        EXTRACT(MONTH FROM date) AS month,
        EXTRACT(DOW FROM date) AS day_of_week,
        EXTRACT(WEEK FROM date) AS week_of_year,
        
        -- Binary flags
        CASE WHEN EXTRACT(DOW FROM date) IN (0, 6) THEN 1 ELSE 0 END AS is_weekend,
        
        -- Lag features (partitioned by region and instance type)
        LAG(daily_demand_total, 1) OVER (
            PARTITION BY region, instance_type 
            ORDER BY date
        ) AS demand_lag_1d,
        
        LAG(daily_demand_total, 7) OVER (
            PARTITION BY region, instance_type 
            ORDER BY date
        ) AS demand_lag_7d,
        
        -- Rolling averages
        AVG(daily_demand_total) OVER (
            PARTITION BY region, instance_type
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS demand_rolling_7d_avg

    FROM daily_agg
)

SELECT * FROM with_time_features
ORDER BY date, region, instance_type
