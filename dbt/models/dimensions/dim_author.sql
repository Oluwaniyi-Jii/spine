WITH authors AS (
    SELECT * FROM {{ ref('int_canonical_authors') }}
)

SELECT
    MD5(openlibrary_author_id) AS author_key,
    openlibrary_author_id,
    canonical_name,
    viaf_id,
    wikidata_id,
    raw_birth_date,
    raw_death_date,
    CURRENT_TIMESTAMP AS created_at
FROM authors
