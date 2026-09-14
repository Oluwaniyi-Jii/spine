from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags.utils.airflow_config import DEFAULT_DAG_ARGS
from ingestion.openlibrary.ingest_works import run_ingest_works
from ingestion.openlibrary.ingest_editions import run_ingest_editions
from ingestion.openlibrary.ingest_authors import run_ingest_authors
from ingestion.gutenberg.ingest_catalog import run_ingest_gutenberg_catalog
from ingestion.viaf.ingest_authority import run_ingest_viaf_authority

with DAG(
    dag_id='shelf_raw_ingestion',
    default_args=DEFAULT_DAG_ARGS,
    description='Bulk download and raw database ingestion for Open Library, Gutenberg, and VIAF',
    schedule_interval='0 2 1 * *', # Monthly on the 1st
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['shelf', 'raw', 'ingestion']
) as dag:

    ingest_ol_works_task = PythonOperator(
        task_id='ingest_openlibrary_works',
        python_callable=run_ingest_works
    )

    ingest_ol_editions_task = PythonOperator(
        task_id='ingest_openlibrary_editions',
        python_callable=run_ingest_editions
    )

    ingest_ol_authors_task = PythonOperator(
        task_id='ingest_openlibrary_authors',
        python_callable=run_ingest_authors
    )

    ingest_gutenberg_task = PythonOperator(
        task_id='ingest_gutenberg_catalog',
        python_callable=run_ingest_gutenberg_catalog
    )

    ingest_viaf_task = PythonOperator(
        task_id='ingest_viaf_authority',
        python_callable=run_ingest_viaf_authority
    )

    [ingest_ol_works_task, ingest_ol_editions_task, ingest_ol_authors_task] >> ingest_gutenberg_task >> ingest_viaf_task
