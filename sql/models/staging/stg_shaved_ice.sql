-- Model 1: Staging - Load and clean raw Shaved Ice data
-- This model loads the raw CSV and performs basic cleaning
-- 
-- Resume talking point: "Used dbt to build a staging layer that 
-- ingests raw CSV data into DuckDB for reproducible transformations"

{{ config(materialized='table') }}

WITH source AS (
    -- Load raw CSV directly using DuckDB's read_csv_auto
    -- Update the path after downloading the dataset
    SELECT * FROM read_csv_auto(
        'data/raw/shavedice-dataset/*.csv',  -- Adjust path as needed
        header = true,
        timestampformat = '%Y-%m-%d %H:%M:%S'
    )
),

cleaned AS (
    SELECT
        -- Standardize column names (adjust based on actual schema)
        *,
        -- Add row-level data quality flag
        CASE 
            WHEN demand IS NULL OR demand < 0 THEN 'invalid'
            ELSE 'valid'
        END AS data_quality_flag
    FROM source
)

SELECT * FROM cleaned
WHERE data_quality_flag = 'valid'
