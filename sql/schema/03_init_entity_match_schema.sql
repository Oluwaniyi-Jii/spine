-- Entity Resolution tracking table schema

CREATE TABLE IF NOT EXISTS meta.entity_match (
    entity_match_id BIGSERIAL PRIMARY KEY,
    source_system VARCHAR(50) NOT NULL,          -- 'openlibrary', 'gutenberg', 'viaf', 'loc'
    source_entity_type VARCHAR(50) NOT NULL,     -- 'work', 'edition', 'author'
    source_entity_id VARCHAR(100) NOT NULL,      -- e.g., 'OL123W', '123'
    target_entity_type VARCHAR(50) NOT NULL,     -- 'canonical_work', 'canonical_author'
    target_entity_id VARCHAR(100) NOT NULL,
    match_method VARCHAR(50) NOT NULL,           -- 'EXACT_ISBN', 'EXACT_VIAF', 'FUZZY_TITLE_AUTHOR'
    match_score NUMERIC(5,4) NOT NULL,           -- 0.0000 to 1.0000
    match_status VARCHAR(20) DEFAULT 'ACCEPTED', -- 'ACCEPTED', 'REVIEW_REQUIRED', 'REJECTED'
    matched_on_isbn BOOLEAN DEFAULT FALSE,
    matched_on_lccn BOOLEAN DEFAULT FALSE,
    matched_on_title_author BOOLEAN DEFAULT FALSE,
    matched_on_viaf BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_entity_match_src ON meta.entity_match(source_system, source_entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_match_tgt ON meta.entity_match(target_entity_type, target_entity_id);
