# Shelf

Shelf is a data warehouse for exploring the publishing history of books.

It integrates public bibliographic data from sources such as [Open Library](https://openlibrary.org/), [Project Gutenberg](https://www.gutenberg.org/), and VIAF to build a canonical view of works, editions, authors, publishers, languages, and subjects.

The project focuses on the data engineering problems behind bibliographic data: ingestion, normalization, entity resolution, data quality, historical modeling, and analytical warehousing.

## Goals

* Ingest large public bibliographic datasets
* Normalize and reconcile records across different sources
* Model books as works and individual editions
* Track source provenance and data quality
* Build a dimensional data warehouse with PostgreSQL and dbt
* Produce analytical datasets for publishing and literary trends

## Stack

* Python
* PostgreSQL
* dbt
* Apache Airflow
* Docker
* Power BI
* GitHub Actions

## Data Sources

* Open Library — works, editions, authors, and bibliographic metadata
* Project Gutenberg — public-domain texts and metadata
* VIAF — authority data for resolving author identities
* Additional sources may be added for enrichment and validation

## Status

**In development**

The initial focus is on building the ingestion and warehouse layers before adding analytical models and dashboards.