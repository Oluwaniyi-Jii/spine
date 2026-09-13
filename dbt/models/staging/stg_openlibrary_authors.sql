WITH raw_authors AS (
    SELECT
        author_key,
        revision,
        last_modified,
        json_data,
        source_system,
        source_file,
        ingestion_batch_id,
        record_hash
    FROM {{ source('raw', 'openlibrary_authors') }}
)

SELECT
    author_key AS openlibrary_author_id,
    TRIM(json_data->>'name') AS canonical_name,
    json_data->>'birth_date' AS raw_birth_date,
    json_data->>'death_date' AS raw_death_date,
    json_data->'alternate_names' AS alternate_names,
    json_data->'remote_ids'->>'viaf' AS viaf_id,
    json_data->'remote_ids'->>'wikidata' AS wikidata_id,
    revision,
    last_modified,
    source_system,
    ingestion_batch_id
FROM raw_authors
