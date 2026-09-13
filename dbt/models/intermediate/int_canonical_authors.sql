WITH ol_authors AS (
    SELECT * FROM {{ ref('stg_openlibrary_authors') }}
),
viaf_authors AS (
    SELECT * FROM {{ ref('stg_viaf_authors') }}
)

SELECT
    a.openlibrary_author_id,
    COALESCE(v.canonical_name, a.canonical_name) AS canonical_name,
    a.viaf_id,
    COALESCE(v.wikidata_id, a.wikidata_id) AS wikidata_id,
    a.raw_birth_date,
    a.raw_death_date
FROM ol_authors a
LEFT JOIN viaf_authors v ON a.viaf_id = v.viaf_id
