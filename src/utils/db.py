import os
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
from src.utils.config import DATABASE_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

def get_connection():
    """Return raw psycopg2 database connection."""
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

def get_engine():
    """Return SQLAlchemy engine."""
    return create_engine(DATABASE_URL)

def execute_sql_file(file_path):
    """Execute raw SQL file against PostgreSQL database."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            with open(file_path, "r", encoding="utf-8") as f:
                cur.execute(f.read())
        conn.commit()
    finally:
        conn.close()

def bulk_insert_rows(table_name, columns, rows, batch_size=10000):
    """Fast batch insertion using psycopg2 execute_values."""
    if not rows:
        return 0
    
    conn = get_connection()
    cols_str = ",".join(columns)
    query = f"INSERT INTO {table_name} ({cols_str}) VALUES %s"
    
    total_inserted = 0
    try:
        with conn.cursor() as cur:
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                execute_values(cur, query, batch)
                total_inserted += len(batch)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
    
    return total_inserted

if __name__ == "__main__":
    # Test connection and initialize schema
    print(f"Connecting to database: {POSTGRES_DB} at {POSTGRES_HOST}:{POSTGRES_PORT}...")
    schema_files = [
        "sql/schema/01_init_raw_schema.sql",
        "sql/schema/02_init_meta_schema.sql"
    ]
    for sf in schema_files:
        if os.path.exists(sf):
            print(f"Executing schema file: {sf}")
            execute_sql_file(sf)
    print("Database connection & initialization verified successfully!")
