# test_bingo.py

import pytest
from solution import announce_column, create_card, mark_number, check_win

# US-1: Announce the column letter for a call
def test_announce_column_valid_B():
    assert announce_column(1) == 'B'  # 1-15 -> B

def test_announce_column_valid_B_upper():
    assert announce_column(15) == 'B'  # 1-15 -> B

def test_announce_column_valid_I():
    assert announce_column(16) == 'I'  # 16-30 -> I

def test_announce_column_valid_I_upper():
    assert announce_column(30) == 'I'  # 16-30 -> I

def test_announce_column_valid_N():
    assert announce_column(31) == 'N'  # 31-45 -> N

def test_announce_column_valid_N_upper():
    assert announce_column(45) == 'N'  # 31-45 -> N

def test_announce_column_valid_G():
    assert announce_column(46) == 'G'  # 46-60 -> G

def test_announce_column_valid_G_upper():
    assert announce_column(60) == 'G'  # 46-60 -> G

def test_announce_column_valid_O():
    assert announce_column(61) == 'O'  # 61-75 -> O

def test_announce_column_valid_O_upper():
    assert announce_column(75) == 'O'  # 61-75 -> O

def test_announce_column_invalid_below():
    with pytest.raises(ValueError):
        announce_column(0)  # Number must be between 1 and 75

def test_announce_column_invalid_above():
    with pytest.raises(ValueError):
        announce_column(76)  # Number must be between 1 and 75

# US-2: Lay out a card
def test_create_card_valid():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert card[0][0] == 1  # B[0]
    assert card[1][0] == 2  # B[1]
    assert card[2][0] == 3  # B[2]
    assert card[3][0] == 4  # B[3]
    assert card[4][0] == 5  # B[4]
    assert card[0][1] == 16  # I[0]
    assert card[1][1] == 17  # I[1]
    assert card[2][1] == 18  # I[2]
    assert card[3][1] == 19  # I[3]
    assert card[4][1] == 20  # I[4]
    assert card[0][2] == 31  # N[0]
    assert card[1][2] == 32  # N[1]
    assert card[2][2] is None  # Free space
    assert card[3][2] == 33  # N[3]
    assert card[4][2] == 34  # N[4]
    assert card[0][3] == 46  # G[0]
    assert card[1][3] == 47  # G[1]
    assert card[2][3] == 48  # G[2]
    assert card[3][3] == 49  # G[3]
    assert card[4][3] == 50  # G[4]
    assert card[0][4] == 61  # O[0]
    assert card[1][4] == 62  # O[1]
    assert card[2][4] == 63  # O[2]
    assert card[3][4] == 64  # O[3]
    assert card[4][4] == 65  # O[4]

def test_create_card_invalid_count_few():
    with pytest.raises(ValueError):
        create_card([1] * 23)  # 23 numbers

def test_create_card_invalid_count_many():
    with pytest.raises(ValueError):
        create_card([1] * 25)  # 25 numbers

def test_create_card_invalid_unique():
    with pytest.raises(ValueError, match="card numbers must be unique"):
        create_card([1, 1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63])  # Duplicates

def test_create_card_invalid_range():
    with pytest.raises(ValueError) as excinfo:
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 76, 62, 63, 64])  # 76 is invalid
    assert "number 76 is not valid for column O" in str(excinfo.value)

# US-3: Invalid column tests
def test_create_card_invalid_B():
    with pytest.raises(ValueError) as excinfo:
        create_card([30, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 30 in column B
    assert "number 30 is not valid for column B" in str(excinfo.value)

def test_create_card_invalid_I():
    with pytest.raises(ValueError) as excinfo:
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 15, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 15 in column I
    assert "number 15 is not valid for column I" in str(excinfo.value)

def test_create_card_invalid_N():
    with pytest.raises(ValueError) as excinfo:
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 30, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 30 in column N
    assert "number 30 is not valid for column N" in str(excinfo.value)

def test_create_card_invalid_G():
    with pytest.raises(ValueError) as excinfo:
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 45, 47, 48, 49, 50, 61, 62, 63, 64, 65])  # 45 in column G
    assert "number 45 is not valid for column G" in str(excinfo.value)

def test_create_card_invalid_O():
    with pytest.raises(ValueError) as excinfo:
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 60, 62, 63, 64, 65])  # 60 in column O
    assert "number 60 is not valid for column O" in str(excinfo.value)

# US-4: Mark called numbers
def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert mark_number(card, 1) == True  # 1 is on the card, should mark and return hit

def test_mark_number_no_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert mark_number(card, 10) == False  # 10 is not on the card, should return no hit
    assert card[0][0] == 1  # Ensure card is unchanged
    assert card[1][0] == 2  # Ensure card is unchanged

def test_mark_number_invalid():
    with pytest.raises(ValueError):
        mark_number([], 76)  # Invalid call

def test_mark_number_valid_boundary():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert mark_number(card, 75) == False  # 75 is not on the card, should return no hit

# US-5: Detect a winning card
def test_check_win_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert check_win(card) == False  # No win on a fresh card

def test_check_win_row():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [1, 2, 3, 4, 5]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning row

def test_check_win_column():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [16, 17, 18, 19, 20]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning column

def test_check_win_middle_row():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [31, 32, 33, 34]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning middle row

def test_check_win_N_column():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [31, 32, 33, 34]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning N column

def test_check_win_diagonal():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [1, 17, 49, 65]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning diagonal

def test_check_win_other_diagonal():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    for number in [61, 47, 19, 5]:
        mark_number(card, number)
    assert check_win(card) == True  # Winning other diagonal

def test_check_win_incomplete_row():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)
    mark_number(card, 2)
    mark_number(card, 3)
    assert check_win(card) == False  # Incomplete row

def test_check_win_scattered_marks():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)
    mark_number(card, 16)
    mark_number(card, 32)
    assert check_win(card) == False  # Scattered marks, no win