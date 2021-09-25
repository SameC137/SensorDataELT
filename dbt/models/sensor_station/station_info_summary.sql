{{ config(materialized='table') }}
with station_info_summary as (
    select 
        {{ ref('station_summary_model') }}.station_id,
        {{ ref('station_summary_model') }}.flow_99,
        {{ ref('station_summary_model') }}.flow_max,
        {{ ref('station_summary_model') }}.flow_median,
        {{ ref('station_summary_model') }}.flow_total,
        {{ ref('station_summary_model') }}.n_obs
    from {{ ref('station_summary_model') }}
     join {{ ref('stations_model') }} on {{ ref('stations_model') }}.station_id= {{ ref('station_summary_model') }}.station_id
)




select * from station_info_summary