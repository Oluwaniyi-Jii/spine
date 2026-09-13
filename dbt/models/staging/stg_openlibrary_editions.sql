WITH raw_editions AS (
    SELECT
        edition_key,
        revision,
        last_modified,
        json_data,
        source_system,
        source_file,
        ingestion_batch_id,
        record_hash
    FROM {{ source('raw', 'openlibrary_editions') }}
)

SELECT
    edition_key AS openlibrary_edition_id,
    json_data->'works'->0->>'key' AS work_key,
    TRIM(json_data->>'title') AS title,
    json_data->>'subtitle' AS subtitle,
    json_data->'publishers'->>0 AS publisher_name,
    json_data->>'publish_date' AS raw_publish_date,
    json_data->>'physical_format' AS physical_format,
    CAST(json_data->>'number_of_pages' AS INT) AS number_of_pages,
    json_data->'isbn_10'->>0 AS raw_isbn10,
    json_data->'isbn_13'->>0 AS raw_isbn13,
    json_data->'lccn'->>0 AS raw_lccn,
    json_data->'oclc_numbers'->>0 AS raw_oclc,
    revision,
    last_modified,
    source_system,
    ingestion_batch_id
FROM raw_editions
