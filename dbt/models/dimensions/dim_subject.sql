SELECT
    MD5(subject_name) AS subject_key,
    subject_name,
    'openlibrary' AS subject_system
FROM (
    SELECT 'Fiction' AS subject_name UNION ALL
    SELECT 'History' AS subject_name UNION ALL
    SELECT 'Biography' AS subject_name UNION ALL
    SELECT 'Science Fiction' AS subject_name UNION ALL
    SELECT 'Poetry' AS subject_name UNION ALL
    SELECT 'Drama' AS subject_name
) sub
