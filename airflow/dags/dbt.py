from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator

from airflow.operators.bash_operator import BashOperator

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
    'dbt',
    schedule_interval='0 0 * * *', default_args=default_args
)
debug = BashOperator(
            task_id= "DBT_debug",
            bash_command="cd /dbt && dbt debug",
            dag=dag,
)
run = BashOperator(
            task_id= "DBT_run",
            bash_command="cd /dbt && dbt run",
            dag=dag,
)
test = BashOperator(
            task_id= "DBT_test",
            bash_command="cd /dbt && dbt test",
            dag=dag,
)
generate_docs = BashOperator(
    task_id='generate_docs',
    bash_command='cd /dbt && dbt docs generate',
    dag=dag
)

debug>>run>>test
run>>generate_docs