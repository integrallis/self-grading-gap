from solution import decode_entry, validate_account_number, classify_entry, repair_entry

def test_decode_entry_all_zeros():
    input_data = [
        " _  _  _  _  _  _  _  _  _ ",
        "| || || || || || || || || |",
        "|_||_||_||_||_||_||_||_||_|"
    ]
    expected = "000000000"
    assert decode_entry(input_data) == expected

def test_decode_entry_all_ones():
    input_data = [
        "     _  _  _  _  _  _  _  _ ",
        "  |  |  |  |  |  |  |  |  |",
        "  |  |  |  |  |  |  |  |  |"
    ]
    expected = "111111111"
    assert decode_entry(input_data) == expected

def test_decode_entry_canonical_example():
    input_data = [
        " _     _  _     _  _  _  _  _ ",
        "| |  | _| _||_||_ |_   ||_||_|",
        "|_|  ||_  _|  | _||_|  ||_| _|"
    ]
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_decode_entry_unreadable_cell():
    input_data = [
        " _     _  _     _  _  _  _  _ ",
        "| |  | _| _||_||_ |_   || | |_|",
        "|_|  ||_  _|  | _||_|  ||_| _|"
    ]
    expected = "12345?789"
    assert decode_entry(input_data) == expected

def test_decode_entry_invalid_lines():
    input_data = [
        " _     _  _     _  _  _  _  _ ",
        "| |  | _| _||_||_ |_   ||_||_|"
    ]
    expected = "entry must have exactly three lines"
    with pytest.raises(ValueError) as excinfo:
        decode_entry(input_data)
    assert str(excinfo.value) == expected

def test_decode_entry_with_trailing_newline():
    input_data = [
        " _     _  _     _  _  _  _  _ ",
        "| |  | _| _||_||_ |_   ||_||_|",
        "|_|  ||_  _|  | _||_|  ||_| _|",
        ""
    ]
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_decode_entry_with_short_line():
    input_data = [
        " _     _  _     _  _  _  _  _ ",
        "| |  | _| _||_||_ |_   ||_||_| ",
        "|_|  ||_  _|  | _||_|  ||_| _| "
    ]
    expected = "123456789"
    assert decode_entry(input_data) == expected

def test_validate_account_number_valid():
    assert validate_account_number("345882865")  # Weighted sum = 3*9 + 4*8 + 5*7 + ... + 5*1 = 0 mod 11
    assert validate_account_number("123456789")  # Weighted sum = 1*9 + 2*8 + ... + 9*1 = 0 mod 11
    assert validate_account_number("000000000")  # Weighted sum = 0 mod 11

def test_validate_account_number_invalid():
    assert not validate_account_number("111111111")  # Weighted sum = 1*9 + ... + 1*1 = 45 mod 11

def test_validate_account_number_non_digit():
    assert not validate_account_number("12345A789")  # Non-digit character
    assert not validate_account_number("12345678")   # Not exactly nine characters

def test_classify_entry_valid():
    assert classify_entry("123456789") == "123456789"
    assert classify_entry("111111111 ERR") == "111111111 ERR"

def test_classify_entry_with_unreadable():
    assert classify_entry("12345?789") == "12345?789 ILL"

def test_classify_entry_invalid():
    assert classify_entry("111111111") == "111111111 ERR"

def test_repair_entry_valid():
    assert repair_entry("123456789") == "123456789"
    assert repair_entry("111111111") == "711111111"  # Example of single stroke repair

def test_repair_entry_ambiguous():
    assert repair_entry("888888888") == "888888888 AMB ['888886888', '888888880', '888888988']"

def test_repair_entry_unrepairable():
    assert repair_entry("??3456789") == "?23456789 ILL"
    assert repair_entry("222222222") == "222222222 ERR"