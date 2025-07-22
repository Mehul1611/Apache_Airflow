from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime


default_args={
    'start_date': datetime(2025,7,21)
}

def channel_function():
    print("Logic for the Branch Master DAG function comes here")

with DAG('channel_mst', default_args=default_args, catchup=False) as dag2:
    channel_dag = BashOperator(
        task_id='ChannelMasterDAG', 
        bash_command='sleep 3')
    
    channel_master_function = PythonOperator(
        task_id='ChannelFunction',
        python_callable=channel_function
        )
    
channel_dag>>channel_master_function