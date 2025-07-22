from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

default_args={
    'start_date': datetime(2025,7,21)
}

def function_master():
    print("Logic for the Master DAG function comes here")

with DAG('master_dag', default_args=default_args, catchup=False) as dag:
    start = PythonOperator(
        task_id='START', 
        python_callable=function_master)
    
    product_mst_etl = TriggerDagRunOperator(
        task_id = 'ProductMasterDAG',
        trigger_dag_id='product_mst_dag',
        conf={"run_date": "{{ ds }}"},     #### ds is built in airflow variable to execution date as YYYY-MM-DD
        reset_dag_run=True,             #### Reset DAG status for mitigation of multiple run failure.
        wait_for_completion=True,       #### Ensure the task wait for completion of the dag being triggered
        poke_interval=10,                #### Check whether the triggered dag is completed after every 3secs interval.
    )

    branch_mst_etl = TriggerDagRunOperator(
        task_id = 'BranchMasterDAG',
        trigger_dag_id='branch_mst_dag',
        conf={"run_date": "{{ ds }}"},
        reset_dag_run=True,        
        wait_for_completion=True, 
        poke_interval=10, 
    )

    channel_mst_etl = TriggerDagRunOperator(
        task_id = 'ChannelMasterDAG',
        trigger_dag_id='channel_mst',
        conf={"run_date": "{{ ds }}"},
        reset_dag_run=True,        
        wait_for_completion=True, 
        poke_interval=10, 
    )

    end = EmptyOperator(task_id="END")

start>>[branch_mst_etl, product_mst_etl]>>channel_mst_etl>>end