import json
import os
from src.utils.db import bulk_insert_rows
from src.utils.audit import start_ingestion_batch, finish_ingestion_batch
from src.utils.logger import logger

def run_ingest_viaf_authority(sample_records: list = None):
    batch_id = start_ingestion_batch("viaf", "viaf_authorities.json")
    total_processed = 0
    total_inserted = 0

    if sample_records is None:
        # Default sample seed authority records for key authors
        sample_records = [
            {
                "viaf_id": "100216611",
                "canonical_name": "Fitzgerald, F. Scott (Francis Scott), 1896-1940",
                "alternate_names": ["F. Scott Fitzgerald", "Francis Scott Key Fitzgerald"],
                "external_identifiers": {"lccn": "n79006871", "wikidata": "Q42830", "isni": "0000000121451980"}
            },
            {
                "viaf_id": "102333412",
                "canonical_name": "Austen, Jane, 1775-1817",
                "alternate_names": ["Jane Austen", "Author of Sense and Sensibility"],
                "external_identifiers": {"lccn": "n79032879", "wikidata": "Q9268", "isni": "000000012283635X"}
            },
            {
                "viaf_id": "95147366",
                "canonical_name": "Melville, Herman, 1819-1891",
                "alternate_names": ["Herman Melville"],
                "external_identifiers": {"lccn": "n79006936", "wikidata": "Q4985", "isni": "0000000121441148"}
            }
        ]

    try:
        rows_to_insert = []
        for rec in sample_records:
            total_processed += 1
            rows_to_insert.append((
                rec["viaf_id"],
                rec["canonical_name"],
                rec["alternate_names"],
                json.dumps(rec.get("external_identifiers", {})),
                "viaf",
                batch_id
            ))

        if rows_to_insert:
            cols = [
                "viaf_id", "canonical_name", "alternate_names",
                "external_identifiers", "source_system", "ingestion_batch_id"
            ]
            total_inserted = bulk_insert_rows("raw.viaf_author_authority", cols, rows_to_insert)

        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="COMPLETED")
        logger.info(f"Ingested {total_inserted} VIAF authority records")

    except Exception as e:
        finish_ingestion_batch(batch_id, total_processed, total_inserted, status="FAILED", error_message=str(e))
        logger.error(f"VIAF authority ingestion failed: {str(e)}")
        raise e

if __name__ == "__main__":
    run_ingest_viaf_authority()
