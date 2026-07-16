from solution import check_bookended_text

def test_empty_text():
    # An empty string has length 0, so it does not match.
    assert check_bookended_text("") == False

def test_single_character_text():
    # A single character has length 1, so it does not match.
    assert check_bookended_text("A") == False

def test_two_character_text():
    # Exactly two characters are the same, so it matches.
    assert check_bookended_text("AA") == True

def test_two_character_different_text():
    # Exactly two characters are different, so it does match.
    assert check_bookended_text("AB") == True  # "AB" matches itself

def test_three_character_matching_text():
    # The first two characters "AB" do not match the last two characters "BA".
    assert check_bookended_text("ABA") == False

def test_three_character_non_matching_text():
    # The first two characters "AB" do not match the last two "BC".
    assert check_bookended_text("ABC") == False

def test_four_character_matching_text():
    # The first two characters "AB" match the last two characters "AB".
    assert check_bookended_text("ABCDAB") == True

def test_four_character_non_matching_text():
    # The first two characters "AB" do not match the last two "CD".
    assert check_bookended_text("ABCD") == False

def test_longer_matching_text():
    # The first two characters "AB" match the last two characters "AB".
    assert check_bookended_text("ABXYZAB") == True

def test_longer_non_matching_text():
    # The first two characters "AB" do not match the last two "CD".
    assert check_bookended_text("ABXYZCD") == False

def test_equal_length_matching_text():
    # The first two characters "XY" match the last two characters "XY".
    assert check_bookended_text("XYXY") == True

def test_three_character_matching_example():
    # The first two characters "AA" match the last two characters "AA".
    assert check_bookended_text("AAA") == True