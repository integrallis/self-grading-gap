# test_matching_opening_closing_pairs.py

from solution import matches_opening_closing_pairs

def test_empty_text():
    # Empty text is shorter than 2 characters, should not match
    assert matches_opening_closing_pairs("") == False

def test_single_character_text():
    # Single character text is shorter than 2 characters, should not match
    assert matches_opening_closing_pairs("A") == False

def test_two_character_text():
    # Two character text always matches (e.g., "AA" -> "AA" == "AA")
    assert matches_opening_closing_pairs("AA") == True
    assert matches_opening_closing_pairs("AB") == True

def test_longer_text_matching():
    # Longer text matches if first two characters are the same as the last two characters
    assert matches_opening_closing_pairs("AAA") == True  # "AA" == "AA"
    assert matches_opening_closing_pairs("ABCAB") == True  # "AB" == "AB"
    assert matches_opening_closing_pairs("ABCDEBA") == False  # "AB" != "BA"

def test_longer_text_not_matching():
    # Longer text does not match if first two characters are different from the last two characters
    assert matches_opening_closing_pairs("ABC") == False  # "AB" != "C"
    assert matches_opening_closing_pairs("AABBC") == False  # "AA" != "BC"
    assert matches_opening_closing_pairs("AABB") == True  # "AA" == "AA"