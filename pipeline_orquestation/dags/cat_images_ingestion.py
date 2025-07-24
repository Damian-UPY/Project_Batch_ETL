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
with DAG('cat_images_ingestion', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    def extract_images(**kwargs):
        url = 'https://api.thecatapi.com/v1/images/search?limit=10'
        data = requests.get(url).json()
        kwargs['ti'].xcom_push(key='images_data', value=data)

    PythonOperator(task_id='extract_images', python_callable=extract_images, provide_context=True)
