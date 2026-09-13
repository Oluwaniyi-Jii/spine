WITH editions AS (
    SELECT DISTINCT publisher_name FROM {{ ref('stg_openlibrary_editions') }}
    WHERE publisher_name IS NOT NULL AND TRIM(publisher_name) != ''
)

SELECT
    publisher_name AS raw_publisher_name,
    TRIM(publisher_name) AS normalized_publisher_name
FROM editions
