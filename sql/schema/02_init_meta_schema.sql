-- Metadata, Audit, and Provenance Audit tables

CREATE TABLE IF NOT EXISTS meta.ingestion_log (
    batch_id VARCHAR(100) PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,
    source_file VARCHAR(255),
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'RUNNING',
    records_processed BIGINT DEFAULT 0,
    records_inserted BIGINT DEFAULT 0,
    records_failed BIGINT DEFAULT 0,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS meta.data_quality_log (
    test_id BIGSERIAL PRIMARY KEY,
    batch_id VARCHAR(100),
    test_name VARCHAR(150) NOT NULL,
    target_table VARCHAR(100) NOT NULL,
    column_name VARCHAR(100),
    status VARCHAR(20) NOT NULL, -- 'PASSED', 'FAILED', 'WARN'
    records_evaluated BIGINT,
    records_flagged BIGINT,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

CREATE INDEX IF NOT EXISTS idx_meta_dq_batch ON meta.data_quality_log(batch_id);
