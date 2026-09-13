import pytest
from src.normalization.dates import extract_publication_year, format_date_key

def test_extract_publication_year():
    assert extract_publication_year("1925") == 1925
    assert extract_publication_year("c1925") == 1925
    assert extract_publication_year("May 1925") == 1925
    assert extract_publication_year("1925?") == 1925
    assert extract_publication_year("First published 1925") == 1925
    assert extract_publication_year("1925-1927") == 1925
    assert extract_publication_year("Unknown date") is None
    assert extract_publication_year("") is None

def test_format_date_key():
    assert format_date_key(1925) == 19250101
    assert format_date_key(None) == 99991231
