-- models/marts/dim_circuits.sql

{{ config(
    materialized='table'
) }}

with staging_sessions as (
    select * from {{ ref('stg_sessions') }}
),

distinct_circuits as (
    select distinct
        circuit_id,
        circuit_name,
        country_name
    from staging_sessions
)

select * from distinct_circuits