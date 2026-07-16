import pytest
from solution import (
    announce_column,
    create_card,
    validate_card,
    mark_number,
    check_win
)

def test_announce_column_valid():
    # 1-15 maps to 'B', 16-30 maps to 'I', 31-45 maps to 'N', 46-60 maps to 'G', 61-75 maps to 'O'
    assert announce_column(1) == 'B'
    assert announce_column(15) == 'B'
    assert announce_column(16) == 'I'
    assert announce_column(30) == 'I'
    assert announce_column(31) == 'N'
    assert announce_column(45) == 'N'
    assert announce_column(46) == 'G'
    assert announce_column(60) == 'G'
    assert announce_column(61) == 'O'
    assert announce_column(75) == 'O'

def test_announce_column_invalid():
    # Numbers outside the range 1-75 should raise an error
    with pytest.raises(ValueError) as excinfo:
        announce_column(0)
    assert str(excinfo.value) == "number must be between 1 and 75"
    
    with pytest.raises(ValueError) as excinfo:
        announce_column(76)
    assert str(excinfo.value) == "number must be between 1 and 75"

def test_create_card_valid():
    # Example card numbers, should be unique and within column limits
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # 24 unique numbers
    card = create_card(card_numbers)
    assert card[0] == [1, 16, 31, 46, 61]  # B column
    assert card[1] == [2, 17, 32, 47, 62]  # I column
    assert card[2] == [3, 18, 0, 48, 63]  # N column (center is 0)
    assert card[3] == [4, 19, 33, 49, 64]  # G column
    assert card[4] == [5, 20, 34, 50, 65]  # O column

def test_validate_card_invalid_count():
    # Must have exactly 24 numbers
    with pytest.raises(ValueError) as excinfo:
        validate_card([1] * 23)  # 23 duplicates
    assert str(excinfo.value) == "exactly 24 numbers are required"

    with pytest.raises(ValueError) as excinfo:
        validate_card([1] * 25)  # 25 duplicates
    assert str(excinfo.value) == "exactly 24 numbers are required"

def test_validate_card_unique_numbers():
    # Must be unique numbers
    with pytest.raises(ValueError) as excinfo:
        validate_card([1, 2, 3, 4, 5, 1])  # Duplicate 1
    assert str(excinfo.value) == "card numbers must be unique"

def test_validate_card_column_ranges_B():
    # Check column range constraints for B
    with pytest.raises(ValueError) as excinfo:
        validate_card([80, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
                       46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 80 is invalid for 'B'
    assert str(excinfo.value) == "number 80 is not valid for column B"

def test_validate_card_column_ranges_I():
    # Check column range constraints for I
    with pytest.raises(ValueError) as excinfo:
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
                       46, 47, 48, 49, 50, 61, 62, 63, 64, 66])  # 66 is invalid for 'I'
    assert str(excinfo.value) == "number 66 is not valid for column I"

def test_validate_card_column_ranges_N():
    # Check column range constraints for N
    with pytest.raises(ValueError) as excinfo:
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 36, 
                       46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 36 is invalid for 'N'
    assert str(excinfo.value) == "number 36 is not valid for column N"

def test_validate_card_column_ranges_G():
    # Check column range constraints for G
    with pytest.raises(ValueError) as excinfo:
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
                       46, 47, 48, 49, 50, 61, 62, 63, 64, 66])  # 66 is invalid for 'G'
    assert str(excinfo.value) == "number 66 is not valid for column G"

def test_validate_card_column_ranges_O():
    # Check column range constraints for O
    with pytest.raises(ValueError) as excinfo:
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
                       46, 47, 48, 49, 50, 61, 62, 63, 64, 76])  # 76 is invalid for 'O'
    assert str(excinfo.value) == "number 76 is not valid for column O"

def test_mark_number_valid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    assert mark_number(card, 1) == True  # 1 is on the card, so it should mark it
    assert card[0][0] == 0  # 1 is marked (set to 0)

def test_mark_number_invalid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    with pytest.raises(ValueError) as excinfo:
        mark_number(card, 99)  # 99 is not on the card, should raise an error
    assert str(excinfo.value) == "number must be between 1 and 75"

def test_mark_number_off_card():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    assert mark_number(card, 15) == False  # 15 is not on the card, should not mark anything
    assert card[0][0] == 1  # Check that 1 is still unmarked

def test_mark_number_boundary_calls():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    assert mark_number(card, 1) == True
    assert card[0][0] == 0  # Marked
    
    assert mark_number(card, 75) == False  # 75 is not on the card, should not mark anything

def test_check_win_no_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    assert not check_win(card)  # No wins yet

def test_check_win_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [1, 2, 3, 4, 5]:  # Marking a full row
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [61, 62, 63, 64, 65]:  # Marking a full column
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_middle_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [3, 18, 48, 63]:  # Marking the middle row with the free space
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_N_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [31, 32, 33, 34]:  # Marking the N column with the free space
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [1, 17, 49, 65]:  # Marking one diagonal
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_other_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [61, 47, 19, 5]:  # Marking the other diagonal
        mark_number(card, number)
    assert check_win(card)  # This should now be a win

def test_check_win_incomplete_row():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [1, 2, 3, 4]:  # Incomplete row
        mark_number(card, number)
    assert not check_win(card)  # This should not be a win

def test_check_win_scattered_marks():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for number in [1, 17, 49]:  # Scattered marks
        mark_number(card, number)
    assert not check_win(card)  # This should not be a win

def test_non_center_spaces_start_unmarked():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    for r in range(5):
        for c in range(5):
            if not (r == 2 and c == 2):  # Skip center
                assert card[r][c] != 0  # Non-center spaces should be unmarked