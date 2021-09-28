from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.generic_transfer import GenericTransfer
from airflow.operators.postgres_operator import PostgresOperator

from datetime import datetime as dt

from datetime import timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt(2021, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,    
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    'transfer_data',
    schedule_interval='0 0 * * *', default_args=default_args
)

station_info = PostgresOperator(task_id='create_station_info_table',
                      sql="./postgres_sql/create_station_postgres.sql",
                      postgres_conn_id='postgres_conn_id',
                      autocommit=True,
                      database="dbtdb",
                      dag=dag)

sql = "SELECT * FROM station_info LIMIT 100;"
mysql_to_postgress_station_info=GenericTransfer(
        task_id='m2p_station_info', 
        source_conn_id='mysql_conn_id',
        destination_conn_id='postgres_conn_id',
        destination_table="station_info",
        sql=sql,
        dag=dag)


station_summary = PostgresOperator(task_id='create_station_summary_table',
                      sql="./postgres_sql/create_station_summary_postgress.sql",
                      postgres_conn_id='postgres_conn_id',
                      autocommit=True,
                      database="dbtdb",
                      dag=dag)
mysql_to_postgress_station_summary=GenericTransfer(
        task_id='m2p_station_summary', 
        source_conn_id='mysql_conn_id',
        destination_conn_id='postgres_conn_id',
        destination_table="station_summary",
        sql="SELECT * FROM station_summary",
        dag=dag)

sensor_data = PostgresOperator(task_id='create_sensor_table',
                      sql="./postgres_sql/create_sensor_data_postgres.sql",
                      postgres_conn_id='postgres_conn_id',
                      autocommit=True,
                      database="dbtdb",
                      dag=dag)
mysql_to_postgress_sensor=GenericTransfer(
        task_id='m2p_sensor_data', 
        source_conn_id='mysql_conn_id',
        destination_conn_id='postgres_conn_id',
        destination_table="sensor_data",
        sql="SELECT * FROM sensor_data",
        dag=dag)

station_info>>mysql_to_postgress_station_info>>station_summary>>mysql_to_postgress_station_summary
mysql_to_postgress_station_info>>sensor_data>>mysql_to_postgress_sensor