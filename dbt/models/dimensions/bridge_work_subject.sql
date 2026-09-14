WITH works AS (
    SELECT * FROM {{ ref('dim_work') }}
),
subjects AS (
    SELECT * FROM {{ ref('dim_subject') }}
)

SELECT
    w.work_key,
    s.subject_key
FROM works w
CROSS JOIN subjects s
LIMIT 100
