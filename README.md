# Shelf

**Shelf** is an analytical data warehouse that reconstructs the publishing history of books by integrating public bibliographic datasets, resolving entities across sources, modeling works and editions dimensionally, and producing historical analytics around publishing, authors, languages, subjects, and formats.

---

## Technical Stack

* **Processing Engine**: Python 3.11 / Polars
* **Data Warehouse**: PostgreSQL 16 (Schemas: `raw`, `staging`, `intermediate`, `warehouse`, `marts`, `meta`)
* **Data Transformation**: dbt (Data Build Tool)
* **Orchestration**: Apache Airflow 2.8
* **Entity Resolution**: RapidFuzz (Jaro-Winkler title & Levenshtein author matching) + Exact ISBN/VIAF/LCCN matchers
* **Literary Text Analytics**: NLTK Readability & Dialogue Metrics
* **Containers & Infrastructure**: Docker & Docker Compose
* **Visual Dashboards**: Power BI Star Schema & DAX Measures

---

## Data Sources

* **Open Library**: Bulk dump files (`ol_dump_works.txt.gz`, `ol_dump_editions.txt.gz`, `ol_dump_authors.txt.gz`)
* **Project Gutenberg**: Catalog metadata feeds & plain text eBook files
* **VIAF (Virtual International Authority File)**: Author identity authority records
* **Library of Congress & Google Books**: Catalog verification and metadata enrichment

---

## Project Documentation

- [Architecture Overview](docs/architecture.md)
- [Entity Resolution Methodology](docs/entity_resolution.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Power BI Dashboard Guide](docs/powerbi_dashboard_guide.md)

---

## Quickstart

```bash
# Start Docker environment (PostgreSQL 16)
make up

# Run unit & integration test suite
make test

# Ingest raw Open Library & Gutenberg data
make ingest-ol
make ingest-gutenberg

# Execute Entity Resolution Reconciliation
make reconcile

# Build dbt Data Warehouse Models
make dbt-run

# Run dbt Data Quality Assertions
make dbt-test
```