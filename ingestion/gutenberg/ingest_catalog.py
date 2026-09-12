import csv
import io
import os
import requests
from src.utils.config import GUTENBERG_CATALOG_URL, DATA_DIR
from src.utils.db import bulk_insert_rows
from src.utils.audit import start_ingestion_batch, finish_ingestion_batch
from src.utils.logger import logger

def run_ingest_gutenberg_catalog(url: str = GUTENBERG_CATALOG_URL, sample_file: str = None):
    batch_id = start_ingestion_batch("gutenberg", "pg_catalog.csv")
    total_processed = 0
    total_inserted = 0

    try:
        if sample_file and os.path.exists(sample_file):
            logger.info(f"Reading Gutenberg catalog from local sample file {sample_file}")
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            logger.info(f"Fetching Gutenberg catalog feed from {url}")
            resp = requests.get(url)
            resp.raise_for_status()
            content = resp.text

        reader = csv.DictReader(io.StringIO(content))
        rows_to_insert = []

        for row in reader:
            total_processed += 1
            gid_str = row.get("Text#", row.get("id", ""))
            if not gid_str.isdigit():
                continue
            
            gid = int(gid_str)
            title = row.get("Title", "")
            author = row.get("Authors", row.get("Author", ""))
            language = row.get("Language", "")
            subjects = row.get("Subjects", "")
            rights = row.get("Rights", "")
            issued = row.get("Issued", "")

            rows_to_insert.append((
                gid, title, author, language, subjects, rights, issued, "gutenberg", batch_id
            ))

        if rows_to_insert:
            cols = [
                "gutenberg_id", "title", "author", "language",
                "subjects", "rights", "issued_date", "source_system", "ingestion_batch_id"
            ]
            total_inserted = bulk_insert_rows("raw.gutenberg_catalog", cols, rows_to_insert)

        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="COMPLETED")
        logger.info(f"Successfully ingested {total_inserted} Gutenberg catalog items")

    except Exception as e:
        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="FAILED", error_message=str(e))
        logger.error(f"Gutenberg catalog ingestion failed: {str(e)}")
        raise e

if __name__ == "__main__":
    run_ingest_gutenberg_catalog()
