#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import all important packages
from datetime import datetime, timedelta
from airflow import models
# imported BashOperator method
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.utils.dates import days_ago

# Get the yesterday timestamp
yesterday = datetime.combine(
    datetime.today() - timedelta(1),
    datetime.min.time())

# Create a dictionary of default arguments for each task to set the task"s constructor
default_dag_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'project_id': models.Variable.get('gcp_project')
}

with DAG(
        dag_id="any_bash_command_dag",
        schedule_interval=None,
        catchup=False,
        start_date=days_ago(1)) as dag:
    cli_command = BashOperator(
        task_id="bash_command",
        bash_command="{{ dag_run.conf['command'] }}"
    )
