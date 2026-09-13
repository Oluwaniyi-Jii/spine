import pytest
from unittest.mock import patch
from src.entity_resolution.exact_match import match_by_exact_isbn, match_by_exact_viaf
from src.entity_resolution.fuzzy_match import compute_title_similarity, evaluate_fuzzy_match
from src.entity_resolution.reconcile import run_entity_reconciliation

def test_match_by_exact_isbn():
    assert match_by_exact_isbn("0743273567", "9780743273565") is True
    assert match_by_exact_isbn("1111111111", "9780743273565") is False

def test_compute_title_similarity():
    sim = compute_title_similarity("The Great Gatsby", "Great Gatsby, The")
    assert sim >= 0.95

def test_evaluate_fuzzy_match():
    match = evaluate_fuzzy_match("The Great Gatsby", "F. Scott Fitzgerald", "Great Gatsby", "Francis Scott Fitzgerald")
    assert match is not None
    assert match["match_status"] in ("ACCEPTED", "REVIEW_REQUIRED")
    assert match["match_score"] > 0.85

def test_run_entity_reconciliation():
    sources = [{
        "source_system": "openlibrary",
        "source_entity_type": "work",
        "source_entity_id": "OL123W",
        "isbn": "0743273567",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
    }]
    targets = [{
        "target_entity_type": "canonical_work",
        "target_entity_id": "CW_GATSBY",
        "isbn": "9780743273565",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
    }]

    with patch("src.entity_resolution.reconcile.bulk_insert_rows", return_value=1) as mock_insert:
        inserted = run_entity_reconciliation(sources, targets)
        assert inserted == 1
        assert mock_insert.called
