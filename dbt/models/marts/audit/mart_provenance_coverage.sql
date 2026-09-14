SELECT
    ingestion_batch_id,
    COUNT(*) AS total_editions_ingested,
    MIN(created_at) AS first_seen,
    MAX(created_at) AS last_seen
FROM {{ ref('fact_edition') }}
GROUP BY ingestion_batch_id
