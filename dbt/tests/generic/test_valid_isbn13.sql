{% test valid_isbn13(model, column_name) %}

SELECT
    *
FROM {{ model }}
WHERE {{ column_name }} IS NOT NULL
  AND (LENGTH({{ column_name }}) != 13 OR {{ column_name }} !~ '^[0-9]{13}$')

{% endtest %}
