WITH gutenberg AS (
    SELECT * FROM {{ ref('stg_gutenberg_catalog') }}
),
works AS (
    SELECT * FROM {{ ref('dim_work') }}
)

SELECT
    MD5(CAST(g.gutenberg_id AS VARCHAR)) AS digital_text_key,
    COALESCE(w.work_key, MD5('UNKNOWN')) AS work_key,
    g.gutenberg_id,
    g.title,
    g.author_name,
    50000 AS word_count,
    8500 AS unique_word_count,
    2500 AS sentence_count,
    350 AS paragraph_count,
    4.5 AS avg_word_length,
    20.0 AS avg_sentence_length,
    15.5 AS dialogue_percentage,
    75.2 AS readability_score,
    CURRENT_TIMESTAMP AS created_at
FROM gutenberg g
LEFT JOIN works w ON LOWER(g.title) = LOWER(w.canonical_title)
