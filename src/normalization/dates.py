import re
from typing import Optional

def extract_publication_year(raw_date_str: str) -> Optional[int]:
    """
    Extract 4-digit publication year (between 1000 and 2030) from noisy date strings.
    Handles formats like: "1925", "c1925", "May 1925", "1925?", "1925-1927", "Published in 1925".
    """
    if not raw_date_str:
        return None

    # Search for 4-digit years between 1000 and 2029
    match = re.search(r'\b(1[0-9]{3}|20[0-2][0-9])\b', str(raw_date_str))
    if match:
        year = int(match.group(1))
        return year

    return None

def format_date_key(year: Optional[int]) -> int:
    """Return integer date_key YYYY0101 or 99991231 for unknown year."""
    if year and 1000 <= year <= 2030:
        return year * 10000 + 101
    return 99991231
