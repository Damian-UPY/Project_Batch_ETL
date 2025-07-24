from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from pymongo import MongoClient

default_args = {
    'owner': 'DamianNovelo',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('load_mongo', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    def load_data(**kwargs):
        # Recuperar datos desde XComs
        breeds = kwargs['ti'].xcom_pull(key='breeds_data', task_ids='extract_breeds')
        images = kwargs['ti'].xcom_pull(key='images_data', task_ids='extract_images')
        categories = kwargs['ti'].xcom_pull(key='categories_data', task_ids='extract_categories')

        consolidated = {
            'breeds': breeds or [],
            'images': images or [],
            'categories': categories or []
        }

        # ✅ Conexión segura a MongoDB
        mongo_uri = os.getenv(
            'MONGO_URI',
            'mongodb://root:example@mongodb:27017/project_db?authSource=admin'
        )
        client = MongoClient(mongo_uri)

        # Obtener base de datos y colección
        db = client.get_database()
        collection_name = os.getenv('MONGO_COLLECTION', 'cats_dataset')
        collection = db[collection_name]

        # Insertar datos
        collection.insert_one(consolidated)
        print(f"✅ Inserted consolidated dataset into '{collection_name}' in MongoDB")

    # Crear la tarea en Airflow
    PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True
    )
