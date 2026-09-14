WITH languages AS (
    SELECT * FROM {{ ref('int_languages') }}
)

SELECT
    MD5(iso_639_2) AS language_key,
    iso_639_1,
    iso_639_2,
    language_name
FROM languages
