#!/usr/bin/python3
import os
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.bash import BashOperator

# let's setup arguments for our dag

DAG_ID = os.path.basename(__file__).replace(".py", "")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 10,
    'concurrency': 1
}

# dag declaration

dag = DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    start_date=datetime.now() + timedelta(days=-1),
    schedule_interval=timedelta(seconds=5)
)


# Here's a task based on Bash Operator!

bash_task = BashOperator(task_id='bash_task_1',
                         bash_command="env",
                         dag=dag)
