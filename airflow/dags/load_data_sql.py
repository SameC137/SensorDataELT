from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator

from datetime import datetime as dt

from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.now(),
    'email_on_failure': False,
    'email_on_retry': False,    
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'load_data_sql',
    schedule_interval='0 0 * * *', default_args=default_args
)


create_station = MySqlOperator(
    task_id='create_station_table',
    mysql_conn_id="mysql_conn_id",
    sql='./create_station.sql',
    dag=dag
)


create_sensor = MySqlOperator(
    task_id='create_sensor_table',
    mysql_conn_id="mysql_conn_id",
    sql='./create_sensor_data.sql',
    dag=dag
)


insert_station = MySqlOperator(
    task_id='insert_station_table',
    mysql_conn_id="mysql_conn_id",
    sql='./insert_station_data.sql',
    dag=dag
)


insert_sensor = MySqlOperator(
    task_id='insert_sensor_table',
    mysql_conn_id="mysql_conn_id",
    sql='./insert_sensor_data.sql',
    dag=dag
)

create_station>>create_sensor>>insert_station>>insert_sensor