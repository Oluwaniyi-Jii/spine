WITH works AS (
    SELECT * FROM {{ ref('int_canonical_works') }}
)

SELECT
    MD5(openlibrary_work_id) AS work_key,
    openlibrary_work_id,
    canonical_title,
    subtitle,
    raw_first_publish_date,
    CURRENT_TIMESTAMP AS created_at
FROM works
