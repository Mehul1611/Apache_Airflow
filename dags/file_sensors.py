from datetime import datetime
from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
import os

PATH = "/opt/airflow/dags/data"

def file_exists(path):
    """Check if any .json file exists in the specified path."""
    return any(f.endswith(".md") for f in os.listdir(path))

def process_file(path):
    print(f'Current working directory: {os.getcwd()}')
    print(f"Processing files in: {path}")

default_args = {
    "owner": "airflow",
    "retries": 0,
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    dag_id='file_sensor',
    default_args=default_args,
    description='A sample DAG using PythonSensor instead of FileSensor',
    catchup=False,
) as dag:

    # Task 1: Wait until any .json file appears
    wait_for_file = PythonSensor(
        task_id='wait_for_file',
        python_callable=file_exists,
        op_args=[PATH],
        poke_interval=10,
        timeout=600,
        mode='reschedule',
    )

    # Task 2: Process the file
    process_file_task = PythonOperator(
        task_id='process_file',
        python_callable=process_file,
        op_kwargs={'path': PATH},
    )

wait_for_file >> process_file_task
