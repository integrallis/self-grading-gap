from solution import decode_entry, validate_account_number, classify_entry, repair_entry
import pytest

def test_decode_entry_valid_cases():
    # AC-1.1: All zeros
    entry_zeros = " _  _  _  _  _  _  _  _  _  _ \n| || || || || || || || || || |\n|_||_||_||_||_||_||_||_||_||_|\n"
    assert decode_entry(entry_zeros) == "000000000"  # All cells represent '0'

    # AC-1.1: All ones
    entry_ones = "   \n  |  |  |  |  |  |  |  |  |\n  |  |  |  |  |  |  |  |  |\n"
    assert decode_entry(entry_ones) == "111111111"  # All cells represent '1'

    # AC-1.1: Canonical ascending entry
    entry_ascending = " _     _  _     _  _  _  _  _ \n| |  | _| _||_||_ |_   ||_||_|\n|_|  ||_  _|  | _||_|  ||_| _|\n"
    assert decode_entry(entry_ascending) == "123456789"  # Proper ascending entry

def test_decode_entry_invalid_cases():
    # AC-1.2: Invalid cell (damaged first cell)
    entry_invalid = " _  _  _  _  _  _  _  _  _  _ \n|_|| || || || || || || || || |\n|_||_||_||_||_||_||_||_||_||_|\n"
    assert decode_entry(entry_invalid) == "?00000000"  # First cell is damaged, so it becomes '?'

    # AC-1.3: Not exactly three lines
    entry_too_few_lines = " _  _  _ \n| || || |\n"
    with pytest.raises(ValueError, match=r"^entry must have exactly three lines$"):
        decode_entry(entry_too_few_lines)

    # AC-1.4: Trailing blank fourth line
    entry_with_trailing_blank = " _     _  _     _  _  _  _  _ \n| |  | _| _||_||_ |_   ||_||_|\n|_|  ||_  _|  | _||_|  ||_| _|\n\n"
    assert decode_entry(entry_with_trailing_blank) == "123456789"

    # AC-1.5: Lines shorter than 27 characters
    entry_with_spaces = " _     _  _     _  _  _  _  _ \n| |  | _| _||_||_ |_   ||_||_|\n|_|  ||_  _|  | _||_|  ||_| _|\n"
    assert decode_entry(entry_with_spaces.rstrip()) == "123456789"

def test_validate_account_number_valid_cases():
    # AC-2.1: Valid account numbers
    assert validate_account_number("345882865")  # Weighted sum = 231 (valid, divisible by 11)
    assert validate_account_number("123456789")  # Weighted sum = 165 (valid, divisible by 11)
    assert validate_account_number("000000000")  # Weighted sum = 0 (valid, divisible by 11)

def test_validate_account_number_invalid_cases():
    # AC-2.2: Invalid account number
    assert not validate_account_number("111111111")  # Weighted sum = 45 (invalid)

    # AC-2.3: Non-digit or wrong length
    assert not validate_account_number("12345678a")  # Non-digit character
    assert not validate_account_number("1234567")    # Not exactly nine characters
    assert not validate_account_number("1234567890") # Not exactly nine characters

def test_classify_entry_valid_cases():
    # AC-3.1: Readable and valid
    assert classify_entry("123456789") == "123456789"

    # AC-3.2: Readable but invalid
    assert classify_entry("111111111") == "111111111 ERR"

    # AC-3.3: Unreadable cells
    assert classify_entry("?23456789") == "?23456789 ILL"

def test_repair_entry_valid_cases():
    # AC-4.1: Already readable and valid
    assert repair_entry("123456789") == "123456789"

    # AC-4.2: Repair single-stroke change yielding valid number
    assert repair_entry("111111111") == "711111111"  # Repairs to valid checksum
    assert repair_entry("777777777") == "777777177"  # Repairs to valid checksum
    assert repair_entry("200000000") == "200800000"  # Repairs to valid checksum
    assert repair_entry("333333333") == "333393333"  # Repairs to valid checksum
    
    # Unique repair of an unreadable cell
    entry_damaged_unreadable = " _     _  _     _  _  _  _  _ \n| |  | _| _||_||_ |_   ||_||_|\n|_|  ||_  _|  | _||_|  ||_| _|\n"  # Damaged entry
    assert repair_entry(entry_damaged_unreadable) == "123456789"  # Should repair to valid ascending

    # AC-4.3: Ambiguous repairs
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"

def test_repair_entry_invalid_cases():
    # AC-4.4: Multiple unreadable cells
    assert repair_entry("??2345678") == "??2345678 ILL"

    # AC-4.5: No valid single-stroke repair
    assert repair_entry("222222222") == "222222222 ERR"