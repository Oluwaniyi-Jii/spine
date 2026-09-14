WITH works AS (
    SELECT * FROM {{ ref('dim_work') }}
),
authors AS (
    SELECT * FROM {{ ref('dim_author') }}
)

SELECT
    w.work_key,
    a.author_key,
    'author' AS author_role,
    1 AS author_order
FROM works w
CROSS JOIN authors a
LIMIT 100 -- Default placeholder relation for works and authors
