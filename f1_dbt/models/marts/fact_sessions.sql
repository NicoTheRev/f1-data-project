-- models/marts/fact_sessions.sql

{{ config(
    materialized='table'
) }}

with staging_sessions as (
    -- Traemos los datos limpios de la capa de staging
    select * from {{ ref('stg_sessions') }}
)

select
    session_id,          -- Llave foránea que conecta con futuros hechos de telemetría
    circuit_id,          -- Llave foránea que conecta directamente con dim_circuits
    session_name,
    session_type,
    session_started_at,
    session_ended_at,
    
    timestamp_diff(session_ended_at, session_started_at, MINUTE) as session_duration_minutes

from staging_sessions