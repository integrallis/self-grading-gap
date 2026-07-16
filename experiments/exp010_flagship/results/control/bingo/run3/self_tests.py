# test_bingo.py

import pytest
from solution import announce_column, create_card, mark_number, has_won

def test_announce_column_valid():
    # Numbers 1-15 map to 'B', 16-30 to 'I', 31-45 to 'N', 46-60 to 'G', 61-75 to 'O'
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
    # Numbers outside 1-75 should raise an error
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(0)
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(76)

def test_create_card_valid():
    # Creating a card with 24 unique numbers in the right ranges
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None for the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, 65]
    ]
    assert card == expected_card

def test_create_card_invalid_count():
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        create_card([1] * 24)  # 24 numbers but not unique

def test_create_card_invalid_unique():
    with pytest.raises(ValueError, match="card numbers must be unique"):
        create_card([1, 2, 3, 4, 5, 1, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
                     46, 47, 48, 49, 50, 61, 62, 63, 64, 65])

def test_create_card_invalid_range():
    with pytest.raises(ValueError, match="not valid for column B"):
        create_card([0, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65])

def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    hit = mark_number(card, 1)
    assert hit == True  # Number 1 is on the card
    assert card[0][0] is None  # Position (0, 0) should be marked (None)

def test_mark_number_no_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    hit = mark_number(card, 6)
    assert hit == False  # Number 6 is not on the card

def test_mark_number_invalid():
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_number([], 76)

def test_has_won_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert not has_won(card)  # No numbers marked

def test_has_won_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [1, 2, 3, 4, 5]:  # Mark the first row
        mark_number(card, number)
    assert has_won(card)  # Should be a win

def test_has_won_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [1, 16, 31, 46, 61]:  # Mark the first column
        mark_number(card, number)
    assert has_won(card)  # Should be a win

def test_has_won_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 
               46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [1, 17, None, 49, 61]:  # Mark the diagonal (1, 17, free, 49, 61)
        mark_number(card, number)
    assert has_won(card)  # Should be a win