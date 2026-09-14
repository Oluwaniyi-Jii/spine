SELECT
    MD5(format_name) AS format_key,
    format_name,
    is_digital
FROM (
    SELECT 'Hardcover' AS format_name, FALSE AS is_digital UNION ALL
    SELECT 'Paperback' AS format_name, FALSE AS is_digital UNION ALL
    SELECT 'Mass Market Paperback' AS format_name, FALSE AS is_digital UNION ALL
    SELECT 'eBook' AS format_name, TRUE AS is_digital UNION ALL
    SELECT 'Audiobook' AS format_name, TRUE AS is_digital
) fmt
