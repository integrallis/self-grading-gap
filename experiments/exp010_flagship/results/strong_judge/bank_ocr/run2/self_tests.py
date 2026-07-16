import pytest
from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    # Entry is all zeros: "000000000"
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    assert decode_entry(entry) == "000000000"

def test_decode_entry_all_ones():
    # Entry is all ones: "111111111"
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |"
    ]
    assert decode_entry(entry) == "111111111"

def test_decode_entry_canonical():
    # Canonical ascending entry: "123456789"
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    assert decode_entry(entry) == "123456789"

def test_decode_entry_with_invalid_cell():
    # Entry with one invalid cell: "12?456789"
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    entry[0] = entry[0][:7] + " " + entry[0][8:]  # Change to invalid
    assert decode_entry(entry) == "12?456789"

def test_decode_entry_too_few_lines():
    # Entry with too few lines
    entry = [
        " _  _  _  _  _  _  _  _  _ "
    ]
    with pytest.raises(ValueError) as exc_info:
        decode_entry(entry)
    assert str(exc_info.value) == "entry must have exactly three lines"

def test_decode_entry_too_many_lines():
    # Entry with too many lines
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|",
        "",
        ""
    ]
    with pytest.raises(ValueError) as exc_info:
        decode_entry(entry)
    assert str(exc_info.value) == "entry must have exactly three lines"

def test_decode_entry_with_trailing_newline():
    # Entry with a trailing newline
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|",
        ""
    ]
    assert decode_entry(entry) == "000000000"

def test_decode_entry_with_short_lines():
    # Entry with shorter lines being padded
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    entry[1] = entry[1][:26]  # Shorten line to test padding
    assert decode_entry(entry) == "000000000"

def test_validate_account_number_valid_123456789():
    # Valid account number: "123456789"
    assert validate_account_number("123456789") is True

def test_validate_account_number_valid_000000000():
    # Valid account number: "000000000"
    assert validate_account_number("000000000") is True

def test_validate_account_number_valid_345882865():
    # Valid account number: "345882865"
    assert validate_account_number("345882865") is True

def test_validate_account_number_invalid():
    # Invalid account number: "111111111"
    assert validate_account_number("111111111") is False

def test_validate_account_number_non_digit():
    # Non-digit characters: "12345678X"
    assert validate_account_number("12345678X") is False

def test_validate_account_number_not_nine_digits():
    # Not exactly nine digits: "12345678"
    assert validate_account_number("12345678") is False

def test_validate_account_number_too_long():
    # Too long: "1234567890"
    assert validate_account_number("1234567890") is False

def test_classify_entry_valid():
    # Fully readable and valid: "123456789"
    assert classify_entry("123456789") == "123456789"

def test_classify_entry_invalid():
    # Fully readable but invalid: "111111111"
    assert classify_entry("111111111") == "111111111 ERR"

def test_classify_entry_with_unreadable():
    # Unreadable cells: "?23456789"
    assert classify_entry("?23456789") == "?23456789 ILL"

def test_repair_entry_already_valid():
    # Already valid: "123456789"
    assert repair_entry("123456789") == "123456789"

def test_repair_entry_single_repair():
    # Single stroke repair: "111111111" to "711111111"
    assert repair_entry("111111111") == "711111111"

def test_repair_entry_multiple_repair_options():
    # Multiple possible repairs: "888888888"
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"

def test_repair_entry_unreadable_cells():
    # Two unreadable cells: "?23?56789"
    assert repair_entry("?23?56789") == "?23?56789 ILL"

def test_repair_entry_no_valid_single_stroke():
    # No valid single-stroke repair: "222222222"
    assert repair_entry("222222222") == "222222222 ERR"

def test_repair_entry_unique_repair_example_777777777():
    # Unique repair: "777777777" to "777777177"
    assert repair_entry("777777777") == "777777177"

def test_repair_entry_unique_repair_example_200000000():
    # Unique repair: "200000000" to "200800000"
    assert repair_entry("200000000") == "200800000"

def test_repair_entry_unique_repair_example_333333333():
    # Unique repair: "333333333" to "333393333"
    assert repair_entry("333333333") == "333393333"

def test_repair_entry_ambiguous_repair_555555555():
    # Ambiguous repairs: "555555555"
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"

def test_repair_entry_ambiguous_repair_490067715():
    # Ambiguous repairs: "490067715"
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"

def test_repair_entry_damaged_ascending_entry():
    # Damaged ascending entry with one unreadable cell repairing to "123456789"
    assert repair_entry("12?456789") == "123456789"