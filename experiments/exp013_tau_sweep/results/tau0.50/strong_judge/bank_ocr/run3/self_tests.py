from solution import decode_entry, validate_account_number, classify_entry, repair_entry
import pytest

def test_decode_entry_all_zeros():
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    # Each cell decodes to '0', so the result should be '000000000'
    assert decode_entry(entry) == '000000000'

def test_decode_entry_all_ones():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|  |  |  |  |  |  |  |"
    ]
    # Each cell decodes to '1', so the result should be '111111111'
    # This input is malformed due to extra character, so expected is "cannot verify"
    with pytest.raises(ValueError, match="^cannot verify$"):
        decode_entry(entry)

def test_decode_entry_ascending():
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    # Each cell decodes to '123456789'
    assert decode_entry(entry) == '123456789'

def test_decode_entry_with_invalid_cell():
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _|???  ||_| _|"
    ]
    # One cell is invalid, so it should decode to '?23456789'
    assert decode_entry(entry) == '?23456789'

def test_decode_entry_invalid_lines():
    entry = [
        " _  _  _  _  _  _  _  _  _ ",
        "| ||_  _||_||_||_  | ||_||_ "
    ]
    # Invalid number of lines
    with pytest.raises(ValueError, match="^entry must have exactly three lines$"):
        decode_entry(entry)

def test_decode_entry_with_trailing_newline():
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|",
        ""
    ]
    # Trailing new line should not affect decoding
    assert decode_entry(entry) == '123456789'

def test_decode_entry_with_short_lines():
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    # Short lines should be padded with spaces
    entry[0] = entry[0].rstrip()  # Remove trailing spaces from first line
    assert decode_entry(entry) == '123456789'

def test_validate_account_number_valid():
    assert validate_account_number('345882865')  # Weighted sum = 0 (valid)
    assert validate_account_number('123456789')   # Weighted sum = 0 (valid)
    assert validate_account_number('000000000')   # Weighted sum = 0 (valid)

def test_validate_account_number_invalid():
    assert not validate_account_number('111111111')  # Weighted sum = 1 (invalid)

def test_validate_account_number_non_digit():
    assert not validate_account_number('12345678a')  # Non-digit character
    assert not validate_account_number('12345678')    # Not 9 digits

def test_validate_account_number_too_long():
    assert not validate_account_number('1234567890')  # Too long

def test_classify_entry_readable_valid():
    assert classify_entry('123456789') == '123456789'  # Valid and readable

def test_classify_entry_readable_invalid():
    assert classify_entry('111111111') == '111111111 ERR'  # Invalid checksum

def test_classify_entry_with_unreadable_cells():
    assert classify_entry('?23456789') == '?23456789 ILL'  # Unreadable cell

def test_repair_entry_already_valid():
    assert repair_entry('123456789') == '123456789'  # Unchanged

def test_repair_entry_single_stroke_change():
    assert repair_entry('111111111') == '711111111'  # One stroke change yields valid number
    assert repair_entry('777777777') == '777777177'  # One stroke change yields valid number
    assert repair_entry('200000000') == '200800000'  # One stroke change yields valid number
    assert repair_entry('333333333') == '333393333'  # One stroke change yields valid number

def test_repair_entry_single_unreadable_cell():
    entry = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    # Damaging the first digit
    entry[1] = "  |  |  |  |  |  |  |  |  |"  # Damaged
    assert repair_entry(entry) == '123456789'  # Unreadable cell can be repaired

def test_repair_entry_multiple_valid_options():
    assert repair_entry('888888888') == '888888888 AMB [\'888886888\', \'888888880\', \'888888988\']'
    assert repair_entry('555555555') == '555555555 AMB [\'555655555\', \'559555555\']'
    assert repair_entry('490067715') == '490067715 AMB [\'490067115\', \'490067719\', \'490867715\']'

def test_repair_entry_two_unreadable_cells():
    assert repair_entry('??2345678') == '?2345678 ILL'  # Two unreadable cells

def test_repair_entry_no_valid_single_stroke():
    assert repair_entry('222222222') == '222222222 ERR'  # No valid single-stroke repair