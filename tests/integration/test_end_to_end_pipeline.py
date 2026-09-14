import pytest
from unittest.mock import patch
from src.normalization.isbn import normalize_isbn
from src.normalization.dates import extract_publication_year
from src.normalization.text import sanitize_title
from src.entity_resolution.exact_match import evaluate_exact_matches
from src.text_analysis.metrics import compute_text_metrics

def test_full_pipeline_transformations():
    # 1. Test Raw ISBN & Date Normalization
    raw_isbn = "0-7432-7356-7"
    norm_isbn = normalize_isbn(raw_isbn)
    assert norm_isbn == "9780743273565"

    raw_date = "First published in 1925"
    pub_year = extract_publication_year(raw_date)
    assert pub_year == 1925

    # 2. Test Title Sanitization
    raw_title = "Great Gatsby, The [1925 Edition]"
    clean_t = sanitize_title(raw_title)
    assert clean_t == "The Great Gatsby"

    # 3. Test Entity Matching
    ol_rec = {"isbn": "0743273567", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    loc_rec = {"isbn": "9780743273565", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
    match = evaluate_exact_matches(ol_rec, loc_rec)
    assert match is not None
    assert match["match_method"] == "EXACT_ISBN"

    # 4. Test Text Analysis
    sample_text = "It was the best of times, it was the worst of times."
    metrics = compute_text_metrics(sample_text)
    assert metrics["word_count"] == 12
