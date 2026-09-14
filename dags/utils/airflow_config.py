import os

POSTGRES_CONN_ID = "shelf_postgres_conn"
DEFAULT_DAG_ARGS = {
    'owner': 'shelf_data_eng',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "./dbt")
DATA_DIR = os.getenv("DATA_DIR", "./data")
