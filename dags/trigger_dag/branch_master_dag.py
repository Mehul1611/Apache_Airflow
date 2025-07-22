from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowFailException
from datetime import datetime


default_args={
    'start_date': datetime(2025,7,21)
}

def branch_function():
    print("Logic for the Branch Master DAG function comes here")

with DAG('branch_mst_dag', default_args=default_args, catchup=False) as dag2:
    branch_dag = BashOperator(
        task_id='BranchMasterDAG', 
        bash_command='sleep 3')
    
    branch_master_function = PythonOperator(
        task_id='BranchFunction',
        python_callable=branch_function
        )
    
branch_dag>>branch_master_function