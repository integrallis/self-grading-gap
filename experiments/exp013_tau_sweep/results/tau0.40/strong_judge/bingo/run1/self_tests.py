import pytest
from solution import announce_column, create_card, mark_number, check_win

def test_announce_column_valid_numbers():
    # Expected output for 1 is 'B', for 15 is 'B', for 16 is 'I', for 30 is 'I', 
    # for 31 is 'N', for 45 is 'N', for 46 is 'G', for 60 is 'G', 
    # for 61 is 'O', for 75 is 'O'
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

def test_announce_column_invalid_numbers():
    # Numbers outside 1-75 should raise a ValueError
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(0)
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(76)

def test_create_card_valid_numbers():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]  # 24 unique numbers
    card = create_card(numbers)
    # The card should be a 5x5 grid with the center space free (None)
    assert card[0][0] == 1
    assert card[0][1] == 16
    assert card[0][2] == 31
    assert card[0][3] == 46
    assert card[0][4] == 61
    assert card[1][0] == 2
    assert card[1][1] == 17
    assert card[1][2] == 32
    assert card[1][3] == 47
    assert card[1][4] == 62
    assert card[2][0] == 3
    assert card[2][1] == 18
    assert card[2][2] is None  # Center is free
    assert card[2][3] == 48
    assert card[2][4] == 63
    assert card[3][0] == 4
    assert card[3][1] == 19
    assert card[3][2] == 33
    assert card[3][3] == 49
    assert card[3][4] == 64
    assert card[4][0] == 5
    assert card[4][1] == 20
    assert card[4][2] == 34
    assert card[4][3] == 50
    assert card[4][4] == 65

def test_create_card_invalid_number_count():
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        create_card([1] * 25)  # 25 numbers
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        create_card([1] * 23)  # 23 numbers

def test_create_card_unique_numbers():
    with pytest.raises(ValueError, match="card numbers must be unique"):
        create_card([1, 2, 3, 4, 5, 1] + list(range(6, 24)))  # Duplicates present

def test_create_card_valid_ranges():
    with pytest.raises(ValueError, match="column B"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])  # 25 is invalid for B
    with pytest.raises(ValueError, match="column I"):
        create_card([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31, 32, 33, 34])  # 31 is invalid for I
    with pytest.raises(ValueError, match="column N"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 30, 31, 32, 33, 34])  # 30 is invalid for N
    with pytest.raises(ValueError, match="column G"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 61])  # 61 is invalid for G
    with pytest.raises(ValueError, match="column O"):
        create_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 76])  # 76 is invalid for O

def test_mark_number_hit():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert mark_number(card, 1) == True  # Marking 1 should hit
    assert mark_number(card, 16) == True  # Marking 16 should hit
    assert mark_number(card, 75) == False  # 75 is not on the card

def test_mark_number_invalid_call():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_number(card, 0)
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_number(card, 76)

def test_mark_number_miss():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert mark_number(card, 15) == False  # 15 is not on the card
    assert not check_win(card)  # Should still be no win

def test_check_win_no_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert check_win(card) == False  # No win yet

def test_check_win_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)
    mark_number(card, 2)
    mark_number(card, 3)
    mark_number(card, 4)
    mark_number(card, 5)
    assert check_win(card) == True  # First row is a win

def test_check_win_column_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 16)
    mark_number(card, 17)
    mark_number(card, 18)
    mark_number(card, 19)
    mark_number(card, 20)
    assert check_win(card) == True  # Second column is a win

def test_check_win_diagonal_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)  # Top left
    mark_number(card, 17)  # Second row, second column
    mark_number(card, 18)  # Third row, third column
    mark_number(card, 49)  # Fourth row, fourth column
    mark_number(card, 65)  # Bottom right
    assert check_win(card) == True  # Diagonal win

def test_check_win_middle_row_win():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 3)  # Number in middle row
    mark_number(card, 18)  # Number in middle row
    mark_number(card, 48)  # Number in middle row
    mark_number(card, 63)  # Number in middle row
    assert check_win(card) == False  # No win

def test_check_win_scattered_marks():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 1)
    mark_number(card, 17)
    mark_number(card, 33)
    mark_number(card, 50)
    assert check_win(card) == False  # No win from scattered marks

def test_check_win_diagonal_win_two():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    mark_number(card, 61)  # Bottom left
    mark_number(card, 47)  # Middle left
    mark_number(card, 18)  # Center
    mark_number(card, 19)  # Middle right
    mark_number(card, 5)  # Top right
    assert check_win(card) == True  # Second diagonal win

def test_new_card_initial_state():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    assert card[2][2] is None  # Center space is free
    for row in range(5):
        for col in range(5):
            if (row, col) != (2, 2):  # Skip center
                assert not mark_number(card, card[row][col])  # All other spaces are unmarked

def test_mark_number_does_not_change_state_on_miss():
    numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65]
    card = create_card(numbers)
    initial_state = [row[:] for row in card]  # Copy the initial state
    mark_number(card, 15)  # 15 is not on the card
    assert card == initial_state  # Card state should not change