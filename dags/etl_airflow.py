# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime

# with DAG(
#     dag_id="hello_airflow",
#     start_date=datetime(2023, 1, 1),
#     schedule_interval="@daily",
#     catchup=False,
# ) as dag:

#     hello = BashOperator(
#         task_id="say_hello",
#         bash_command="echo 'Hello, Airflow!'"
#     )
## To initialise the DAG object
from airflow import DAG
## Operators are require to perform variopus data transformation operations
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime   ### date from which the dag should execute

## Basic DAG parameters:
def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 7, 14)
}


##DAG OBJECT:
with DAG("ETL",
        catchup=False,
        default_args=def_args) as dag:
    
    ## various operations by dummy processes ------- here we can call our normal python functions for data transformations.
    start=EmptyOperator(task_id="START")
    e=EmptyOperator(task_id="EXTRACT")
    t=EmptyOperator(task_id="TRANSFORM")
    l=EmptyOperator(task_id="LOAD")
    end=EmptyOperator(task_id="END")

start >> e >> t >> l >> end ###order of execution