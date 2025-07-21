from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
# from utils.plugin_connection import use_postgres_connection, ensure_postgres_connection
from hooks.update_data import Hooks
from datetime import datetime

def run_dag():
        def_args={
            "owner": "airflow",
            "start_date": datetime(2025, 6, 16)
        }
        pg_hook=Hooks()
        with DAG("PgHook_dag", default_args=def_args, catchup=False) as dag:
            start = EmptyOperator(task_id= "START")
            etl = PythonOperator(
                task_id="Load",
                python_callable=pg_hook.run_etl_pipeline,
                )
            # check_or_create_conn = PythonOperator(
            #         task_id="ensure_connection",
            #         python_callable=ensure_postgres_connection
            #     )

            # use_conn = PythonOperator(
            #         task_id="use_connection",
            #         python_callable=use_postgres_connection
            #     )
            end = EmptyOperator(task_id= "END")

            # start >> check_or_create_conn >> use_conn >> etl >> end
            start >> etl >> end

        return dag 

run_dag()