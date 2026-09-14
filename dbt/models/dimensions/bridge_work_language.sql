WITH works AS (
    SELECT * FROM {{ ref('dim_work') }}
),
languages AS (
    SELECT * FROM {{ ref('dim_language') }}
)

SELECT
    w.work_key,
    l.language_key,
    'original' AS language_role
FROM works w
CROSS JOIN languages l
LIMIT 100
