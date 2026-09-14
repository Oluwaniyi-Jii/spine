from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from dags.utils.airflow_config import DEFAULT_DAG_ARGS

with DAG(
    dag_id='shelf_quality_audit',
    default_args=DEFAULT_DAG_ARGS,
    description='Run weekly automated data quality assertions and record metrics to meta table',
    schedule_interval='0 0 * * 0', -- Every Sunday midnight
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['shelf', 'quality', 'audit']
) as dag:

    run_quality_audit_task = BashOperator(
        task_id='execute_dbt_data_tests',
        bash_command='cd dbt && dbt test --select marts.audit'
    )
