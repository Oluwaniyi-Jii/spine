from typing import Optional, Dict, Any
from src.normalization.isbn import normalize_isbn

def match_by_exact_isbn(ol_isbn: str, target_isbn: str) -> bool:
    """Return True if normalized ISBN-13 match exactly."""
    norm1 = normalize_isbn(ol_isbn)
    norm2 = normalize_isbn(target_isbn)
    if norm1 and norm2 and norm1 == norm2:
        return True
    return False

def match_by_exact_lccn(lccn1: str, lccn2: str) -> bool:
    """Return True if cleaned LCCN matches."""
    if not lccn1 or not lccn2:
        return False
    clean1 = str(lccn1).strip().lower().replace(" ", "")
    clean2 = str(lccn2).strip().lower().replace(" ", "")
    return clean1 == clean2

def match_by_exact_viaf(viaf1: str, viaf2: str) -> bool:
    """Return True if VIAF ID matches."""
    if not viaf1 or not viaf2:
        return False
    return str(viaf1).strip() == str(viaf2).strip()

def evaluate_exact_matches(source_rec: Dict[str, Any], target_rec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Evaluate exact matching rules between source record and candidate target record.
    Returns match result dict or None.
    """
    # Check ISBN match
    src_isbn = source_rec.get("isbn")
    tgt_isbn = target_rec.get("isbn")
    if match_by_exact_isbn(src_isbn, tgt_isbn):
        return {
            "match_method": "EXACT_ISBN",
            "match_score": 1.0000,
            "match_status": "ACCEPTED",
            "matched_on_isbn": True
        }

    # Check LCCN match
    src_lccn = source_rec.get("lccn")
    tgt_lccn = target_rec.get("lccn")
    if match_by_exact_lccn(src_lccn, tgt_lccn):
        return {
            "match_method": "EXACT_LCCN",
            "match_score": 1.0000,
            "match_status": "ACCEPTED",
            "matched_on_lccn": True
        }

    # Check VIAF match
    src_viaf = source_rec.get("viaf_id")
    tgt_viaf = target_rec.get("viaf_id")
    if match_by_exact_viaf(src_viaf, tgt_viaf):
        return {
            "match_method": "EXACT_VIAF",
            "match_score": 1.0000,
            "match_status": "ACCEPTED",
            "matched_on_viaf": True
        }

    return None
