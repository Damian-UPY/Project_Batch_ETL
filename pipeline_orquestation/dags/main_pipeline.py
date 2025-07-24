from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os
from pymongo import MongoClient

default_args = {
    'owner': 'DamianNovelo',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG('main_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    def log_start():
        print("Pipeline started")
    PythonOperator(task_id='start', python_callable=log_start)
