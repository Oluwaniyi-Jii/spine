WITH editions AS (
    SELECT * FROM {{ ref('stg_openlibrary_editions') }}
)

SELECT
    openlibrary_edition_id,
    work_key,
    title AS edition_title,
    publisher_name,
    raw_publish_date,
    physical_format,
    number_of_pages,
    COALESCE(raw_isbn13, raw_isbn10) AS isbn,
    raw_lccn,
    raw_oclc,
    ingestion_batch_id
FROM editions
