import pytest
from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_valid_all_zeros():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |"
    ]
    # Expected: '000000000' (all cells decoded as 0)
    assert decode_entry(entry) == '000000000'

def test_decode_entry_valid_all_ones():
    entry = [
        "                           ",
        "    |    |    |    |    |",
        "    |    |    |    |    |"
    ]
    # Expected: '111111111' (all cells decoded as 1)
    assert decode_entry(entry) == '111111111'

def test_decode_entry_valid_ascending():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|"
    ]
    # Expected: '123456789' (each cell decoded as 1-9)
    assert decode_entry(entry) == '123456789'

def test_decode_entry_with_unreadable_cell():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|"
    ]
    entry[1] = "  |  |  |  |  |  |  |  |  |"  # Making one cell unreadable
    # Expected: '1?3456789' (first cell is unreadable)
    assert decode_entry(entry) == '1?3456789'

def test_decode_entry_invalid_lines():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |"
    ]
    # Expected: raises ValueError with message "entry must have exactly three lines"
    with pytest.raises(ValueError) as excinfo:
        decode_entry(entry)
    assert str(excinfo.value) == "entry must have exactly three lines"

def test_decode_entry_with_trailing_newline():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|",
        ""  # Trailing newline
    ]
    # Expected: '123456789' (decodes the same way)
    assert decode_entry(entry) == '123456789'

def test_decode_entry_with_trailing_spaces():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|   "  # Trailing spaces
    ]
    # Expected: '123456789' (decodes the same way as if spaces were trimmed)
    assert decode_entry(entry) == '123456789'

def test_validate_account_number_valid():
    assert validate_account_number("123456789")  # Valid checksum
    assert validate_account_number("000000000")  # Valid checksum
    assert validate_account_number("345882865")  # Valid checksum

def test_validate_account_number_invalid():
    assert not validate_account_number("111111111")  # Invalid checksum
    assert not validate_account_number("222222222")  # Invalid checksum

def test_validate_account_number_non_digit():
    assert not validate_account_number("1234a6789")  # Contains non-digit

def test_validate_account_number_not_nine_digits():
    assert not validate_account_number("12345678")  # Not exactly nine digits
    assert not validate_account_number("1234567890")  # More than nine digits

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"  # Valid entry

def test_classify_entry_invalid():
    assert classify_entry("111111111") == "111111111 ERR"  # Failing checksum

def test_classify_entry_with_unreadable():
    assert classify_entry("1?3456789") == "1?3456789 ILL"  # Unreadable cell

def test_repair_entry_already_valid():
    assert repair_entry("123456789") == "123456789"  # Already valid

def test_repair_entry_single_stroke_change():
    assert repair_entry("111111111") == "711111111"  # Changes to a valid number
    assert repair_entry("777777777") == "777777177"  # Changes to a valid number
    assert repair_entry("200000000") == "200800000"  # Changes to a valid number
    assert repair_entry("333333333") == "333393333"  # Changes to a valid number

def test_repair_entry_single_unreadable():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|"
    ]
    entry[1] = "  |  |  |  |  |  |  |  |  |"  # Making one cell unreadable
    # Expected: '123456789' (repairs to valid number)
    assert repair_entry(entry) == "123456789"

def test_repair_entry_multiple_valid_candidates():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"  # Multiple repairs

def test_repair_entry_with_two_unreadable():
    assert repair_entry("1??345678") == "1??345678 ILL"  # Cannot repair

def test_repair_entry_no_valid_single_stroke():
    assert repair_entry("222222222") == "222222222 ERR"  # No valid repair

def test_repair_entry_ambiguous_cases():
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"

def test_repair_entry_single_unreadable_cell():
    entry = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |__|__|__|__|__|__|__|__|__|"
    ]
    entry[1] = "  |  |  |  |  |  |  |  |  |"  # Making one cell unreadable
    # Expected: '123456789' (repairs to valid number)
    assert repair_entry(entry) == "123456789"