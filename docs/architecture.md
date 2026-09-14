# Shelf Architecture & System Design

Shelf is an end-to-end analytical data warehouse designed to reconstruct the publishing history of books using real public bibliographic datasets (Open Library bulk dumps, Project Gutenberg, VIAF, Library of Congress, Google Books).

---

## Technical Stack & Infrastructure
- **Data Processing Engine**: Python 3.11+ / Polars (Streaming TSV & JSON processing)
- **Database Warehouse**: PostgreSQL 16 (Schemas: `raw`, `staging`, `intermediate`, `warehouse`, `marts`, `meta`)
- **Transformation & Modeling**: dbt 1.7 (Conformed Star-Schema Dimensions & Incremental Facts)
- **Workflow Orchestration**: Apache Airflow 2.8 (DAGs for ingestion, reconciliation, dbt builds, and quality audits)
- **Entity Resolution**: RapidFuzz (Jaro-Winkler title & Levenshtein author distance) + Exact ID matchers (ISBN, LCCN, VIAF)
- **Literary Text Analytics**: NLTK NLP metrics (Word count, vocabulary richness, readability scores, dialogue ratio)
- **Container Infrastructure**: Docker & Docker Compose
- **Visual Analytics**: Power BI Star Schema & DAX Measures

---

## Data Pipeline Lifecycle

```
Open Library Dumps (GZ) ──┐
Project Gutenberg RDF ────┼──> Raw Ingestion (Polars) ──> Raw PostgreSQL Tables 
VIAF Authority Files ─────┘                                    │
                                                               ▼
                                                    dbt Staging Views
                                                               │
                                                               ▼
                                                  Entity Resolution Engine
                                                    (meta.entity_match)
                                                               │
                                                               ▼
                                                    dbt Intermediate Layer
                                                               │
                                                               ▼
                                              Dimensional Warehouse (Star Schema)
                                              (dim_work, dim_author, fact_edition)
                                                               │
                                                               ▼
                                                    Analytical Data Marts
                                                               │
                                                               ▼
                                                    Power BI Dashboards
```
