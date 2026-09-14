-- Raw schema table definitions for heterogeneous source data ingestion
CREATE SCHEMA IF NOT EXISTS raw;

-- Open Library Works Raw Storage
CREATE TABLE IF NOT EXISTS raw.openlibrary_works (
    raw_id BIGSERIAL PRIMARY KEY,
    work_key VARCHAR(100) NOT NULL,
    revision INT,
    last_modified TIMESTAMP WITH TIME ZONE,
    json_data JSONB NOT NULL,
    source_system VARCHAR(50) DEFAULT 'openlibrary',
    source_file VARCHAR(255),
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(100),
    record_hash VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_raw_ol_works_key ON raw.openlibrary_works(work_key);
CREATE INDEX IF NOT EXISTS idx_raw_ol_works_batch ON raw.openlibrary_works(ingestion_batch_id);

-- Open Library Editions Raw Storage
CREATE TABLE IF NOT EXISTS raw.openlibrary_editions (
    raw_id BIGSERIAL PRIMARY KEY,
    edition_key VARCHAR(100) NOT NULL,
    revision INT,
    last_modified TIMESTAMP WITH TIME ZONE,
    json_data JSONB NOT NULL,
    source_system VARCHAR(50) DEFAULT 'openlibrary',
    source_file VARCHAR(255),
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(100),
    record_hash VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_raw_ol_editions_key ON raw.openlibrary_editions(edition_key);
CREATE INDEX IF NOT EXISTS idx_raw_ol_editions_batch ON raw.openlibrary_editions(ingestion_batch_id);

-- Open Library Authors Raw Storage
CREATE TABLE IF NOT EXISTS raw.openlibrary_authors (
    raw_id BIGSERIAL PRIMARY KEY,
    author_key VARCHAR(100) NOT NULL,
    revision INT,
    last_modified TIMESTAMP WITH TIME ZONE,
    json_data JSONB NOT NULL,
    source_system VARCHAR(50) DEFAULT 'openlibrary',
    source_file VARCHAR(255),
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(100),
    record_hash VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS idx_raw_ol_authors_key ON raw.openlibrary_authors(author_key);

-- Project Gutenberg Catalog Raw Storage
CREATE TABLE IF NOT EXISTS raw.gutenberg_catalog (
    raw_id BIGSERIAL PRIMARY KEY,
    gutenberg_id INT NOT NULL,
    title TEXT,
    author TEXT,
    language VARCHAR(20),
    subjects TEXT,
    rights TEXT,
    issued_date VARCHAR(50),
    source_system VARCHAR(50) DEFAULT 'gutenberg',
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_raw_gutenberg_id ON raw.gutenberg_catalog(gutenberg_id);

-- VIAF Authority Data Raw Storage
CREATE TABLE IF NOT EXISTS raw.viaf_author_authority (
    raw_id BIGSERIAL PRIMARY KEY,
    viaf_id VARCHAR(100) NOT NULL,
    canonical_name TEXT,
    alternate_names TEXT[],
    external_identifiers JSONB,
    source_system VARCHAR(50) DEFAULT 'viaf',
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_raw_viaf_id ON raw.viaf_author_authority(viaf_id);
