# test_account_number_occr.py

import pytest
from solution import decode_entry, validate_checksum, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|",
    ]
    # Decodes to "000000000"
    expected = "000000000"
    assert decode_entry(input_data) == expected

def test_decode_entry_all_ones():
    input_data = [
        "                     ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |",
    ]
    # Decodes to "111111111"
    expected = "111111111"
    assert decode_entry(input_data) == expected

def test_decode_entry_canonical_ascending():
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  ||_  _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|",
    ]
    # Decodes to "123456789"
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_decode_entry_with_unreadable_cell():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_||_|",
        "|_||_  _|  | _||_|  ||_| _|",
    ]
    # Decodes to "?23456789" (the first cell is unreadable)
    expected = "?23456789"
    assert decode_entry(input_data) == expected

def test_decode_entry_invalid_lines_count():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_||_|",
        # Only two lines, should fail
    ]
    # Raises error with the message "entry must have exactly three lines"
    with pytest.raises(Exception, match=r"^entry must have exactly three lines$"):
        decode_entry(input_data)

def test_decode_entry_with_four_nonblank_lines():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "|_  _||_||_ |_   ||_||_|",
        "|_||_  _|  | _||_|  ||_| _|",
        "|_||_  _|  | _||_|  ||_| _|",
    ]
    # Raises error with the message "entry must have exactly three lines"
    with pytest.raises(Exception, match=r"^entry must have exactly three lines$"):
        decode_entry(input_data)

def test_decode_entry_with_trailing_blank_line():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "|_  _||_||_ |_   ||_||_|",
        "|_||_  _|  | _||_|  ||_| _|",
        ""
    ]
    # Decodes to "123456789" (trailing blank line is tolerated)
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_decode_entry_with_short_line():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "|_  _||_||_ |_   ||_||_|  ",
        "|_||_  _|  | _||_|  ||_| _|",
    ]
    # Decodes to "123456789" (short line treated as padded)
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_validate_checksum_valid():
    assert validate_checksum("345882865")  # Valid
    assert validate_checksum("123456789")  # Valid
    assert validate_checksum("000000000")  # Valid

def test_validate_checksum_invalid():
    assert not validate_checksum("111111111")  # Invalid

def test_validate_checksum_non_digit_character():
    assert not validate_checksum("12345678A")  # Invalid

def test_validate_checksum_not_nine_characters():
    assert not validate_checksum("12345678")  # Invalid

def test_validate_checksum_too_long():
    assert not validate_checksum("1234567890")  # Invalid

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"

def test_classify_entry_with_error():
    assert classify_entry("111111111") == "111111111 ERR"

def test_classify_entry_with_unreadable():
    assert classify_entry("?23456789") == "?23456789 ILL"

def test_classify_entry_with_multiple_unreadable_cells():
    assert classify_entry("??23456789") == "??23456789 ILL"

def test_repair_entry_valid():
    assert repair_entry("123456789") == "123456789"

def test_repair_entry_single_stroke_change():
    assert repair_entry("111111111") == "711111111"  # Example of repair
    assert repair_entry("777777777") == "777777177"  # Example of repair
    assert repair_entry("200000000") == "200800000"  # Example of repair
    assert repair_entry("333333333") == "333393333"  # Example of repair

def test_repair_entry_ambiguous():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"

def test_repair_entry_checksum_failing_no_valid_repair():
    assert repair_entry("222222222") == "222222222 ERR"