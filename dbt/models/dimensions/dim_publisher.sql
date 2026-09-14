WITH publishers AS (
    SELECT * FROM {{ ref('int_normalized_publishers') }}
)

SELECT
    MD5(normalized_publisher_name) AS publisher_key,
    normalized_publisher_name AS canonical_name,
    raw_publisher_name,
    CURRENT_TIMESTAMP AS created_at
FROM publishers
