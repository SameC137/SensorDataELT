{{ config(materialized='table') }}
with stations as (
    select
        *
    from {{ source('station_sensors', 'station_info') }}
)


select * from stations