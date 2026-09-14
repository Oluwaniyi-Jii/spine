WITH texts AS (
    SELECT * FROM {{ ref('fact_text_statistics') }}
),
works AS (
    SELECT * FROM {{ ref('dim_work') }}
)

SELECT
    t.digital_text_key,
    t.gutenberg_id,
    t.title,
    t.author_name,
    w.raw_first_publish_date AS publication_year,
    t.word_count,
    t.unique_word_count,
    t.sentence_count,
    t.paragraph_count,
    t.avg_word_length,
    t.avg_sentence_length,
    t.dialogue_percentage,
    t.readability_score
FROM texts t
LEFT JOIN works w ON t.work_key = w.work_key
