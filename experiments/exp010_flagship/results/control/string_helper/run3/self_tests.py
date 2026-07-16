from solution import check_bookended

def test_empty_text():
    # Text is empty, so it never matches
    assert check_bookended("") == False

def test_single_character_text():
    # Text is a single character, so it never matches
    assert check_bookended("A") == False

def test_two_character_text_matches():
    # Text is exactly two characters and always matches
    assert check_bookended("AA") == True
    assert check_bookended("AB") == True

def test_long_text_matching_pairs():
    # Longer text matches when first two and last two characters are the same
    assert check_bookended("AAA") == True  # first: "AA", last: "AA"
    assert check_bookended("ABCAB") == True  # first: "AB", last: "AB"

def test_long_text_not_matching_pairs():
    # Longer text does not match when first two and last two characters are different
    assert check_bookended("ABC") == False  # first: "AB", last: "BC"
    assert check_bookended("ABCDEBA") == False  # first: "AB", last: "BA"