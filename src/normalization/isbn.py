import re
from typing import Optional

def clean_isbn(isbn_str: str) -> str:
    """Remove spaces, hyphens, and non-alphanumeric characters except trailing X/x for ISBN-10."""
    if not isbn_str:
        return ""
    s = re.sub(r'[^0-9Xx]', '', str(isbn_str).upper())
    return s

def validate_isbn10(isbn10: str) -> bool:
    """Validate ISBN-10 checksum."""
    isbn10 = str(isbn10).upper()
    if len(isbn10) != 10:
        return False
    if not re.match(r'^\d{9}[\dX]$', isbn10):
        return False
    
    total = 0
    for i in range(9):
        total += int(isbn10[i]) * (10 - i)
    
    last_char = isbn10[9]
    total += 10 if last_char == 'X' else int(last_char)
    
    return total % 11 == 0


def validate_isbn13(isbn13: str) -> bool:
    """Validate ISBN-13 checksum."""
    if len(isbn13) != 13 or not isbn13.isdigit():
        return False
    
    total = 0
    for i in range(12):
        weight = 1 if i % 2 == 0 else 3
        total += int(isbn13[i]) * weight
    
    check_digit = (10 - (total % 10)) % 10
    return check_digit == int(isbn13[12])

def convert_isbn10_to_13(isbn10: str) -> Optional[str]:
    """Convert valid ISBN-10 to ISBN-13 format."""
    clean = clean_isbn(isbn10)
    if not validate_isbn10(clean):
        return None
    
    prefix = "978" + clean[:9]
    total = 0
    for i in range(12):
        weight = 1 if i % 2 == 0 else 3
        total += int(prefix[i]) * weight
    
    check_digit = (10 - (total % 10)) % 10
    return prefix + str(check_digit)

def normalize_isbn(raw_isbn: str) -> Optional[str]:
    """Return clean valid ISBN-13 string or converted ISBN-10 -> ISBN-13."""
    clean = clean_isbn(raw_isbn)
    if len(clean) == 13 and validate_isbn13(clean):
        return clean
    if len(clean) == 10 and validate_isbn10(clean):
        return convert_isbn10_to_13(clean)
    return None
