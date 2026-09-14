SELECT
    'fact_edition' AS table_name,
    COUNT(*) AS total_records,
    COUNT(isbn) AS records_with_isbn,
    ROUND((COUNT(isbn)::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 2) AS isbn_coverage_pct,
    COUNT(publisher_key) AS records_with_publisher,
    ROUND((COUNT(publisher_key)::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 2) AS publisher_coverage_pct
FROM {{ ref('fact_edition') }}
