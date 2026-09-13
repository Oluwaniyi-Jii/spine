from typing import Optional, Dict, Any
from rapidfuzz import fuzz
from src.normalization.text import sanitize_title

def compute_title_similarity(title1: str, title2: str) -> float:
    """Compute Jaro-Winkler / token_sort similarity between two title strings."""
    t1 = sanitize_title(title1)
    t2 = sanitize_title(title2)
    if not t1 or not t2:
        return 0.0
    
    score = fuzz.token_sort_ratio(t1, t2) / 100.0
    return float(score)

def compute_author_similarity(author1: str, author2: str) -> float:
    """Compute author name fuzzy distance score."""
    if not author1 or not author2:
        return 0.0
    
    score = fuzz.token_set_ratio(str(author1).lower(), str(author2).lower()) / 100.0
    return float(score)

def evaluate_fuzzy_match(
    source_title: str,
    source_author: str,
    target_title: str,
    target_author: str,
    threshold: float = 0.85
) -> Optional[Dict[str, Any]]:
    """
    Evaluate combined title + author fuzzy similarity score.
    Returns match dictionary if combined score exceeds threshold.
    """
    title_score = compute_title_similarity(source_title, target_title)
    author_score = compute_author_similarity(source_author, target_author)

    combined_score = (title_score * 0.6) + (author_score * 0.4)

    if combined_score >= threshold:
        status = "ACCEPTED" if combined_score >= 0.90 else "REVIEW_REQUIRED"
        return {
            "match_method": "FUZZY_TITLE_AUTHOR",
            "match_score": round(combined_score, 4),
            "match_status": status,
            "matched_on_title_author": True,
            "title_score": title_score,
            "author_score": author_score
        }

    return None
