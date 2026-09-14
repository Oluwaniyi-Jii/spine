WITH date_series AS (
    SELECT generate_series('1800-01-01'::date, '2030-12-31'::date, '1 day'::interval)::date AS date_day
)

SELECT
    (EXTRACT(YEAR FROM date_day) * 10000 + EXTRACT(MONTH FROM date_day) * 100 + EXTRACT(DAY FROM date_day))::INT AS date_key,
    date_day,
    EXTRACT(YEAR FROM date_day)::INT AS year,
    (FLOOR(EXTRACT(YEAR FROM date_day) / 10) * 10)::INT AS decade,
    (FLOOR(EXTRACT(YEAR FROM date_day) / 100) + 1)::INT AS century,
    EXTRACT(QUARTER FROM date_day)::INT AS quarter,
    EXTRACT(MONTH FROM date_day)::INT AS month,
    TO_CHAR(date_day, 'Month') AS month_name
FROM date_series
UNION ALL
SELECT
    99991231 AS date_key,
    '9999-12-31'::date AS date_day,
    9999 AS year,
    9990 AS decade,
    100 AS century,
    4 AS quarter,
    12 AS month,
    'Unknown' AS month_name
