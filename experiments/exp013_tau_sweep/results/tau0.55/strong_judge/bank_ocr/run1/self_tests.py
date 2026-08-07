import pytest
from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    entry = [" _  _  _  _  _  _  _  _  _ ",
             "| || || || || || || || || |",
             "|_||_||_||_||_||_||_||_||_|"]
    expected = "000000000"  # Each cell corresponds to '0'
    assert decode_entry(entry) == expected

def test_decode_entry_all_ones():
    entry = ["     _  _  _  _  _  _  _  _ ",
             "  |  |  |  |  |  |  |  |  |",
             "  |_|  |  |  |  |  |  |  |"]
    expected = "111111111"  # Each cell corresponds to '1'
    assert decode_entry(entry) == expected

def test_decode_entry_canonical_example():
    entry = ["    _  _     _  _  _  _  _ ",
             "  | _| _||_||_ |_   ||_||_|",
             "  ||_  _|  | _||_|  ||_| _|"]
    expected = "123456789"  # Each cell corresponds to '1' to '9'
    assert decode_entry(entry) == expected

def test_decode_entry_with_unreadable_cell():
    entry = ["    _  _     _  _  _  _  _ ",
             "  | _| _||_||_ |_   ||_||_|",
             "  ||_  _|  | _||_|  |  | _|"]  
    expected = "12?456789"  # Cell for '3' is unreadable
    assert decode_entry(entry) == expected

def test_decode_entry_invalid_line_count():
    entry = [" _  _  _  _  _  _  _  _  _ ",
             "|_   |  ||_  |  ||_  | |"]
    with pytest.raises(Exception, match=r"^entry must have exactly three lines$"):
        decode_entry(entry)

def test_decode_entry_trailing_blank_line():
    entry = [" _  _  _  _  _  _  _  _  _ ",
             "|_   |  ||_  |  ||_  | |",
             "|_  |  ||_  |  |  |  | |",
             ""]
    expected = "123456789"  # Trailing blank line should not affect decoding
    assert decode_entry(entry) == expected

def test_decode_entry_short_line():
    entry = [" _  _  _  _  _  _  _  _  _ ",
             "|_   |  ||_  |  ||_  | ",
             "|_  |  ||_  |  |  |  | |"] 
    expected = "123456789"  # Short line treated as padded
    assert decode_entry(entry) == expected

def test_validate_account_number_valid():
    assert validate_account_number("345882865")  # Valid account number
    assert validate_account_number("123456789")  # Valid account number
    assert validate_account_number("000000000")  # Valid account number

def test_validate_account_number_invalid():
    assert not validate_account_number("111111111")  # Invalid account number
    assert not validate_account_number("12345678A")  # Contains non-digit
    assert not validate_account_number("12345678")   # Not exactly nine characters
    assert not validate_account_number("1234567890")  # Overlong input

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"  # Fully readable and valid

def test_classify_entry_invalid():
    assert classify_entry("111111111") == "111111111 ERR"  # Checksum fails

def test_classify_entry_unreadable():
    assert classify_entry("12?456789") == "12?456789 ILL"  # Unreadable cell present

def test_repair_entry_valid():
    assert repair_entry("123456789") == "123456789"  # Already valid

def test_repair_entry_single_stroke_change():
    assert repair_entry("111111111") == "711111111"  # One stroke change repairs it
    assert repair_entry("777777777") == "777777177"  # One stroke change repairs it
    assert repair_entry("200000000") == "200800000"  # One stroke change repairs it
    assert repair_entry("333333333") == "333393333"  # One stroke change repairs it

def test_repair_entry_single_unreadable_cell():
    entry = ["    _  _     _  _  _  _  _ ",
             "  | _| _||_||_ |_   ||_||_|",
             "  ||_  _|  | _||_|  |  | _|"]
    assert repair_entry(entry) == "123456789"  # Unreadable cell repaired uniquely

def test_repair_entry_ambiguous():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"  # Several valid repairs
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"  # Several valid repairs
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"  # Several valid repairs

def test_repair_entry_unrepairable():
    entry = [" _  _  _  _  _  _  _  _  _ ",
             "|_   |  ||_  |  ||_  | |",
             "|_  |  ||_  |  |  |  | |"]
    assert repair_entry(entry) == "12?456789 ILL"  # Two unreadable cells cannot be repaired

def test_repair_entry_no_valid_single_stroke():
    assert repair_entry("222222222") == "222222222 ERR"  # No valid single-stroke repair