# airflow related
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

# other packages
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from airflow.utils import timezone

now = timezone.utcnow()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt(2021, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,    
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

def read_unprocessed_data_from_s3():
    print("reading unprocessed data completed i think")
    pass
    # code that reads audio data kafka
    
def spark_audio_processing():
    print("spark audio processing completed")
    pass
    

def save_processed_audio_to_s3():
    print("saving to audio s3 bucket")

    pass
    


with DAG( catchup=False, dag_id='audio_processing_dag', schedule_interval='*/1 * * * *', description='Amharic speech data audio processing dag', default_args=default_args) as dag:
  
  read_unprocessed_data_from_s3 = PythonOperator(
    task_id='read_unprocessed_data_from_s3', 
    python_callable=read_unprocessed_data_from_s3, 
    dag=dag)

  spark_audio_processing = PythonOperator(
    task_id='spark_audio_processing', 
    python_callable=spark_audio_processing, 
    dag=dag)

  # spark_audio_processing = PythonOperator(
  #   task_id='spark_audio_processing', 
  #   python_callable=spark_audio_processing, 
  #   op_kwargs = {'config' : config},
  #   provide_context=True,
  #   dag=dag
  # )

  save_processed_audio_to_s3 = PythonOperator(
    task_id='save_processed_audio_to_s3', 
    python_callable=save_processed_audio_to_s3, 
    dag=dag)

  # spark_job = BashOperator(
  #   task_id='spark_task_etl',
  #   bash_command='spark-submit --master spark://localhost:7077 spark_job.py',
  #   dag = dag)

  # setting dependencies


  read_unprocessed_data_from_s3 >> spark_audio_processing
  spark_audio_processing >> save_processed_audio_to_s3