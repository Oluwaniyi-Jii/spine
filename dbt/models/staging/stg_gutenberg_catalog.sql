WITH raw_gutenberg AS (
    SELECT
        gutenberg_id,
        title,
        author,
        language,
        subjects,
        rights,
        issued_date,
        source_system,
        ingestion_timestamp,
        ingestion_batch_id
    FROM {{ source('raw', 'gutenberg_catalog') }}
)

SELECT
    gutenberg_id,
    TRIM(title) AS title,
    TRIM(author) AS author_name,
    LOWER(TRIM(language)) AS language_code,
    subjects,
    rights,
    issued_date,
    source_system,
    ingestion_batch_id
FROM raw_gutenberg
