from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime


default_args={
    'start_date': datetime(2025,7,21)
}

def product_function():
    print("Logic for the Product Master DAG function comes here")

with DAG('product_mst_dag', default_args=default_args, catchup=False) as dag1:
    prod_etl = BashOperator(
        task_id='ProductMasterDAG', 
        bash_command='sleep 3'
        )
    
    prod_function = PythonOperator(
        task_id='ProductFunction',
        python_callable=product_function
        )
    
prod_etl>>prod_function