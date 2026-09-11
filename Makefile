.PHONY: up down db-init ingest dbt-run dbt-test test lint clean

up:
	docker-compose up -d

down:
	docker-compose down

db-init:
	python -m src.utils.db

ingest-ol:
	python -m ingestion.openlibrary.ingest_works
	python -m ingestion.openlibrary.ingest_editions
	python -m ingestion.openlibrary.ingest_authors

ingest-gutenberg:
	python -m ingestion.gutenberg.ingest_catalog

reconcile:
	python -m src.entity_resolution.reconcile

dbt-run:
	cd dbt && dbt run --profiles-dir .

dbt-test:
	cd dbt && dbt test --profiles-dir .

test:
	pytest tests/ -v

lint:
	flake8 src/ ingestion/ dags/ tests/
	black --check src/ ingestion/ dags/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
