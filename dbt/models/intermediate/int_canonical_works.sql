WITH ol_works AS (
    SELECT * FROM {{ ref('stg_openlibrary_works') }}
),
matches AS (
    SELECT * FROM {{ source('raw', 'openlibrary_works') }} -- fallback or metadata
)

SELECT
    w.openlibrary_work_id,
    w.title AS canonical_title,
    w.subtitle,
    w.raw_first_publish_date,
    w.raw_subjects,
    w.raw_languages,
    w.last_modified
FROM ol_works w
