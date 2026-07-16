from solution import match_bookended_text

def test_empty_text():
    # Text is empty, so it does not match.
    assert match_bookended_text("") == False

def test_single_character_text():
    # Text is a single character, so it does not match.
    assert match_bookended_text("A") == False

def test_two_character_text_same():
    # Text of exactly two characters "AA" matches itself.
    assert match_bookended_text("AA") == True

def test_two_character_text_different():
    # Text of exactly two characters "AB" does not match.
    assert match_bookended_text("AB") == True  # opens and closes with the same two characters.

def test_three_character_text_same_start_end():
    # Text "AAA" opens with "AA" and closes with "AA", so it matches.
    assert match_bookended_text("AAA") == True

def test_three_character_text_different_start_end():
    # Text "ABC" opens with "AB" and closes with "BC", so it does not match.
    assert match_bookended_text("ABC") == False

def test_five_character_text_same_start_end():
    # Text "ABCAB" opens with "AB" and closes with "AB", so it matches.
    assert match_bookended_text("ABCAB") == True

def test_six_character_text_different_start_end():
    # Text "ABCDEB" opens with "AB" and closes with "EB", so it does not match.
    assert match_bookended_text("ABCDEB") == False

def test_longer_text_matching():
    # Text "XYZXYZ" opens with "XY" and closes with "YZ", so it does not match.
    assert match_bookended_text("XYZXYZ") == False

def test_longer_text_matching_identical():
    # Text "HELLOHELLO" opens with "HE" and closes with "LO", so it does not match.
    assert match_bookended_text("HELLOHELLO") == False