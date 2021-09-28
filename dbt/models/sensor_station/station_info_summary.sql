{{ config(materialized='table') }}
with station_info_summary as (
    select 
{{ ref('station_summary_model') }}.summary_id,	
{{ ref('station_summary_model') }}.station_id,	
{{ ref('station_summary_model') }}.flow_99,	
{{ ref('station_summary_model') }}.flow_max,	
{{ ref('station_summary_model') }}.flow_median,	
{{ ref('station_summary_model') }}.flow_total,	
{{ ref('station_summary_model') }}.n_obs,
{{ ref('stations_model') }}.Fwy,
{{ ref('stations_model') }}.Dir,
{{ ref('stations_model') }}.District,	
{{ ref('stations_model') }}.County,
{{ ref('stations_model') }}.City,	
{{ ref('stations_model') }}.State_PM,	
{{ ref('stations_model') }}.Abs_PM,	
{{ ref('stations_model') }}.Latitude,	
{{ ref('stations_model') }}.Longitude,	
{{ ref('stations_model') }}.Length,	
{{ ref('stations_model') }}.Type,
{{ ref('stations_model') }}.Lanes,	
{{ ref('stations_model') }}.Name,		
{{ ref('stations_model') }}.User_ID_1,	
{{ ref('stations_model') }}.User_ID_2,		
{{ ref('stations_model') }}.User_ID_3,		
{{ ref('stations_model') }}.User_ID_4
    from {{ ref('station_summary_model') }}
     join {{ ref('stations_model') }} on {{ ref('stations_model') }}.station_id= {{ ref('station_summary_model') }}.station_id
)




select * from station_info_summary