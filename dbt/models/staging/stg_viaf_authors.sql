WITH raw_viaf AS (
    SELECT
        viaf_id,
        canonical_name,
        alternate_names,
        external_identifiers,
        source_system,
        ingestion_batch_id
    FROM {{ source('raw', 'viaf_author_authority') }}
)

SELECT
    viaf_id,
    TRIM(canonical_name) AS canonical_name,
    alternate_names,
    external_identifiers->>'lccn' AS lccn,
    external_identifiers->>'wikidata' AS wikidata_id,
    source_system,
    ingestion_batch_id
FROM raw_viaf
