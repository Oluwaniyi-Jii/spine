# Data Dictionary — Shelf Dimensional Warehouse

## Dimensional Tables (`warehouse` schema)

### `dim_work`
- `work_key` (VARCHAR, PK): MD5 surrogate key for canonical work.
- `openlibrary_work_id` (VARCHAR): Open Library work identifier (e.g. `/works/OL123W`).
- `canonical_title` (TEXT): Cleaned canonical work title.
- `subtitle` (TEXT): Subtitle text.
- `raw_first_publish_date` (VARCHAR): Original publication year / date string.

### `dim_author`
- `author_key` (VARCHAR, PK): MD5 surrogate key for author.
- `openlibrary_author_id` (VARCHAR): Open Library author identifier.
- `canonical_name` (TEXT): Standardized author name from VIAF/OL.
- `viaf_id` (VARCHAR): Virtual International Authority File ID.
- `wikidata_id` (VARCHAR): Wikidata entity identifier.

### `dim_publisher`
- `publisher_key` (VARCHAR, PK): MD5 surrogate key for publisher.
- `canonical_name` (TEXT): Normalized publisher name (e.g. "Scribner", "Penguin").
- `raw_publisher_name` (TEXT): Raw source string.

---

## Fact Tables (`warehouse` schema)

### `fact_edition`
- `edition_key` (VARCHAR, PK): MD5 surrogate key per edition record.
- `work_key` (VARCHAR, FK): Foreign key to `dim_work`.
- `publisher_key` (VARCHAR, FK): Foreign key to `dim_publisher`.
- `language_key` (VARCHAR, FK): Foreign key to `dim_language`.
- `publication_date_key` (INT, FK): Foreign key to `dim_date` (YYYYMMDD).
- `isbn` (VARCHAR): Cleaned ISBN-13 string.
- `lccn` (VARCHAR): Library of Congress Catalog Number.
- `edition_title` (TEXT): Title of published manifestation.
- `format` (VARCHAR): Hardcover, Paperback, eBook, etc.
- `number_of_pages` (INT): Total page count.
