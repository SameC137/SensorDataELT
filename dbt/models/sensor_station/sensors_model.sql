{{ config(materialized='table') }}

with sensors as (
select * from {{ source('station_sensors', 'sensor_data') }}

)


select * from sensors