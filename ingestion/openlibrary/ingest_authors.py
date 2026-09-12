import os
from src.utils.config import DATA_DIR, LIMIT_ROWS
from src.utils.db import bulk_insert_rows
from src.utils.audit import start_ingestion_batch, finish_ingestion_batch
from src.utils.logger import logger
from ingestion.openlibrary.parser import parse_openlibrary_dump_chunks

def run_ingest_authors(filepath: str = None, limit: int = LIMIT_ROWS):
    if not filepath:
        filepath = os.path.join(DATA_DIR, "openlibrary", "ol_dump_authors.txt.gz")

    if not os.path.exists(filepath):
        logger.warning(f"Author dump file not found: {filepath}. Skipping authors ingestion.")
        return

    batch_id = start_ingestion_batch("openlibrary_authors", os.path.basename(filepath))
    total_processed = 0
    total_inserted = 0

    try:
        for chunk in parse_openlibrary_dump_chunks(filepath, chunk_size=20000, limit_rows=limit):
            rows_to_insert = []
            for item in chunk:
                total_processed += 1
                if item["type"] in ("/type/author", "author"):
                    rows_to_insert.append((
                        item["key"],
                        item["revision"],
                        item["last_modified"],
                        item["json_str"],
                        "openlibrary",
                        os.path.basename(filepath),
                        batch_id,
                        item["record_hash"]
                    ))

            if rows_to_insert:
                cols = [
                    "author_key", "revision", "last_modified", "json_data",
                    "source_system", "source_file", "ingestion_batch_id", "record_hash"
                ]
                inserted = bulk_insert_rows("raw.openlibrary_authors", cols, rows_to_insert)
                total_inserted += inserted

        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="COMPLETED")
        logger.info(f"Ingested {total_inserted} author records in batch {batch_id}")

    except Exception as e:
        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="FAILED", error_message=str(e))
        logger.error(f"Authors ingestion failed: {str(e)}")
        raise e

if __name__ == "__main__":
    run_ingest_authors()
