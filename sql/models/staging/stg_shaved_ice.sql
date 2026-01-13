-- Model 1: Staging - Load and clean raw Shaved Ice data
-- 
-- Resume talking point: "Used dbt to build a staging layer that 
-- ingests raw Parquet data into DuckDB for reproducible transformations"

{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM read_parquet(
        'data/raw/shavedice-dataset/hourly_normalized.parquet'
    )
),

cleaned AS (
    SELECT
        -- Rename columns for clarity
        USAGE_HOUR AS timestamp,
        REGION_NUM AS region,
        INSTANCE_TYPE AS instance_type,
        NORM_USAGE AS demand,
        
        -- Data quality flag
        CASE 
            WHEN NORM_USAGE IS NULL OR NORM_USAGE < 0 THEN 'invalid'
            ELSE 'valid'
        END AS data_quality_flag
    FROM source
)

SELECT * FROM cleaned
WHERE data_quality_flag = 'valid'
