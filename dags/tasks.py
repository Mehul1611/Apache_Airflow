from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

with DAG("TaskScheduler", default_args={"owner": "airflow", "start_date": datetime(2025, 7, 21)}) as dag:
    
    start=EmptyOperator(task_id="START")
    # a=EmptyOperator(task_id="TASK_A")
    # a1=EmptyOperator(task_id="TASK_A1")
    # b=EmptyOperator(task_id="TASK_B")
    # c=EmptyOperator(task_id="TASK_C")
    # d=EmptyOperator(task_id="TASK_D")
    # e=EmptyOperator(task_id="TASK_E")
    # f=EmptyOperator(task_id="TASK_F")
    # g=EmptyOperator(task_id="TASK_G")
    end=EmptyOperator(task_id="END")
    
# start >> a >> a1 >> b >> c >> d >> e >> f >> g >> end


    #### TASK SCHEDULER ####

    ## 1. Sequential Task Group : 
    with TaskGroup("A_A1", tooltip="Task Group for A and A1") as grp1:
        a=EmptyOperator(task_id="TASK_A")
        a1=EmptyOperator(task_id="TASK_A1")
        b=EmptyOperator(task_id="TASK_B")
        c=EmptyOperator(task_id="TASK_C")
        a >> a1

# start >> grp1 >> d >> e >> f >> g >> end


    ## 2. Nested Task Group : 
    with TaskGroup("D-E-F-G", tooltip="Nested Task Group") as grp_2:
        d=EmptyOperator(task_id="Task_D")
        with TaskGroup("E-F-G", tooltip="Inner Nested Task Group") as grp_3:
            e=EmptyOperator(task_id="TASK_E")
            f=EmptyOperator(task_id="TASK_F")
            g=EmptyOperator(task_id="TASK_G")
            e>>f
            e>>g
    
    start >> grp1 >> grp_2 >> end