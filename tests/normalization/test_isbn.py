import pytest
from src.normalization.isbn import (
    clean_isbn, validate_isbn10, validate_isbn13,
    convert_isbn10_to_13, normalize_isbn
)

def test_clean_isbn():
    assert clean_isbn("0-7432-7356-7") == "0743273567"
    assert clean_isbn("978 0 7432 7356 5") == "9780743273565"
    assert clean_isbn("0-393-02030-X") == "039302030X"

def test_validate_isbn10():
    assert validate_isbn10("0743273567") is True
    assert validate_isbn10("097522980X") is True
    assert validate_isbn10("0000000000") is True
    assert validate_isbn10("1234567890") is False


def test_validate_isbn13():
    assert validate_isbn13("9780743273565") is True
    assert validate_isbn13("9780393020304") is True
    assert validate_isbn13("9781234567890") is False

def test_convert_isbn10_to_13():
    assert convert_isbn10_to_13("0743273567") == "9780743273565"
    assert convert_isbn10_to_13("invalid") is None

def test_normalize_isbn():
    assert normalize_isbn("0-7432-7356-7") == "9780743273565"
    assert normalize_isbn("978-0-7432-7356-5") == "9780743273565"
    assert normalize_isbn("12345") is None
