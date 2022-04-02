#!/usr/bin/python3
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.bash import BashOperator

# let's setup arguments for our dag

my_dag_id = "my_first_dag"

default_args = {
    'owner': 'proton',
    'depends_on_past': False,
    'retries': 1,
    'concurrency': 1
}

# dag declaration

dag = DAG(
    dag_id=my_dag_id,
    default_args=default_args,
    start_date=datetime(2019, 6, 17),
    schedule_interval=timedelta(seconds=5)
)


# Here's a task based on Bash Operator!

bash_task = BashOperator(task_id='bash_task_1',
                         bash_command="echo 'Hello Airflow!'",
                         dag=dag)
