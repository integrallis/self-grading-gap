import pytest
from solution import announce_column, lay_out_card, validate_card, mark_number, detect_win

def test_announce_column_valid_b_lower():
    assert announce_column(1) == 'B'  # 1 is in range 1-15, should return 'B'

def test_announce_column_valid_b_upper():
    assert announce_column(15) == 'B'  # 15 is in range 1-15, should return 'B'

def test_announce_column_valid_i_lower():
    assert announce_column(16) == 'I'  # 16 is in range 16-30, should return 'I'

def test_announce_column_valid_i_upper():
    assert announce_column(30) == 'I'  # 30 is in range 16-30, should return 'I'

def test_announce_column_valid_n_lower():
    assert announce_column(31) == 'N'  # 31 is in range 31-45, should return 'N'

def test_announce_column_valid_n_upper():
    assert announce_column(45) == 'N'  # 45 is in range 31-45, should return 'N'

def test_announce_column_valid_g_lower():
    assert announce_column(46) == 'G'  # 46 is in range 46-60, should return 'G'

def test_announce_column_valid_g_upper():
    assert announce_column(60) == 'G'  # 60 is in range 46-60, should return 'G'

def test_announce_column_valid_o_lower():
    assert announce_column(61) == 'O'  # 61 is in range 61-75, should return 'O'

def test_announce_column_valid_o_upper():
    assert announce_column(75) == 'O'  # 75 is in range 61-75, should return 'O'

def test_announce_column_out_of_bounds_lower():
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        announce_column(0)
    assert 'number must be between 1 and 75' in str(excinfo.value)

def test_announce_column_out_of_bounds_upper():
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        announce_column(76)
    assert 'number must be between 1 and 75' in str(excinfo.value)

def test_lay_out_card_correct_order():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]  # 24 unique numbers
    card = lay_out_card(numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None for the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, 75]
    ]
    assert card == expected_card

def test_lay_out_card_incorrect_count():
    numbers = [1, 2, 3]  # only 3 numbers
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        lay_out_card(numbers)
    assert 'exactly 24 numbers are required' in str(excinfo.value)

def test_validate_card_unique_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 24]  # duplicates
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        validate_card(numbers)
    assert str(excinfo.value) == 'card numbers must be unique'

def test_validate_card_column_range():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75, 80]  # 80 is invalid
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        validate_card(numbers)
    assert 'O' in str(excinfo.value)  # Assert only the column name is in the exception

def test_validate_card_too_many_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]  # 25 numbers
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        validate_card(numbers)
    assert 'exactly 24 numbers are required' in str(excinfo.value)

def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    hit = mark_number(card, 3)  # 3 is on the card
    assert hit == True  # should report a hit
    # Check if 3 is marked (the specific representation is unspecified)

def test_mark_number_no_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    hit = mark_number(card, 10)  # 10 is not on the card
    assert hit == False  # should report no hit
    # Verify the card state is unchanged (exact verification unspecified)

def test_mark_number_out_of_bounds():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    with pytest.raises(Exception) as excinfo:  # Expecting an error
        mark_number(card, 100)  # out of bounds
    assert 'number must be between 1 and 75' in str(excinfo.value)

def test_detect_win_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    assert detect_win(card) == False  # no win initially

def test_detect_win_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark a complete row
    mark_number(card, 1)  # B1
    mark_number(card, 2)  # B2
    mark_number(card, 3)  # B3
    mark_number(card, 4)  # B4
    mark_number(card, 5)  # B5
    assert detect_win(card) == True  # should detect a win

def test_detect_win_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark a complete column
    mark_number(card, 1)  # B1
    mark_number(card, 16) # I1
    mark_number(card, 31) # N1
    mark_number(card, 46) # G1
    mark_number(card, 61) # O1
    assert detect_win(card) == True  # should detect a win

def test_detect_win_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark the main diagonal from top-left to bottom-right
    mark_number(card, 1)   # B1
    mark_number(card, 17)  # I2
    mark_number(card, 49)  # G4
    mark_number(card, 75)  # O5
    assert detect_win(card) == True  # should detect a win

def test_detect_win_opposite_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark the opposite diagonal from top-right to bottom-left
    mark_number(card, 5)   # B5
    mark_number(card, 17)  # I2
    mark_number(card, 49)  # G4
    mark_number(card, 61)  # O1
    assert detect_win(card) == True  # should detect a win

def test_detect_win_incomplete_row():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark only 4 in a row
    mark_number(card, 1)  # B1
    mark_number(card, 2)  # B2
    mark_number(card, 3)  # B3
    mark_number(card, 4)  # B4
    assert detect_win(card) == False  # should not detect a win

def test_detect_win_scattered_marks():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = lay_out_card(numbers)
    # Mark scattered numbers
    mark_number(card, 1)   # B1
    mark_number(card, 16)  # I1
    mark_number(card, 49)  # G4
    assert detect_win(card) == False  # should not detect a win