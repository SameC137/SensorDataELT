
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator

from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
# from airflow.hooks.mysql_hook import MySqlHook

from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import pandas as pd
import numpy as np
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
    task_id='create_sensor_data_table_mysql',
    mysql_conn_id='mysql_conn_id',
    sql='create table if not exists dbtdb.sensor_data(sense_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,\
         time DATETIME, station_id int, col3 float, col4 float, col5 float, col6 float, col7 float, \
        col8 float, col9 float, col10 float, col11 float, col12 float, col13 float, col14 float, col15 float, col16 float, \
        col17 float, col18 float, col19 float, col20 float, col21 float, col22 float, \
        col23 float, col24 float, col25 float, col26 float,FOREIGN KEY (station_id)\
        REFERENCES station_info(station_id)\
        ON DELETE CASCADE)',
    dag=dag
)

task2 = MySqlOperator(
    task_id='create_station_table_mysql',
    mysql_conn_id='mysql_conn_id',
    sql='create table if not exists dbtdb.station_info(station_id int,Fwy int,Dir ENUM("E","W","N","S"),District int,County int,City float,State_PM float,Abs_PM float,Latitude float,Longitude float,Length float,Type varchar(2),Lanes int,Name varchar(255),User_ID_1 varchar(255),User_ID_2 varchar(255),User_ID_3 int,User_ID_4 float)',
    dag=dag
)

def load_station_data():
    mysql = MySqlHook("mysql_conn_id")
    station_data=pd.read_csv("../data/I80_stations.csv")
    station_data = station_data.replace(np.nan, "'NULL'")
    sql = "INSERT INTO dbtdb.station_info VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for i,row in station_data.iterrows():
        print(row)
        conn = mysql.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(row))
        conn.commit()

def load_data():
    with open("../data/I80_sample.txt") as myfile:
        hook=MySqlHook("mysql_conn_id")
        for line in myfile:
            # sql1="insert into test1 values ({})".format(line)
            split_line=line.strip().split(",")


            values=[]
            for i in split_line:
                if i=="":
                    values.append("NULL")
                else:
                    values.append(i)
            values[0]=str(dt.strptime( values[0], '%m/%d/%Y %H:%M:%S'))
            values[0]= f'"{values[0]}"'
        # .strftime("%Y-%m-%d %H:%M:%S")
            values_string=" , ".join(values)
            sql=f"INSERT INTO `sensor_data` (`time`, `station_id`, `col3`, `col4`, `col5`, `col6`, `col7`, `col8`, `col9`, `col10`, `col11`, `col12`, `col13`, `col14`, `col15`, `col16`, `col17`, `col18`, `col19`, `col20`, `col21`, `col22`, `col23`, `col24`, `col25`, `col26`)VALUES ({values_string});"
            # hook.insert_rows(table="sensor_data", rows=[",".join(values)])
            hook.run(sql,autocommit=True)

add_data=PythonOperator(
    
    task_id='load_sensor_data', 
    python_callable=load_data, 
    dag=dag
)
       
station=PythonOperator(
    task_id='load_station_data', 
    python_callable=load_station_data, 
    dag=dag
)

task2>>station>>mysql_task>>add_data