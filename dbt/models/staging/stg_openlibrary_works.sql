WITH raw_works AS (
    SELECT
        work_key,
        revision,
        last_modified,
        json_data,
        source_system,
        source_file,
        ingestion_batch_id,
        record_hash
    FROM {{ source('raw', 'openlibrary_works') }}
)

SELECT
    work_key AS openlibrary_work_id,
    TRIM(json_data->>'title') AS title,
    json_data->>'subtitle' AS subtitle,
    CAST(json_data->>'first_publish_date' AS VARCHAR) AS raw_first_publish_date,
    json_data->'subjects' AS raw_subjects,
    json_data->'authors' AS raw_authors,
    json_data->'languages' AS raw_languages,
    revision,
    last_modified,
    source_system,
    ingestion_batch_id
FROM raw_works
