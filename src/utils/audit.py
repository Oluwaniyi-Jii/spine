import uuid
from datetime import datetime
from src.utils.db import get_connection
from src.utils.logger import logger

def start_ingestion_batch(source_system: str, source_file: str) -> str:
    """Register a new ingestion batch in meta.ingestion_log and return batch_id."""
    batch_id = f"batch_{source_system}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO meta.ingestion_log 
                (batch_id, source_system, source_file, start_time, status)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, 'RUNNING')
            """, (batch_id, source_system, source_file))
        conn.commit()
        logger.info(f"Started ingestion batch {batch_id} for source {source_system}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to record start of batch {batch_id}: {str(e)}")
        raise e
    finally:
        conn.close()
    return batch_id

def finish_ingestion_batch(batch_id: str, records_processed: int, records_inserted: int, records_failed: int = 0, status: str = "COMPLETED", error_message: str = None):
    """Update ingestion batch stats upon completion or failure."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE meta.ingestion_log
                SET end_time = CURRENT_TIMESTAMP,
                    status = %s,
                    records_processed = %s,
                    records_inserted = %s,
                    records_failed = %s,
                    error_message = %s
                WHERE batch_id = %s
            """, (status, records_processed, records_inserted, records_failed, error_message, batch_id))
        conn.commit()
        logger.info(f"Finished ingestion batch {batch_id} with status={status}, inserted={records_inserted}")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to update end status for batch {batch_id}: {str(e)}")
    finally:
        conn.close()
