from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


global_var = "XCom demo"

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
        print (f"Value of the Global Variable is: {global_var}")
        value = "Extracted value from source"
        return value
        ## creating a DataFrame object ----- This cannot be returned directly
        # details = {
        #     "cust_id": [1,2,4,5,3],
        #     "Name": ['GKMIT', 'Mehul', 'Airflow']
        # }
        # df = pd.DataFrame(details)
        # return df

    def transform_function(self, num, **kwargs):   #### Add a new task instance to pass the variables
        print("This is the Transformation Step")
        print(f"Value of Number is: {num}")

        task_inst = kwargs['ti']  # TaskInstance object from context
        xcom_pull_obj = task_inst.xcom_pull(task_ids = ["EXTRACT"])
        print(f"Type of xcom_pull_obj is {type(xcom_pull_obj)}")
        
        extrct_val = xcom_pull_obj[0]
        print(f"The value of xcom pull object is {extrct_val}")
        return 10
    
    def load_function(self, num1, num2, **kwargs):  
        print("Logic to Load the data")
        print(f"The value of number 1: {num1}\nThe value of number 2: {num2}\n")

        task_inst = kwargs['ti']  # TaskInstance object from context
        xcom_pull_obj = task_inst.xcom_pull(task_ids = ["Transform"])
        print(f"Type of xcom_pull_obj is {type(xcom_pull_obj)}")

        extrct_val = xcom_pull_obj[0]
        print(f"The value of xcom pull object is {extrct_val}")
        return 20

    def run_dag(self):
        with DAG("example_py_operator1", default_args=self.def_args, catchup=False) as dag:
            start = EmptyOperator(task_id= "START")
            ext = PythonOperator(
                task_id="EXTRACT",
                python_callable=self.extract_function,
                # do_xcom_push = True   ## By default this parameter is True
            )
            trnsfm = PythonOperator(
                task_id="Transform",
                python_callable=self.transform_function,
                op_args=[1234567890],
                # op_kwargs={
                #     "num":1234567890,
                #     "task_inst": "{{ ti }}"
                # },
                do_xcom_push = True
            )
            load = PythonOperator(
                task_id="Load",
                python_callable=self.load_function,
                op_args=[1234567890, 9876543210],
                # op_kwargs={
                #     "num1":"Negative number",
                #     "num2":"Positive number",
                #     "task_inst": "{{ ti }}"
                # }
            )
            end = EmptyOperator(task_id= "END")
            start >> ext >> trnsfm >> load >> end
        return dag 
    
etl = ELTLogic()
dag = etl.run_dag()