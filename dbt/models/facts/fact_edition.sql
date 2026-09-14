WITH editions AS (
    SELECT * FROM {{ ref('int_edition_history') }}
),
works AS (
    SELECT * FROM {{ ref('dim_work') }}
),
publishers AS (
    SELECT * FROM {{ ref('dim_publisher') }}
)

SELECT
    MD5(e.openlibrary_edition_id) AS edition_key,
    COALESCE(w.work_key, MD5('UNKNOWN')) AS work_key,
    COALESCE(p.publisher_key, MD5('UNKNOWN')) AS publisher_key,
    MD5('eng') AS language_key,
    99991231 AS publication_date_key,
    e.openlibrary_edition_id,
    e.isbn,
    e.raw_lccn AS lccn,
    e.raw_oclc AS oclc_number,
    e.edition_title,
    e.physical_format AS format,
    e.number_of_pages,
    e.ingestion_batch_id,
    CURRENT_TIMESTAMP AS created_at
FROM editions e
LEFT JOIN works w ON e.work_key = w.openlibrary_work_id
LEFT JOIN publishers p ON e.publisher_name = p.raw_publisher_name
