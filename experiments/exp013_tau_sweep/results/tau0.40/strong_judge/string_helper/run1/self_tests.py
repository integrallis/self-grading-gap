from solution import check_bookended_text

def test_empty_text():
    # An empty string is shorter than two characters, so it never matches
    assert check_bookended_text("") == False

def test_single_character_text():
    # A single character is shorter than two characters, so it never matches
    assert check_bookended_text("A") == False

def test_two_character_text():
    # A text of exactly two characters always matches
    assert check_bookended_text("AB") == True

def test_three_character_text_matching():
    # First two characters "AB" match last two characters "AB"
    assert check_bookended_text("ABA") == True

def test_three_character_text_not_matching():
    # First two characters "AB" do not match last two characters "BC"
    assert check_bookended_text("ABC") == False

def test_four_character_text_matching():
    # First two characters "AB" match last two characters "AB"
    assert check_bookended_text("ABCDAB") == True

def test_four_character_text_not_matching():
    # First two characters "AB" do not match last two characters "CD"
    assert check_bookended_text("ABCDCD") == False

def test_five_character_text_matching():
    # First two characters "AB" match last two characters "AB"
    assert check_bookended_text("ABCDEAB") == True

def test_five_character_text_not_matching():
    # First two characters "AB" do not match last two characters "CD"
    assert check_bookended_text("ABCDECD") == False

def test_longer_text_matching():
    # First two characters "AB" match last two characters "AB"
    assert check_bookended_text("ABCDABCDAB") == True

def test_longer_text_not_matching():
    # First two characters "AB" do not match last two characters "CD"
    assert check_bookended_text("ABCDABCDCD") == False