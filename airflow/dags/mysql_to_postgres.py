from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.generic_transfer import GenericTransfer

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
    'load_data',
    schedule_interval='0 0 * * *', default_args=default_args
)
sql = "SELECT * FROM station_info LIMIT 100;"
mysql_to_postgress=GenericTransfer(
        task_id='test_m2p', preoperator=[
            "DROP TABLE IF EXISTS station_info",
            "CREATE TABLE IF NOT EXISTS "
            "station_info (LIKE INFORMATION_SCHEMA.TABLES)"
        ],
        source_conn_id='mysql_conn_id',
        destination_conn_id='postgres_conn_id',
        destination_table="station_info",
        sql=sql,
        dag=dag)

mysql_to_postgress