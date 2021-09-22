
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator

from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook

from datetime import datetime as dt
from datetime import timedelta
from datetime import date

# from airflow import settings
# from airflow.models import Connection

# conn = Connection(
#         conn_id="mysql_conn_id",
#         conn_type="mysql",
#         host="mysqldb",
#         login="root",
#         password="root",
#         port="3306"
# ) #create a connection object
# session = settings.Session() # get the session
# session.add(conn)
# session.commit()


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

mysql_task = MySqlOperator(
    task_id='create_table_mysql_external_file',
    mysql_conn_id='mysql_conn_id',
    sql='create table if not exists dbtdb.sensor_data(sense_id int NOT NULL PRIMARY KEY,date Date, time Time, station_id int, col3 float, col4 float, col5 float, col6 float, col7 float, col8 float, col9 float, col10 float, col11 float, col12 float, col13 float, col14 float, col15 float, col16 float, col17 float, col18 float, col19 float, col20 float, col21 float, col22 float, col23 float, col24 float, col25 float, col26 float)',
    dag=dag
)

task2 = MySqlOperator(
    task_id='create_table_mysql',
    mysql_conn_id='mysql_conn_id',
    sql='create table if not exists dbtdb.session(sense_id int NOT NULL PRIMARY KEY,date Date, time Time, station_id int, col3 float, col4 float, col5 float, col6 float, col7 float, col8 float, col9 float, col10 float, col11 float, col12 float, col13 float, col14 float, col15 float, col16 float, col17 float, col18 float, col19 float, col20 float, col21 float, col22 float, col23 float, col24 float, col25 float, col26 float)',
    dag=dag
)

def load_data():
    with open("../data/I80_davis.txt") as myfile:
        hook=MySqlHook("mysql_conn_id")
        for line in myfile:
            # sql1="insert into test1 values ({})".format(line)
            
            hook.insert_rows(table="sensor_data", rows=line)
    
            break

add_data=PythonOperator(
    
    task_id='load_sensor_data', 
    python_callable=load_data, 
    dag=dag
)
       


mysql_task>>add_data