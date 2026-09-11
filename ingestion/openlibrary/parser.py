import gzip
import hashlib
import json
import polars as pl
from typing import Generator, Dict, Any, List
from src.utils.logger import logger

def compute_record_hash(key: str, json_str: str) -> str:
    """Compute SHA-256 hash for raw record provenance tracking."""
    return hashlib.sha256(f"{key}:{json_str}".encode('utf-8')).hexdigest()

def parse_openlibrary_dump_chunks(
    filepath: str,
    chunk_size: int = 50000,
    limit_rows: int = -1
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Stream and parse tab-delimited Open Library gzipped dump file.
    Dump format: type \t key \t revision \t last_modified \t json_string
    """
    logger.info(f"Parsing Open Library dump file: {filepath} with chunk size {chunk_size}")
    
    current_chunk = []
    total_parsed = 0

    open_fn = gzip.open if filepath.endswith('.gz') else open

    with open_fn(filepath, 'rt', encoding='utf-8') as f:
        for line in f:
            parts = line.rstrip('\r\n').split('\t')
            if len(parts) < 5:
                continue

            rec_type, rec_key, revision_str, last_modified, json_str = parts[0], parts[1], parts[2], parts[3], parts[4]

            try:
                revision = int(revision_str) if revision_str.isdigit() else None
            except ValueError:
                revision = None

            record_hash = compute_record_hash(rec_key, json_str)

            record = {
                "type": rec_type,
                "key": rec_key,
                "revision": revision,
                "last_modified": last_modified,
                "json_str": json_str,
                "record_hash": record_hash
            }

            current_chunk.append(record)
            total_parsed += 1

            if len(current_chunk) >= chunk_size:
                yield current_chunk
                current_chunk = []

            if limit_rows > 0 and total_parsed >= limit_rows:
                logger.info(f"Reached limit_rows={limit_rows}")
                break

    if current_chunk:
        yield current_chunk

    logger.info(f"Finished parsing file {filepath}. Total records processed: {total_parsed}")
