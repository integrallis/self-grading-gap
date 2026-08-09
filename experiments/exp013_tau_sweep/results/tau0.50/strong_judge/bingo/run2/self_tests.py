# test_bingo.py

import pytest
from solution import BingoCaller, BingoCard

def test_announce_column_letter_for_calls():
    caller = BingoCaller()
    assert caller.announce_column(1) == 'B'  # 1-15 maps to B
    assert caller.announce_column(15) == 'B'  # 1-15 maps to B
    assert caller.announce_column(16) == 'I'  # 16-30 maps to I
    assert caller.announce_column(30) == 'I'  # 16-30 maps to I
    assert caller.announce_column(31) == 'N'  # 31-45 maps to N
    assert caller.announce_column(45) == 'N'  # 31-45 maps to N
    assert caller.announce_column(46) == 'G'  # 46-60 maps to G
    assert caller.announce_column(60) == 'G'  # 46-60 maps to G
    assert caller.announce_column(61) == 'O'  # 61-75 maps to O
    assert caller.announce_column(75) == 'O'  # 61-75 maps to O
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        caller.announce_column(0)  # Reject number < 1
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        caller.announce_column(76)  # Reject number > 75

def test_bingo_card_layout():
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    assert card.get_number(0, 0) == 1  # B1
    assert card.get_number(1, 0) == 2  # B2
    assert card.get_number(2, 0) == 3  # B3
    assert card.get_number(3, 0) == 4  # B4
    assert card.get_number(4, 0) == 5  # B5
    assert card.get_number(0, 1) == 16  # I1
    assert card.get_number(1, 1) == 17  # I2
    assert card.get_number(2, 1) == 18  # I3
    assert card.get_number(3, 1) == 19  # I4
    assert card.get_number(4, 1) == 20  # I5
    assert card.get_number(0, 2) == 31  # N1
    assert card.get_number(1, 2) == 32  # N2
    assert card.get_number(2, 2) is None  # N3 is free space
    assert card.get_number(3, 2) == 34  # N4
    assert card.get_number(4, 2) == 35  # N5
    assert card.get_number(0, 3) == 46  # G1
    assert card.get_number(1, 3) == 47  # G2
    assert card.get_number(2, 3) == 48  # G3
    assert card.get_number(3, 3) == 49  # G4
    assert card.get_number(4, 3) == 50  # G5
    assert card.get_number(0, 4) == 61  # O1
    assert card.get_number(1, 4) == 62  # O2
    assert card.get_number(2, 4) == 63  # O3
    assert card.get_number(3, 4) == 64  # O4
    assert card.get_number(4, 4) == 65  # O5

def test_validate_bingo_card():
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        BingoCard([1] * 25)  # Too many numbers
    with pytest.raises(Exception, match="exactly 24 numbers are required"):
        BingoCard([1] * 23)  # Too few numbers
    with pytest.raises(Exception, match="card numbers must be unique"):
        BingoCard([1, 1, 3, 4, 5] + list(range(6, 24)))  # Duplicate number
    with pytest.raises(Exception, match="B"):
        BingoCard([31, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])  # Invalid B number
    with pytest.raises(Exception, match="I"):
        BingoCard([1, 2, 3, 4, 5, 31, 29, 28, 27, 26, 31, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])  # Invalid I number
    with pytest.raises(Exception, match="N"):
        BingoCard([1, 2, 3, 4, 5, 30, 16, 32, 33, 34, 46, 32, 33, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])  # Invalid N number
    with pytest.raises(Exception, match="G"):
        BingoCard([1, 2, 3, 4, 5, 30, 16, 32, 33, 34, 60, 47, 48, 49, 50, 32, 33, 34, 35, 46, 61, 62, 63, 64])  # Invalid G number
    with pytest.raises(Exception, match="O"):
        BingoCard([1, 2, 3, 4, 5, 30, 16, 32, 33, 34, 60, 47, 48, 49, 50, 46, 47, 48, 49, 50, 60, 62, 63, 80])  # Invalid O number

def test_mark_called_numbers():
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    assert card.mark_number(1) == True  # Number 1 is on the card, should mark it
    assert card.mark_number(10) == False  # Number 10 is not on the card, should not mark anything
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        card.mark_number(0)  # Invalid number < 1
    with pytest.raises(Exception, match="number must be between 1 and 75"):
        card.mark_number(76)  # Invalid number > 75

def test_detect_winning_card():
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    assert not card.check_win()  # No win yet
    for number in [1, 2, 3, 4, 5]:
        card.mark_number(number)
    assert card.check_win()  # Column win
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    for number in [16, 17, 18, 19, 20]:
        card.mark_number(number)
    assert card.check_win()  # Column win
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    for number in [31, 32, 34, 35]:
        card.mark_number(number)
    card.mark_number(33)  # Mark the free space
    assert card.check_win()  # Win now due to marked N column
    # Test for diagonal win
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    for number in [1, 17, 33, 49, 65]:
        card.mark_number(number)
    assert card.check_win()  # Diagonal win
    # Test for row win
    card = BingoCard([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 31, 32, 34, 35, 46, 47, 48, 49, 50, 61, 62, 63, 64])
    for number in [3, 18, 48, 63]:
        card.mark_number(number)
    assert card.check_win()  # Row win