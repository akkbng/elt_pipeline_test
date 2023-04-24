import os
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow_dbt.operators.dbt_operator import DbtRunOperator, DbtTestOperator


schedule_interval = "@daily"
start_date = days_ago(1)
default_args = {"owner": "airflow", "depends_on_past": False, "retries": 1}


with DAG(
    dag_id="sumup_dbt_dag",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1, 
) as dag:
    task_1 = BashOperator(
        task_id='dbt_test',
        bash_command='cd /sumup && dbt test --profiles-dir .',
        dag=dag
    )

    task_2 = BashOperator(
        task_id='dbt_run',
        bash_command='cd /sumup && dbt run --profiles-dir .',
        dag=dag
    )

task_1 >> task_2  