import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "shelf_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "shelf_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "shelf_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATA_DIR = os.getenv("DATA_DIR", "./data")
OPENLIBRARY_DUMP_URL = os.getenv("OPENLIBRARY_DUMP_URL", "https://openlibrary.org/data/")
GUTENBERG_CATALOG_URL = os.getenv("GUTENBERG_CATALOG_URL", "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv")
LIMIT_ROWS = int(os.getenv("LIMIT_ROWS", 100000))
