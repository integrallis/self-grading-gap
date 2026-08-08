import pytest
from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_valid_full():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    # Decodes to 123456789
    assert decode_entry(entry) == "123456789"

def test_decode_entry_all_zeros():
    entry = [
        "    _  _  _  _  _  _  _  _  _ ",
        "  ||_||_||_||_||_||_||_||_||_ ",
        "  | _||_||_||_||_||_||_||_||_ "
    ]
    # Decodes to 000000000
    assert decode_entry(entry) == "000000000"

def test_decode_entry_all_ones():
    entry = [
        "    _  _  _  _  _  _  _  _  _ ",
        "  |  |  |  |  |  |  |  |  |  ",
        "  |  |  |  |  |  |  |  |  |  "
    ]
    # Decodes to 111111111
    assert decode_entry(entry) == "111111111"

def test_decode_entry_invalid_cell():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _| |_|  ||_| _|    "
    ]
    # The third cell is unreadable, so it should return "12345????"
    assert decode_entry(entry) == "12345????"

def test_decode_entry_invalid_length():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ "
    ]
    # Raises an error for having less than 3 lines
    with pytest.raises(Exception) as exc_info:
        decode_entry(entry)
    assert str(exc_info.value) == "entry must have exactly three lines"

def test_decode_entry_more_than_three_lines():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    ",
        "    _  _     _  _  _  _  _  _ "
    ]
    # Raises an error for having more than 3 lines
    with pytest.raises(Exception) as exc_info:
        decode_entry(entry)
    assert str(exc_info.value) == "entry must have exactly three lines"

def test_decode_entry_with_trailing_newline():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    ",
        ""
    ]
    # Should decode to 123456789 ignoring the empty line
    assert decode_entry(entry) == "123456789"

def test_decode_entry_with_trailing_spaces():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    # Trailing spaces are treated as padded, should decode to 123456789
    assert decode_entry(entry) == "123456789"

def test_decode_entry_with_shortened_line():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    # Raises an error for having less than 3 lines
    with pytest.raises(Exception) as exc_info:
        decode_entry(entry[:-1])  # This will leave only two lines
    assert str(exc_info.value) == "entry must have exactly three lines"

def test_validate_account_number_valid():
    assert validate_account_number("345882865")  # Weighted sum is valid
    assert validate_account_number("123456789")  # Weighted sum is valid
    assert validate_account_number("000000000")  # Weighted sum is valid

def test_validate_account_number_invalid():
    assert not validate_account_number("111111111")  # Weighted sum is invalid
    assert not validate_account_number("12345678a")  # Contains non-digit character
    assert not validate_account_number("1234567890")  # Not exactly nine characters

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"  # Valid entry

def test_classify_entry_valid_with_error():
    assert classify_entry("111111111") == "111111111 ERR"  # Valid but checksum fails

def test_classify_entry_with_unreadable_cells():
    assert classify_entry("?23456789") == "?23456789 ILL"  # Entry with unreadable cells

def test_repair_entry_valid():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "123456789"  # Already valid

def test_repair_entry_single_stroke_change():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _| |_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "711111111"  # Single stroke change makes valid

def test_repair_entry_multiple_valid_candidates():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "888888888 AMB ['888886888', '888888880', '888888988']"  # Multiple valid repairs

def test_repair_entry_with_two_unreadable_cells():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _| ?|  ||_| _|    "
    ]
    assert repair_entry(entry) == "?23456789 ILL"  # Multiple unreadable cells can't be repaired

def test_repair_entry_checksum_fails_no_valid_repair():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "222222222 ERR"  # Checksum fails with no valid repairs

def test_repair_entry_valid_candidates():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _| |_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "200800000"  # Single stroke change repairs valid

def test_repair_entry_single_unreadable_cell():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "123456789"  # One stroke completion repairs to valid

def test_repair_entry_multiple_valid_candidates_five():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "555555555 AMB ['555655555', '559555555']"  # Multiple valid repairs

def test_repair_entry_multiple_valid_candidates_four_nine():
    entry = [
        "    _  _     _  _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_||_ ",
        "  ||_  _|  | _||_|  ||_| _|    "
    ]
    assert repair_entry(entry) == "490067715 AMB ['490067115', '490067719', '490867715']"  # Multiple valid repairs