# Entity Resolution Methodology — Shelf

Reconstructing canonical works across heterogeneous public bibliographic sources requires deduplicating works, editions, authors, and publishers without manual intervention.

---

## Resolution Strategy & Rules

1. **Exact Deterministic Identification**:
   - **ISBN-10 / ISBN-13 Match**: Clean raw ISBNs, convert ISBN-10 to ISBN-13 via weighted modulus-11 checksums, and match edition keys (`match_score = 1.0`).
   - **LCCN Match**: Normalize Library of Congress Catalog Numbers (`match_score = 1.0`).
   - **VIAF Cluster Match**: Link variant author names via Virtual International Authority File IDs (`match_score = 1.0`).

2. **Probabilistic Fuzzy Matching**:
   - **Title Similarity**: Jaro-Winkler distance on sanitized titles (removing diacritics, bracketed year notes, and leading/trailing articles).
   - **Author Similarity**: Token-set ratio Levenshtein distance on normalized author names.
   - **Combined Confidence Score**:
     $$\text{Score} = 0.6 \times \text{TitleScore} + 0.4 \times \text{AuthorScore}$$
   - **Thresholds**:
     - $\ge 0.90$: Automatically `ACCEPTED`
     - $0.85 - 0.89$: Flagged as `REVIEW_REQUIRED`
     - $< 0.85$: `REJECTED`

3. **Provenance Audit**:
   - Every candidate match is recorded in `meta.entity_match` with match rule metadata, score, and match status flags.
