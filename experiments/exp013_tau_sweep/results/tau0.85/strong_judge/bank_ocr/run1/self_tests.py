import pytest
from solution import decode_entry, validate_checksum, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    input_data = [
        " _  _  _  _  _  _  _  _  _",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    # Expected: "000000000"
    assert decode_entry(input_data) == "000000000"

def test_decode_entry_all_ones():
    input_data = [
        "                           ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |"
    ]
    # Expected: "111111111"
    assert decode_entry(input_data) == "111111111"

def test_decode_entry_ascending():
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    # Expected: "123456789"
    assert decode_entry(input_data) == "123456789"

def test_decode_entry_unreadable_cell():
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  | _|  | ||_  _|  | ||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    # Expected: "?23456789"
    assert decode_entry(input_data) == "?23456789"

def test_decode_entry_invalid_line_count():
    input_data = [
        " _  _  _  _  _  _  _  _  _",
        "| ||_  _|  | ||_  _|  | ||_|",
        "|_||_||_||_||_||_||_||_||_|",
        "Extra line here"  # Fourth line
    ]
    # Expected: Error with message "entry must have exactly three lines"
    with pytest.raises(Exception) as exc:
        decode_entry(input_data)
    assert str(exc.value) == "entry must have exactly three lines"

def test_decode_entry_trailing_blank_line():
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|",
        ""
    ]
    # Expected: "123456789"
    assert decode_entry(input_data) == "123456789"

def test_decode_entry_with_stripped_trailing_spaces():
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_| ",
        "  ||_  _|  | _||_|  ||_| _| "
    ]
    # Expected: "123456789"
    assert decode_entry([line.rstrip() for line in input_data]) == "123456789"

def test_validate_checksum_valid():
    # Expected: True
    assert validate_checksum("345882865") == True
    assert validate_checksum("123456789") == True
    assert validate_checksum("000000000") == True

def test_validate_checksum_invalid():
    # Expected: False
    assert validate_checksum("111111111") == False

def test_validate_checksum_non_digit_character():
    # Expected: False
    assert validate_checksum("12345a789") == False
    assert validate_checksum("12345678") == False

def test_validate_checksum_overlong():
    # Expected: False
    assert validate_checksum("1234567890") == False

def test_classify_entry_valid():
    # Expected: "123456789"
    assert classify_entry("123456789") == "123456789"

def test_classify_entry_failing_checksum():
    # Expected: "111111111 ERR"
    assert classify_entry("111111111") == "111111111 ERR"

def test_classify_entry_with_unreadable_cells():
    # Expected: "?23456789 ILL"
    assert classify_entry("?23456789") == "?23456789 ILL"

def test_repair_entry_valid():
    # Expected: "123456789"
    assert repair_entry("123456789") == "123456789"

def test_repair_entry_single_stroke_change():
    # Expected: "711111111"
    assert repair_entry("111111111") == "711111111"

def test_repair_entry_single_stroke_change_valid():
    # Expected: "200800000"
    assert repair_entry("200000000") == "200800000"

def test_repair_entry_single_stroke_change_another_case():
    # Expected: "333393333"
    assert repair_entry("333333333") == "333393333"

def test_repair_entry_single_stroke_change_777777777():
    # Expected: "777777177"
    assert repair_entry("777777777") == "777777177"

def test_repair_entry_ambiguous():
    # Expected: "888888888 AMB ['888886888', '888888880', '888888988']"
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"

def test_repair_entry_ambiguous_fives():
    # Expected: "555555555 AMB ['555655555', '559555555']"
    assert repair_entry("555555555") == "555555555 AMB ['555655555', '559555555']"

def test_repair_entry_ambiguous_nines():
    # Expected: "490067715 AMB ['490067115', '490067719', '490867715']"
    assert repair_entry("490067715") == "490067715 AMB ['490067115', '490067719', '490867715']"

def test_repair_entry_unrepairable():
    # Expected: "?23456789 ILL"
    input_data = [
        " _  _  _  _  _  _  _  _  _",
        "| ||_|  | ||_  _|  | ||_|",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    assert repair_entry(decode_entry(input_data)) == "?23456789 ILL"

def test_repair_entry_no_valid_single_stroke_repair():
    # Expected: "222222222 ERR"
    assert repair_entry("222222222") == "222222222 ERR"

def test_repair_entry_single_stroke_change_to_ascending():
    # Expected: "123456789"
    input_data = [
        "    _  _     _  _  _  _  _ ",
        "  | _| _||_||_ |_   ||_||_|",
        "  ||_  _|  | _||_|  ||_| _|"
    ]
    assert repair_entry(decode_entry(input_data)) == "123456789"