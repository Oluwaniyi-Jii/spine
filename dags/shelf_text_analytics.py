from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from dags.utils.airflow_config import DEFAULT_DAG_ARGS

with DAG(
    dag_id='shelf_text_analytics',
    default_args=DEFAULT_DAG_ARGS,
    description='Download Project Gutenberg texts and calculate NLP readability metrics',
    schedule_interval='0 6 1 * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['shelf', 'nlp', 'text']
) as dag:

    run_nlp_metrics_task = BashOperator(
        task_id='calculate_gutenberg_text_metrics',
        bash_command='python -m src.text_analysis.metrics'
    )
