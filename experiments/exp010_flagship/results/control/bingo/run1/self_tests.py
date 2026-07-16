import pytest
from solution import announce_column, lay_out_card, validate_card, mark_called_number, detect_win

def test_announce_column_valid_numbers():
    assert announce_column(1) == "B"  # 1-15 maps to B
    assert announce_column(15) == "B"  # 1-15 maps to B
    assert announce_column(16) == "I"  # 16-30 maps to I
    assert announce_column(30) == "I"  # 16-30 maps to I
    assert announce_column(31) == "N"  # 31-45 maps to N
    assert announce_column(45) == "N"  # 31-45 maps to N
    assert announce_column(46) == "G"  # 46-60 maps to G
    assert announce_column(60) == "G"  # 46-60 maps to G
    assert announce_column(61) == "O"  # 61-75 maps to O
    assert announce_column(75) == "O"  # 61-75 maps to O

def test_announce_column_invalid_numbers():
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(0)  # Below valid range
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(76)  # Above valid range

def test_lay_out_card_correct_layout():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]
    card = lay_out_card(numbers)
    assert card[0] == [1, 16, 31, 46, 61]  # B column
    assert card[1] == [2, 17, 32, 47, 62]  # I column
    assert card[2] == [3, 18, None, 48, 63]  # N column with free space
    assert card[3] == [4, 19, 34, 49, 64]  # G column
    assert card[4] == [5, 20, 35, 50, 75]  # O column

def test_lay_out_card_invalid_number_count():
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        lay_out_card([1] * 24)  # 24 numbers, but not unique

def test_validate_card_unique_numbers():
    with pytest.raises(ValueError, match="card numbers must be unique"):
        validate_card([1, 2, 3, 4, 5] + [1] + list(range(6, 25)))  # Duplicates present

def test_validate_card_column_ranges():
    with pytest.raises(ValueError, match="B column has an invalid number 16"):
        validate_card([16] + list(range(2, 25)))  # Invalid for column B

def test_mark_called_number_hit():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    marked, hit = mark_called_number(card, 1)  # 1 is on the card
    assert marked[0][0] == "X"  # First position marked
    assert hit is True  # It was a hit

def test_mark_called_number_no_hit():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    marked, hit = mark_called_number(card, 15)  # 15 is not on the card
    assert hit is False  # It was not a hit

def test_mark_called_number_invalid_number():
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_called_number([], 0)  # Invalid number

def test_detect_win_no_win():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    assert detect_win(card) is False  # No win yet

def test_detect_win_row_win():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    card[0] = ["X", "X", "X", "X", "X"]  # Marked first row
    assert detect_win(card) is True  # This should be a win

def test_detect_win_column_win():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    card[0][0] = "X"  # Marked B column
    card[1][0] = "X"
    card[3][0] = "X"
    card[4][0] = "X"
    assert detect_win(card) is True  # This should be a win

def test_detect_win_diagonal_win():
    card = lay_out_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    card[0][0] = "X"  # Marked diagonal
    card[1][1] = "X"
    card[2][2] = "X"  # Free space counts as marked
    card[3][3] = "X"
    card[4][4] = "X"
    assert detect_win(card) is True  # This should be a win