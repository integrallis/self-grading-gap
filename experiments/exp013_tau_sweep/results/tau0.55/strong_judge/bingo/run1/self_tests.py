# test_bingo.py

import pytest
from solution import announce_column, create_card, mark_number, check_win

def test_announce_column_valid():
    assert announce_column(1) == 'B'  # 1-15 -> B
    assert announce_column(15) == 'B'  # 1-15 -> B
    assert announce_column(16) == 'I'  # 16-30 -> I
    assert announce_column(30) == 'I'  # 16-30 -> I
    assert announce_column(31) == 'N'  # 31-45 -> N
    assert announce_column(45) == 'N'  # 31-45 -> N
    assert announce_column(46) == 'G'  # 46-60 -> G
    assert announce_column(60) == 'G'  # 46-60 -> G
    assert announce_column(61) == 'O'  # 61-75 -> O
    assert announce_column(75) == 'O'  # 61-75 -> O

def test_announce_column_invalid():
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(0)
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(76)

def test_create_card_valid():
    numbers = [
        1, 2, 3, 4, 5,  # B column
        16, 17, 18, 19, 20,  # I column
        31, 32, 33, 34, 35,  # N column
        46, 47, 48, 49, 50,  # G column
        61, 62, 63, 64, 65   # O column
    ]
    card = create_card(numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None for the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, 65],
    ]
    assert card == expected_card

def test_create_card_invalid_count():
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1]*25)  # More than 24
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1]*23)  # Less than 24

def test_create_card_invalid_unique():
    with pytest.raises(Exception, match="card numbers must be unique"):
        create_card([1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])  # Duplicates present

def test_create_card_invalid_range_b():
    with pytest.raises(Exception, match="not valid for column B"):
        create_card([1, 2, 3, 4, 16, 17, 18, 19, 20, 31, 32, 33, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 16 not valid for B

def test_create_card_invalid_range_i():
    with pytest.raises(Exception, match="not valid for column I"):
        create_card([1, 2, 3, 4, 5, 31, 32, 33, 34, 35, 18, 19, 20, 21, 22, 46, 47, 48, 49, 50, 61, 62, 63, 64])  # 31, 32 not valid for I

def test_create_card_invalid_range_n():
    with pytest.raises(Exception, match="not valid for column N"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64])  # 31 not valid for N

def test_create_card_invalid_range_g():
    with pytest.raises(Exception, match="not valid for column G"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 66])  # 66 not valid for G

def test_create_card_invalid_range_o():
    with pytest.raises(Exception, match="not valid for column O"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 61, 62, 63, 64, 75])  # 75 not valid for O

def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)  # Mark 1
    # Check here should depend on the API contract if it specifies how marking works
    assert card[0][0] is None  # Position (0, 0) should now be marked (None)

def test_mark_number_no_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 6)  # Call a number not on the card
    assert card[0][0] == 1  # Position (0, 0) should still be 1

def test_mark_number_invalid():
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number([], 0)
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number([], 76)

def test_check_win_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert check_win(card) == False  # No win yet

def test_check_win_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)  # (0,0)
    mark_number(card, 2)  # (0,1)
    mark_number(card, 3)  # (0,2)
    mark_number(card, 4)  # (0,3)
    mark_number(card, 5)  # (0,4)
    assert check_win(card) == True  # Win in the first row

def test_check_win_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)   # (0,0)
    mark_number(card, 16)  # (1,0)
    mark_number(card, 31)  # (2,0)
    mark_number(card, 46)  # (3,0)
    mark_number(card, 61)  # (4,0)
    assert check_win(card) == True  # Win in the first column

def test_check_win_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)   # (0,0)
    mark_number(card, 17)  # (1,1)
    mark_number(card, 33)  # (2,2)
    mark_number(card, 49)  # (3,3)
    mark_number(card, 65)  # (4,4)
    assert check_win(card) == True  # Win in diagonal

def test_check_win_anti_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 61)  # (4,0)
    mark_number(card, 47)  # (3,1)
    mark_number(card, 33)  # (2,2)
    mark_number(card, 19)  # (1,3)
    mark_number(card, 5)   # (0,4)
    assert check_win(card) == True  # Win in anti-diagonal

def test_check_win_no_complete_line():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)
    mark_number(card, 2)
    mark_number(card, 3)
    assert check_win(card) == False  # No complete line

def test_check_win_scattered_marks():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)   # (0,0)
    mark_number(card, 16)  # (1,0)
    assert check_win(card) == False  # No complete line

def test_mark_number_valid_boundary_75():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 75]
    card = create_card(numbers)
    mark_number(card, 75)  # Call the valid boundary number
    assert card[4][4] is None  # Position (4, 4) should now be marked (None)

def test_check_win_middle_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 18)  # (2,1)
    mark_number(card, 19)  # (2,2)
    mark_number(card, 20)  # (2,3)
    mark_number(card, 21)  # (2,4)
    assert check_win(card) == True  # Win in the middle row

def test_check_win_n_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 31)  # (0,2)
    mark_number(card, 32)  # (1,2)
    mark_number(card, 33)  # (2,2)
    mark_number(card, 34)  # (3,2)
    assert check_win(card) == True  # Win in the N column