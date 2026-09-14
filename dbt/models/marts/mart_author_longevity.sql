WITH authors AS (
    SELECT * FROM {{ ref('dim_author') }}
),
bridge AS (
    SELECT * FROM {{ ref('bridge_work_author') }}
),
editions AS (
    SELECT * FROM {{ ref('fact_edition') }}
),
dates AS (
    SELECT * FROM {{ ref('dim_date') }}
)

SELECT
    a.author_key,
    a.canonical_name AS author_name,
    a.viaf_id,
    COUNT(DISTINCT b.work_key) AS total_works_published,
    COUNT(DISTINCT e.edition_key) AS total_editions_published,
    MIN(d.year) AS first_edition_year,
    MAX(d.year) AS last_edition_year,
    (MAX(d.year) - MIN(d.year)) AS publishing_career_span_years
FROM authors a
JOIN bridge b ON a.author_key = b.author_key
JOIN editions e ON b.work_key = e.work_key
JOIN dates d ON e.publication_date_key = d.date_key
WHERE d.year != 9999
GROUP BY a.author_key, a.canonical_name, a.viaf_id
