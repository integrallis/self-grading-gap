# test_bingo.py

import pytest
from solution import announce_column, create_card, mark_number, check_win

def test_announce_column_valid_b():
    assert announce_column(1) == 'B'  # 1-15 maps to B

def test_announce_column_valid_i():
    assert announce_column(16) == 'I'  # 16-30 maps to I

def test_announce_column_valid_n():
    assert announce_column(31) == 'N'  # 31-45 maps to N

def test_announce_column_valid_g():
    assert announce_column(46) == 'G'  # 46-60 maps to G

def test_announce_column_valid_o():
    assert announce_column(61) == 'O'  # 61-75 maps to O

def test_announce_column_invalid_low():
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(0)

def test_announce_column_invalid_high():
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        announce_column(76)

def test_announce_column_valid_b_upper():
    assert announce_column(15) == 'B'  # 15 maps to B

def test_announce_column_valid_i_upper():
    assert announce_column(30) == 'I'  # 30 maps to I

def test_announce_column_valid_n_upper():
    assert announce_column(45) == 'N'  # 45 maps to N

def test_announce_column_valid_g_upper():
    assert announce_column(60) == 'G'  # 60 maps to G

def test_announce_column_valid_o_upper():
    assert announce_column(75) == 'O'  # 75 maps to O

def test_create_card_valid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # 24 unique numbers
    card = create_card(card_numbers)
    expected_card = [
        [1, 16, 31, 46, 61],
        [2, 17, 32, 47, 62],
        [3, 18, None, 48, 63],  # None for the free space
        [4, 19, 33, 49, 64],
        [5, 20, 34, 50, 65],
    ]
    assert card == expected_card

def test_create_card_invalid_number_count():
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1] * 25)  # Too many numbers

def test_create_card_invalid_number_count_few():
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        create_card([1] * 23)  # Too few numbers

def test_create_card_invalid_unique_numbers():
    with pytest.raises(Exception, match="card numbers must be unique"):
        create_card([1, 2, 2, 3] + [4] * 20)  # Duplicate numbers

def test_create_card_invalid_number_in_column():
    with pytest.raises(Exception, match="B"):
        create_card([30, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 46, 50,
                      61, 62, 63, 64, 65, 66])  # 30 is invalid for B

def test_mark_number_valid_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    mark_number(card, 2)  # Mark the number 2
    assert card[1][0] is None  # 2 should be marked as None

def test_mark_number_no_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    initial_card_state = [row[:] for row in card]  # Copy for comparison
    mark_number(card, 6)  # 6 is not on the card
    assert card == initial_card_state  # Card state unchanged

def test_mark_number_invalid_low():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number(card, 0)

def test_mark_number_invalid_high():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        mark_number(card, 76)

def test_mark_number_boundary_low():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    mark_number(card, 1)  # Should mark 1

def test_mark_number_boundary_high():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    mark_number(card, 75)  # Should not mark anything, as 75 is not on the card

def test_check_win_no_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    assert check_win(card) == False  # No win yet

def test_check_win_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [1, 2, 3, 4, 5]:
        mark_number(card, number)
    assert check_win(card) == True  # First row is complete

def test_check_win_middle_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [3, 18, 48, 63]:
        mark_number(card, number)
    assert check_win(card) == True  # Middle row is complete

def test_check_win_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [31, 32, 33, 34]:
        mark_number(card, number)
    assert check_win(card) == True  # Column N is complete

def test_check_win_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [1, 17, 49, 65]:  # Marking one diagonal
        mark_number(card, number)
    assert check_win(card) == True  # One diagonal is complete

def test_check_win_other_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [61, 47, 19, 5]:  # Marking the other diagonal
        mark_number(card, number)
    assert check_win(card) == True  # Other diagonal is complete

def test_check_win_incomplete_row():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [1, 2, 3]:  # Marking only part of the row
        mark_number(card, number)
    assert check_win(card) == False  # Incomplete row, no win

def test_check_win_scattered_marks():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46,
                    47, 48, 49, 50, 61, 62, 63, 64, 65]  # Valid card
    card = create_card(card_numbers)
    for number in [1, 17, 34]:  # Marking scattered numbers
        mark_number(card, number)
    assert check_win(card) == False  # No complete line, no win