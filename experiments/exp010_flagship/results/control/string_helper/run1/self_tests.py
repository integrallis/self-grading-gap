# test_matching_pairs.py

from solution import check_bookended_text

def test_empty_text():
    # An empty string has no characters, so it cannot match.
    assert check_bookended_text("") == False

def test_single_character_text():
    # A single character cannot form a two-character sequence, so it cannot match.
    assert check_bookended_text("A") == False

def test_two_character_exact_match():
    # A two-character string consists of the same opening and closing pair.
    assert check_bookended_text("AB") == True

def test_two_character_different_characters():
    # A two-character string with different characters does not match.
    assert check_bookended_text("AC") == False

def test_three_character_match():
    # The first two characters 'AB' and the last two characters 'AB' match.
    assert check_bookended_text("ABA") == True

def test_three_character_no_match():
    # The first two characters 'AB' and the last two characters 'AC' do not match.
    assert check_bookended_text("ABC") == False

def test_four_character_match():
    # The first two characters 'AB' and the last two characters 'AB' match.
    assert check_bookended_text("ABCDAB") == True

def test_four_character_no_match():
    # The first two characters 'AB' and the last two characters 'CD' do not match.
    assert check_bookended_text("ABCD") == False

def test_longer_text_match():
    # The first two characters 'AB' and the last two characters 'AB' match.
    assert check_bookended_text("ABXYZAB") == True

def test_longer_text_no_match():
    # The first two characters 'AB' and the last two characters 'CD' do not match.
    assert check_bookended_text("ABXYZCD") == False

def test_longer_text_with_same_start_end_characters():
    # The first two characters 'XY' and the last two characters 'XY' match.
    assert check_bookended_text("XYThis is a testXY") == True

def test_longer_text_with_same_start_different_end_characters():
    # The first two characters 'XY' and the last two characters 'YZ' do not match.
    assert check_bookended_text("XYThis is a testYZ") == False