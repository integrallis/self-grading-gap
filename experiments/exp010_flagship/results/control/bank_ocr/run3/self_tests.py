from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    input_entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "000000000"  # All zeros
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_all_ones():
    input_entry = [
        "     _           _           ",
        "  |  _|  |_|  |_|  |_|  |_| ",
        "  |_|  _|  |_|  |_|  |_|  |_|"
    ]
    expected_output = "111111111"  # All ones
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_canonical_case():
    input_entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "123456789"  # Canonical ascending
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_with_invalid_cell():
    input_entry = [
        " _  _  _     _  _  _  _  _ ",
        "| ||_|| ||_||_||_ |_   ||_||_",
        "|_|| ||_  _|  | _||_|  ||_| _|"
    ]
    expected_output = "12?456789"  # One invalid cell
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_three_lines_only():
    input_entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected_output = "123456789"  # Exactly three lines
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_tolerates_blank_line():
    input_entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|",
        ""
    ]
    expected_output = "123456789"  # Trailing blank line
    assert decode_entry(input_entry) == expected_output

def test_decode_entry_shorter_than_27_characters():
    input_entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_|| "
    ]
    expected_output = "123456789"  # Short line treated as padded
    assert decode_entry(input_entry) == expected_output

def test_validate_account_number_valid():
    assert validate_account_number("345882865")  # Valid checksum
    assert validate_account_number("123456789")  # Valid checksum
    assert validate_account_number("000000000")  # Valid checksum

def test_validate_account_number_invalid():
    assert not validate_account_number("111111111")  # Invalid checksum

def test_validate_account_number_non_digit():
    assert not validate_account_number("1234a6789")  # Non-digit character
    assert not validate_account_number("12345678!")  # Non-digit character

def test_validate_account_number_not_nine_digits():
    assert not validate_account_number("12345678")  # Not nine characters
    assert not validate_account_number("1234567890")  # Not nine characters

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"  # Valid entry

def test_classify_entry_valid_error():
    assert classify_entry("111111111") == "111111111 ERR"  # Valid but fails checksum

def test_classify_entry_with_unreadable():
    assert classify_entry("12?456789") == "12?456789 ILL"  # Unreadable cell

def test_repair_entry_no_repair_needed():
    assert repair_entry("123456789") == "123456789"  # No repair needed

def test_repair_entry_single_valid_repair():
    assert repair_entry("111111111") == "711111111"  # One valid repair

def test_repair_entry_ambiguous_repair():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"  # Ambiguous repairs

def test_repair_entry_with_multiple_unreadable():
    assert repair_entry("12?45678?") == "12?45678? ILL"  # Multiple unreadable cells

def test_repair_entry_valid_checksum_with_no_repair():
    assert repair_entry("222222222") == "222222222 ERR"  # Valid but fails checksum with no repair