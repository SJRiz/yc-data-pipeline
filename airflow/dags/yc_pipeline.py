from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl.extract import extract_yc_data
from etl.transform import transform_yc_data
from etl.load import load_to_postgres

with DAG("yc_etl", start_date=datetime(2025,7,29), schedule="@daily", catchup=False) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract_yc_data)
    t2 = PythonOperator(task_id="transform", python_callable=transform_yc_data)
    t3 = PythonOperator(task_id="load", python_callable=load_to_postgres)
    t1 >> t2 >> t3