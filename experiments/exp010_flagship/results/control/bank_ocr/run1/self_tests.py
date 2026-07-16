# test_account_ocr.py

from solution import decode_entry, validate_checksum, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "000000000"  # All cells decode to '0'
    assert decode_entry(input_data) == expected_output

def test_decode_entry_all_ones():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |"
    ]
    expected_output = "111111111"  # All cells decode to '1'
    assert decode_entry(input_data) == expected_output

def test_decode_entry_canonical_ascending():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_||_|",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "123456789"  # Each cell decodes to '1' through '9'
    assert decode_entry(input_data) == expected_output

def test_decode_entry_with_unreadable_cells():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_  |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "1?3456789"  # One cell is unreadable
    assert decode_entry(input_data) == expected_output

def test_decode_entry_with_invalid_shape():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_||_|"
    ]
    expected_output = "entry must have exactly three lines"
    with pytest.raises(ValueError) as excinfo:
        decode_entry(input_data)
    assert str(excinfo.value) == expected_output

def test_decode_entry_with_trailing_blank_line():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_ |_   ||_||_|",
        "|_||_||_||_||_||_||_||_||_|",
        ""
    ]
    expected_output = "123456789"  # Trailing blank line does not affect decoding
    assert decode_entry(input_data) == expected_output

def test_validate_checksum_valid():
    assert validate_checksum("345882865")  # Weighted sum is divisible by 11
    assert validate_checksum("123456789")  # Weighted sum is divisible by 11
    assert validate_checksum("000000000")  # Weighted sum is divisible by 11

def test_validate_checksum_invalid():
    assert not validate_checksum("111111111")  # Weighted sum is not divisible by 11
    assert not validate_checksum("222222222")  # Weighted sum is not divisible by 11

def test_validate_checksum_non_digit_or_invalid_length():
    assert not validate_checksum("12345678a")  # Non-digit character present
    assert not validate_checksum("1234567890")  # Not exactly 9 characters long

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"  # Valid entry

def test_classify_entry_with_error():
    assert classify_entry("111111111") == "111111111 ERR"  # Fails checksum

def test_classify_entry_with_unreadable():
    assert classify_entry("1?3456789") == "1?3456789 ILL"  # Unreadable cells present

def test_repair_entry_valid():
    assert repair_entry("123456789") == "123456789"  # Already valid and readable

def test_repair_entry_single_stroke_change():
    assert repair_entry("111111111") == "711111111"  # One stroke change repairs it

def test_repair_entry_multiple_possible_repair():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"  # Multiple valid repairs

def test_repair_entry_unrepairable_with_multiple_unreadable():
    assert repair_entry("1?3456789") == "1?3456789 ILL"  # Multiple unreadable cells

def test_repair_entry_checksum_failing_no_valid_repair():
    assert repair_entry("222222222") == "222222222 ERR"  # Fails checksum and no valid repair