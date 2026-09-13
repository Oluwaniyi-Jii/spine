import tempfile
import os
import pytest
from unittest.mock import patch, MagicMock
from ingestion.gutenberg.ingest_catalog import run_ingest_gutenberg_catalog

def test_gutenberg_catalog_parser_with_sample_file():
    csv_content = """Text#,Type,Issued,Title,Language,Authors,Subjects,LoCC,Rights
1,Text,1971-12-01,The Declaration of Independence,en,Jefferson Thomas,United States -- History -- Revolution 1775-1783,E201,Public domain
2,Text,1972-01-01,The United States Bill of Rights,en,United States,Civil rights -- United States,KF,Public domain
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        with patch("ingestion.gutenberg.ingest_catalog.bulk_insert_rows") as mock_insert:
            with patch("ingestion.gutenberg.ingest_catalog.start_ingestion_batch", return_value="batch_test"):
                with patch("ingestion.gutenberg.ingest_catalog.finish_ingestion_batch"):
                    mock_insert.return_value = 2
                    run_ingest_gutenberg_catalog(sample_file=tmp_path)
                    assert mock_insert.called
                    args, kwargs = mock_insert.call_args
                    rows = args[2]
                    assert len(rows) == 2
                    assert rows[0][0] == 1
                    assert rows[0][1] == "The Declaration of Independence"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
