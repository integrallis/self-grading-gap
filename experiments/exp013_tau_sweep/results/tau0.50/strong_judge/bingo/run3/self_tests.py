import pytest
from solution import announce_column, lay_out_card, validate_card, mark_called_number, detect_winning_card

def test_announce_column_valid_numbers():
    assert announce_column(1) == 'B'  # 1-15 maps to B
    assert announce_column(15) == 'B'  # 1-15 maps to B
    assert announce_column(16) == 'I'  # 16-30 maps to I
    assert announce_column(30) == 'I'  # 16-30 maps to I
    assert announce_column(31) == 'N'  # 31-45 maps to N
    assert announce_column(45) == 'N'  # 31-45 maps to N
    assert announce_column(46) == 'G'  # 46-60 maps to G
    assert announce_column(60) == 'G'  # 46-60 maps to G
    assert announce_column(61) == 'O'  # 61-75 maps to O
    assert announce_column(75) == 'O'  # 61-75 maps to O

def test_announce_column_invalid_numbers():
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(0)  # Below the valid range
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        announce_column(76)  # Above the valid range

def test_lay_out_card():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    assert card[0][0] == 1   # B1
    assert card[1][0] == 2   # B2
    assert card[2][0] == 3   # B3
    assert card[3][0] == 4   # B4
    assert card[4][0] == 5   # B5
    assert card[0][1] == 16  # I1
    assert card[1][1] == 17  # I2
    assert card[2][1] == 18  # I3
    assert card[3][1] == 19  # I4
    assert card[4][1] == 20  # I5
    assert card[0][2] == 31  # N1
    assert card[1][2] == 32  # N2
    assert card[2][2] is None # Center space is free
    assert card[3][2] == 33  # N4
    assert card[4][2] == 34  # N5
    assert card[0][3] == 35  # G1
    assert card[1][3] == 46  # G2
    assert card[2][3] == 47  # G3
    assert card[3][3] == 48  # G4
    assert card[4][3] == 49  # G5
    assert card[0][4] == 50  # O1
    assert card[1][4] == 61  # O2
    assert card[2][4] == 62  # O3
    assert card[3][4] == 63  # O4
    assert card[4][4] == 64  # O5
    assert all(cell is not None for row in card for cell in row if not (row.index(cell) == 2 and card.index(row) == 2))  # Other spaces are filled

def test_validate_card_valid():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    validate_card(card_numbers)  # Should not raise any error

def test_validate_card_invalid_number_count():
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        validate_card([1] * 25)  # Too many numbers
    with pytest.raises(ValueError, match="exactly 24 numbers are required"):
        validate_card([1] * 23)  # Too few numbers

def test_validate_card_unique_numbers():
    with pytest.raises(ValueError, match="card numbers must be unique"):
        validate_card([1, 2, 3, 4, 5, 1] + [6] * 18)  # Duplicate number

def test_validate_card_column_range():
    with pytest.raises(ValueError, match="B"):
        validate_card([16] + [1, 2, 3, 4] + [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34])  # Invalid B
    with pytest.raises(ValueError, match="I"):
        validate_card([1, 2, 3, 4, 5, 31] + [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34])  # Invalid I
    with pytest.raises(ValueError, match="N"):
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 46] + [31, 32, 33, 34, 35, 36, 37, 38, 39, 40])  # Invalid N
    with pytest.raises(ValueError, match="G"):
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 61] + [46, 47, 48, 49, 50])  # Invalid G
    with pytest.raises(ValueError, match="O"):
        validate_card([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 76, 61, 62, 63])  # Invalid O

def test_mark_called_number_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    assert mark_called_number(card, 1) == True  # 1 is on the card
    assert all(cell is not None for row in card for cell in row if cell != 1)  # 1 should be marked

def test_mark_called_number_no_hit():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    assert mark_called_number(card, 10) == False  # 10 is not on the card
    assert all(cell is not None for row in card for cell in row)  # No changes to the card

def test_mark_called_number_invalid():
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_called_number([], 0)  # Below the valid range
    with pytest.raises(ValueError, match="number must be between 1 and 75"):
        mark_called_number([], 76)  # Above the valid range

def test_detect_winning_card_no_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    assert detect_winning_card(card) == False  # No win yet

def test_detect_winning_card_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [1, 2, 3, 4, 5]:  # Marks the top row
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # Row win

def test_detect_winning_card_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [16, 17, 18, 19, 20]:  # Marks the I column
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # Column win

def test_detect_winning_card_middle_row_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [18, 32, 47, 63]:  # Marking the middle row
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # Middle row win

def test_detect_winning_card_n_column_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [31, 32, 33, 34]:  # Marking the N column
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # N column win

def test_detect_winning_card_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [1, 17, 33, 49]:  # Marks the main diagonal
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # Diagonal win

def test_detect_winning_card_other_diagonal_win():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [5, 19, 33, 46]:  # Marks the other diagonal
        mark_called_number(card, number)
    assert detect_winning_card(card) == True  # Other diagonal win

def test_detect_winning_card_incomplete_marks():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [1, 2, 3]:  # Only part of a row
        mark_called_number(card, number)
    assert detect_winning_card(card) == False  # No win

def test_detect_winning_card_scattered_marks():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    for number in [1, 16, 33]:  # Scattered marks
        mark_called_number(card, number)
    assert detect_winning_card(card) == False  # No win

def test_mark_called_number_boundary_calls():
    card_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 33, 34, 46, 47, 48, 49, 50, 61, 62, 63, 64]  # 24 unique numbers
    card = lay_out_card(card_numbers)
    assert mark_called_number(card, 1) == True  # 1 is on the card
    assert mark_called_number(card, 75) == False  # 75 is not on the card, but is valid