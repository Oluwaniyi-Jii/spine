WITH publishers AS (
    SELECT * FROM {{ ref('dim_publisher') }}
),
editions AS (
    SELECT * FROM {{ ref('fact_edition') }}
),
dates AS (
    SELECT * FROM {{ ref('dim_date') }}
)

SELECT
    p.publisher_key,
    p.canonical_name AS publisher_name,
    d.decade,
    COUNT(DISTINCT e.edition_key) AS editions_published,
    COUNT(DISTINCT e.work_key) AS works_published,
    AVG(e.number_of_pages) AS avg_pages_per_edition
FROM publishers p
JOIN editions e ON p.publisher_key = e.publisher_key
JOIN dates d ON e.publication_date_key = d.date_key
WHERE d.year != 9999
GROUP BY p.publisher_key, p.canonical_name, d.decade
