# test_bingo.py

import pytest
from solution import announce_column, create_card, validate_card, mark_number, check_win

# Test US-1: Announce the column letter for a call
def test_announce_column_B():
    assert announce_column(1) == 'B'  # 1-15 maps to B

def test_announce_column_I():
    assert announce_column(16) == 'I'  # 16-30 maps to I

def test_announce_column_N():
    assert announce_column(31) == 'N'  # 31-45 maps to N

def test_announce_column_G():
    assert announce_column(46) == 'G'  # 46-60 maps to G

def test_announce_column_O():
    assert announce_column(61) == 'O'  # 61-75 maps to O

def test_announce_column_out_of_range():
    with pytest.raises(ValueError) as excinfo:
        announce_column(76)
    assert str(excinfo.value) == 'number must be between 1 and 75'

# Test US-2: Lay out a card
def test_create_card_correct_layout():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None represents the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, None]
    ]
    assert card == expected_card

def test_create_card_center_space_marked():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    assert card[2][2] is None  # Center space is free

# Test US-3: Validate a card
def test_validate_card_exactly_24_numbers():
    numbers = list(range(1, 25))  # 24 unique numbers
    validate_card(numbers)  # Should not raise an error

def test_validate_card_too_few_numbers():
    numbers = list(range(1, 23))  # 22 unique numbers
    with pytest.raises(ValueError) as excinfo:
        validate_card(numbers)
    assert str(excinfo.value) == 'exactly 24 numbers are required'

def test_validate_card_duplicates():
    numbers = [1, 2, 2, 4]  # Duplicate number
    with pytest.raises(ValueError) as excinfo:
        validate_card(numbers)
    assert str(excinfo.value) == 'card numbers must be unique'

def test_validate_card_column_range():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 76]
    with pytest.raises(ValueError) as excinfo:
        validate_card(numbers)
    assert str(excinfo.value) == 'number not valid for column O'

# Test US-4: Mark called numbers
def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked, hit = mark_number(card, 1)  # 1 is on the card
    assert marked[0][0] is True  # First position should be marked
    assert hit is True  # Should report a hit

def test_mark_number_no_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked, hit = mark_number(card, 10)  # 10 is not on the card
    assert hit is False  # Should not report a hit

def test_mark_number_out_of_range():
    with pytest.raises(ValueError) as excinfo:
        mark_number([], 80)  # Invalid number
    assert str(excinfo.value) == 'number must be between 1 and 75'

# Test US-5: Detect a winning card
def test_check_win_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked = [[False] * 5 for _ in range(5)]  # No numbers marked
    assert check_win(card, marked) is False

def test_check_win_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked = [[True] * 5 for _ in range(5)]  # All marked
    assert check_win(card, marked) is True

def test_check_win_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked = [
        [True, False, False, False, False],
        [True, False, False, False, False],
        [True, False, None, False, False],  # None represents the free space
        [True, False, False, False, False],
        [True, False, False, False, False]
    ]
    assert check_win(card, marked) is True

def test_check_win_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = create_card(numbers)
    marked = [
        [True, False, False, False, True],
        [False, True, False, True, False],
        [False, False, None, False, False],  # None represents the free space
        [False, True, False, True, False],
        [True, False, False, False, True]
    ]
    assert check_win(card, marked) is True