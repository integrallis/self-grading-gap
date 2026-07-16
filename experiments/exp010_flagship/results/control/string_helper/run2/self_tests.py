# test_matching_pairs.py

from solution import matching_pairs

def test_empty_text():
    # Empty text has length 0, so it should not match.
    assert matching_pairs("") == False

def test_single_character_text():
    # Single character text has length 1, so it should not match.
    assert matching_pairs("A") == False

def test_two_character_text_matches():
    # Text of exactly two characters matches only if both characters are the same.
    assert matching_pairs("AA") == True  # Both characters are the same.
    assert matching_pairs("AB") == False  # Characters are different.

def test_three_character_text_matches():
    # Text "AAA" has the same first two and last two characters: "AA" and "AA".
    assert matching_pairs("AAA") == True

def test_four_character_text_matches():
    # Text "ABAB" has the same first two and last two characters: "AB" and "AB".
    assert matching_pairs("ABAB") == True

def test_four_character_text_does_not_match():
    # Text "ABCD" does not match, as "AB" and "CD" are different.
    assert matching_pairs("ABCD") == False

def test_five_character_text_matches():
    # Text "ABCAB" has the same first two and last two characters: "AB" and "AB".
    assert matching_pairs("ABCAB") == True

def test_five_character_text_does_not_match():
    # Text "ABCDE" does not match, as "AB" and "DE" are different.
    assert matching_pairs("ABCDE") == False

def test_six_character_text_matches():
    # Text "AABBCC" has the same first two and last two characters: "AA" and "CC".
    assert matching_pairs("AABBCC") == False  # They are different.

def test_six_character_text_does_not_match():
    # Text "AABBAA" has the same first two and last two characters: "AA" and "AA".
    assert matching_pairs("AABBAA") == True