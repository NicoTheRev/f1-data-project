-- models/staging/stg_sessions.sql

with source_sessions as (
    -- Usamos la macro source (sin llaves en el comentario) para heredar la configuración del yml
    select * from {{ source('f1_raw', 'ext_sessions') }}
)

select
    -- Convertimos identificadores a tipos numéricos fijos
    cast(session_key as INT64) as session_id,
    cast(circuit_key as INT64) as circuit_id,
    
    -- Limpieza y estandarización de cadenas de texto
    cast(session_name as STRING) as session_name,
    cast(session_type as STRING) as session_type,
    cast(circuit_short_name as STRING) as circuit_name,
    cast(country_name as STRING) as country_name,
    
    -- Casteo correcto de campos de tiempo a Timestamps reales
    cast(date_start as TIMESTAMP) as session_started_at,
    cast(date_end as TIMESTAMP) as session_ended_at

from source_sessions