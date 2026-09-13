from typing import List, Dict, Any
from src.utils.db import bulk_insert_rows, get_connection
from src.utils.logger import logger
from src.entity_resolution.exact_match import evaluate_exact_matches
from src.entity_resolution.fuzzy_match import evaluate_fuzzy_match

def run_entity_reconciliation(source_records: List[Dict[str, Any]], target_records: List[Dict[str, Any]]):
    """
    Run entity resolution across candidate pairs and persist matches to meta.entity_match.
    """
    logger.info(f"Starting entity resolution reconciliation across {len(source_records)} sources and {len(target_records)} targets")
    
    matches_to_insert = []

    for src in source_records:
        src_id = src.get("source_entity_id")
        src_type = src.get("source_entity_type", "work")
        src_sys = src.get("source_system", "openlibrary")

        for tgt in target_records:
            tgt_id = tgt.get("target_entity_id")
            tgt_type = tgt.get("target_entity_type", "canonical_work")

            # Try exact matching first
            match_res = evaluate_exact_matches(src, tgt)
            if not match_res:
                # Fallback to fuzzy matching
                match_res = evaluate_fuzzy_match(
                    src.get("title", ""), src.get("author", ""),
                    tgt.get("title", ""), tgt.get("author", "")
                )

            if match_res:
                matches_to_insert.append((
                    src_sys,
                    src_type,
                    src_id,
                    tgt_type,
                    tgt_id,
                    match_res["match_method"],
                    match_res["match_score"],
                    match_res["match_status"],
                    match_res.get("matched_on_isbn", False),
                    match_res.get("matched_on_lccn", False),
                    match_res.get("matched_on_title_author", False),
                    match_res.get("matched_on_viaf", False)
                ))

    if matches_to_insert:
        cols = [
            "source_system", "source_entity_type", "source_entity_id",
            "target_entity_type", "target_entity_id", "match_method",
            "match_score", "match_status", "matched_on_isbn",
            "matched_on_lccn", "matched_on_title_author", "matched_on_viaf"
        ]
        inserted = bulk_insert_rows("meta.entity_match", cols, matches_to_insert)
        logger.info(f"Inserted {inserted} entity match records into meta.entity_match")
        return inserted
    
    return 0
