from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable

xyz = Variable.get("AWS_SECRET_KEY")
json_obj = Variable.get("DB_CONN_VARS")
dict_obj = Variable.get("DB_CONN_VARS", deserialize_json=True)    ### Must be done to convert the json obj to python dict or str to its default dtype.
pwd = Variable.get("DB_PASSWORD")

def print_airflow_variables():
    print(f"AWS_Secret_Key: {xyz}; Datatype: {type(xyz)}")
    print(f"Json_obj value: {json_obj}; Datatype: {type(json_obj)}")
    print(f"Dict_obj value: {dict_obj}; Datatype: {type(dict_obj)}")
    print(f"'DB_HOST_IP' in dict_obj: {dict_obj['DB_HOST_IP']}")
    print(f"Password: {pwd}; Datatype: {type(pwd)}")
    return None

def_args = {
    "owner": "airflow",
    "retries": 0,
    "start_date": datetime(2025, 7, 21)
}

with DAG("airflow_variables", default_args=def_args, catchup=False) as dag:
    start = EmptyOperator(task_id="START")

    airflow_variables = PythonOperator(
        task_id="AIRFLOW_VARIABLES",
        python_callable=print_airflow_variables
    )

    end = EmptyOperator(task_id="END")

    start >> airflow_variables >> end
