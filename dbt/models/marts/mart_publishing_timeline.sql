WITH works AS (
    SELECT * FROM {{ ref('dim_work') }}
),
editions AS (
    SELECT * FROM {{ ref('fact_edition') }}
),
publishers AS (
    SELECT * FROM {{ ref('dim_publisher') }}
),
languages AS (
    SELECT * FROM {{ ref('dim_language') }}
),
dates AS (
    SELECT * FROM {{ ref('dim_date') }}
)

SELECT
    w.work_key,
    w.canonical_title AS work_title,
    w.raw_first_publish_date AS original_publication_year,
    e.edition_key,
    e.edition_title,
    p.canonical_name AS publisher_name,
    l.language_name,
    e.format,
    d.year AS edition_publication_year,
    d.decade AS edition_publication_decade,
    e.number_of_pages,
    e.isbn
FROM editions e
JOIN works w ON e.work_key = w.work_key
LEFT JOIN publishers p ON e.publisher_key = p.publisher_key
LEFT JOIN languages l ON e.language_key = l.language_key
LEFT JOIN dates d ON e.publication_date_key = d.date_key
