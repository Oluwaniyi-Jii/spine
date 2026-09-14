from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from dags.utils.airflow_config import DEFAULT_DAG_ARGS, DBT_PROJECT_DIR

with DAG(
    dag_id='shelf_dbt_transformation',
    default_args=DEFAULT_DAG_ARGS,
    description='Run entity resolution script and build dbt dimensional warehouse models',
    schedule_interval='0 4 1 * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['shelf', 'dbt', 'transformation']
) as dag:

    run_dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt deps'
    )

    run_dbt_staging = BashOperator(
        task_id='dbt_run_staging',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select staging'
    )

    run_dbt_warehouse = BashOperator(
        task_id='dbt_run_warehouse',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select dimensions facts marts'
    )

    run_dbt_test = BashOperator(
        task_id='dbt_test_all',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt test'
    )

    run_dbt_deps >> run_dbt_staging >> run_dbt_warehouse >> run_dbt_test
