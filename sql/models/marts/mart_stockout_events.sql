-- models/marts/mart_stockout_events.sql
{{ config(materialized='table') }}

WITH base AS (
    SELECT * FROM {{ ref('int_daily_demand') }}
),

calculations AS (
    SELECT 
        date,
        region,
        instance_type,
        daily_demand_total as demand,
        daily_demand_max,
        -- Define capacity as the 95th percentile safety stock level
        (daily_demand_avg + 1.645 * daily_demand_stddev) as capacity_limit_p95,
        -- Calculate severity
        (daily_demand_max - (daily_demand_avg + 1.645 * daily_demand_stddev)) / 
            NULLIF((daily_demand_avg + 1.645 * daily_demand_stddev), 0) as severity_pct
    FROM base
)

SELECT * FROM calculations
WHERE severity_pct > 0 -- Only show days where we exceeded capacity