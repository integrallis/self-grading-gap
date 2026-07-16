# test_bingo.py

import pytest
from solution import announce_column, create_card, mark_number, check_win

def test_announce_column_valid_b():
    assert announce_column(1) == 'B'  # 1 maps to B
    assert announce_column(15) == 'B'  # 15 maps to B

def test_announce_column_valid_i():
    assert announce_column(16) == 'I'  # 16 maps to I
    assert announce_column(30) == 'I'  # 30 maps to I

def test_announce_column_valid_n():
    assert announce_column(31) == 'N'  # 31 maps to N
    assert announce_column(45) == 'N'  # 45 maps to N

def test_announce_column_valid_g():
    assert announce_column(46) == 'G'  # 46 maps to G
    assert announce_column(60) == 'G'  # 60 maps to G

def test_announce_column_valid_o():
    assert announce_column(61) == 'O'  # 61 maps to O
    assert announce_column(75) == 'O'  # 75 maps to O

def test_announce_column_invalid():
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(0)  # outside the valid range
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(76)  # outside the valid range

def test_create_card_valid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # 24 unique numbers
    card = create_card(card_numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None for the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, 65]
    ]
    assert card == expected_card

def test_create_card_invalid_count():
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1] * 23)  # 23 numbers, too few
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1] * 25)  # 25 numbers, too many

def test_create_card_invalid_unique():
    with pytest.raises(Exception, match=r"^card numbers must be unique$"):
        create_card([1, 1, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                     47, 48, 49, 50, 61, 62, 63, 64, 65])  # 24 numbers with duplicates

def test_create_card_invalid_range():
    with pytest.raises(Exception, match="B"):
        create_card([76, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                     47, 48, 49, 50, 61, 62, 63, 64, 65])  # invalid B column entry

def test_mark_number_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    result = mark_number(card, 1)  # 1 is on the card
    assert result  # should report hit
    assert card[0][0] is None  # position of 1 should now be marked

def test_mark_number_no_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    result = mark_number(card, 6)  # 6 is not on the card
    assert result is False  # should report no hit
    assert all(cell is not None for row in card for cell in row if cell is not None)  # no cell should be marked

def test_mark_number_invalid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number(card, 0)  # invalid low number
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number(card, 76)  # invalid high number

def test_check_win_no_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    assert not check_win(card)  # fresh card

def test_check_win_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 1)
    mark_number(card, 2)
    mark_number(card, 3)
    mark_number(card, 4)
    mark_number(card, 5)  # complete first row
    assert check_win(card)  # should report a win

def test_check_win_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 1)
    mark_number(card, 16)
    mark_number(card, 31)
    mark_number(card, 46)
    mark_number(card, 61)  # complete first column
    assert check_win(card)  # should report a win

def test_check_win_diagonal_win_top_left_to_bottom_right():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 1)  # top left
    mark_number(card, 17)  # center left
    mark_number(card, 49)  # center right
    mark_number(card, 65)  # bottom right
    assert check_win(card)  # should report a win

def test_check_win_diagonal_win_bottom_left_to_top_right():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 61)  # bottom left
    mark_number(card, 47)  # center left
    mark_number(card, 33)  # center
    mark_number(card, 19)  # center right
    mark_number(card, 5)  # top right
    assert check_win(card)  # should report a win

def test_check_win_no_win_incomplete_row():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 1)
    mark_number(card, 2)
    mark_number(card, 3)  # incomplete row
    assert not check_win(card)  # should not report a win

def test_check_win_no_win_scattered_marks():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 
                    47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(card_numbers)
    mark_number(card, 1)
    mark_number(card, 16)  # scattered marks
    assert not check_win(card)  # should not report a win