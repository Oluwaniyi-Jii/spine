import re
import unicodedata

PUBLISHER_SYNONYMS = {
    r'\bpenguin books\b': 'Penguin',
    r'\bpenguin classics\b': 'Penguin',
    r'\bpenguin group\b': 'Penguin',
    r'\bpenguin random house\b': 'Penguin Random House',
    r'\bcharles scribner\'?s sons\b': 'Scribner',
    r'\bscribners?\b': 'Scribner',
    r'\bharper \& brothers\b': 'HarperCollins',
    r'\bharpercollins publishers\b': 'HarperCollins',
    r'\boup\b': 'Oxford University Press',
    r'\boxford university press\b': 'Oxford University Press'
}

def remove_diacritics(text: str) -> str:
    """Strip accents and diacritics from text string."""
    if not text:
        return ""
    nfkd = unicodedata.normalize('NFKD', str(text))
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def sanitize_title(title: str) -> str:
    """
    Standardize title string:
    - Handle trailing articles like "Great Gatsby, The" -> "The Great Gatsby"
    - Normalize whitespace and casing
    """
    if not title:
        return ""
    
    t = remove_diacritics(title).strip()
    
    # Remove bracketed descriptions e.g. "The Great Gatsby [1925]"
    t = re.sub(r'\[.*?\]', '', t).strip()

    # Check for "Title, The" / "Title, A" / "Title, An"
    article_match = re.match(r'^(.*),\s*(the|a|an)$', t, re.IGNORECASE)
    if article_match:
        t = f"{article_match.group(2).capitalize()} {article_match.group(1).strip()}"
    
    # Normalize spaces
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def normalize_publisher(publisher_str: str) -> str:
    """Normalize messy publisher strings to canonical company names."""
    if not publisher_str:
        return "Unknown Publisher"
    
    p = remove_diacritics(publisher_str).strip()
    p_lower = p.lower()
    
    for pattern, canonical in PUBLISHER_SYNONYMS.items():
        if re.search(pattern, p_lower):
            return canonical
            
    # Clean common suffixes like "Inc.", "Ltd.", "Co."
    p = re.sub(r'\b(inc|ltd|llc|co|corp|corporation|company|publishers?|publishing)\.?\b', '', p, flags=re.IGNORECASE)
    p = re.sub(r'\s+', ' ', p).strip(" ,.-")
    
    return p.title() if p else "Unknown Publisher"
