from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

class ELTLogic():
    def __init__(self):
        self.def_args = {
            "owner": "airflow",
            "retries": 0,
            "retry_delay": timedelta(minutes=1),
            "start_date": datetime(2022, 6, 15)
        }

    def extract_function(self):
        print("This is the Extraction Logic")
    
    def transform_function(self, num):
        print("This is the Transformation Step")
        print(f"Value of Number is: {num}")
    
    def load_function(self, num1, num2):
        print("Logic to Load the data")
        print(f"The value of number 1: {num1}\nThe value of number 2: {num2}\n")

    def run_dag(self):
        with DAG("example_py_operator", default_args=self.def_args, catchup=False) as dag:
            
            #Initialize the dag object
            start = EmptyOperator(task_id= "START")
            
            #Call the extract function by assigning task_id and PythonOP
            ext = PythonOperator(
                task_id="EXTRACT",
                python_callable=self.extract_function
            )

            #Call the transform function by giving additional args
            trnsfm = PythonOperator(
                task_id="Transform",
                python_callable=self.transform_function,
                op_args=[1234567890]
            )

            #Call the load function(Can pass args in 2 ways)
            load = PythonOperator(
                task_id="Load",
                python_callable=self.load_function,
                op_args=[1234567890, 9876543210],       # ------> Way 1 (to pass the parameters in the same sequence)
                # op_kwargs={
                #     "num1":"Negative number",
                #     "num2":"Positive number"            # ------> Way 2 (Key-Value pair mapping)
                # }
            )

            end = EmptyOperator(task_id= "END")

            start >> ext >> trnsfm >> load >> end
        return dag 
    
etl = ELTLogic()
dag = etl.run_dag()