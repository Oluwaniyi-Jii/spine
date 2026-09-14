-- Assert that publication year is within reasonable bounds (1000 to current year + 2)

SELECT
    edition_key,
    publication_date_key
FROM {{ ref('fact_edition') }}
WHERE publication_date_key != 99991231
  AND (publication_date_key < 10000101 OR publication_date_key > 20301231)
