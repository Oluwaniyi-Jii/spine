import gzip
import os
import tempfile
import pytest
from ingestion.openlibrary.parser import parse_openlibrary_dump_chunks, compute_record_hash

def test_compute_record_hash():
    h1 = compute_record_hash("/works/OL123W", '{"title": "The Great Gatsby"}')
    h2 = compute_record_hash("/works/OL123W", '{"title": "The Great Gatsby"}')
    h3 = compute_record_hash("/works/OL123W", '{"title": "Different Title"}')

    assert h1 == h2
    assert h1 != h3
    assert len(h1) == 64

def test_parse_openlibrary_dump_chunks():
    dump_lines = [
        "/type/work\t/works/OL100W\t1\t2025-01-01T00:00:00\t{\"title\": \"Work One\"}\n",
        "/type/edition\t/books/OL100M\t2\t2025-01-02T00:00:00\t{\"title\": \"Edition One\"}\n"
    ]

    with tempfile.NamedTemporaryFile(suffix=".txt.gz", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        with gzip.open(tmp_path, "wt", encoding="utf-8") as f:
            f.writelines(dump_lines)

        chunks = list(parse_openlibrary_dump_chunks(tmp_path, chunk_size=10))
        assert len(chunks) == 1
        assert len(chunks[0]) == 2
        assert chunks[0][0]["key"] == "/works/OL100W"
        assert chunks[0][1]["key"] == "/books/OL100M"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
