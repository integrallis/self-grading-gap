# test_solution.py

from solution import score_guess

def test_score_guess_no_common_digits():
    # secret 1234, guess 5678 gives ""
    assert score_guess("1234", "5678") == ""

def test_score_guess_exact_match():
    # secret 1234, guess 1578 gives "+"
    assert score_guess("1234", "1578") == "+"

def test_score_guess_fully_correct():
    # secret 1234, guess 1234 gives "++++"
    assert score_guess("1234", "1234") == "++++"

def test_score_guess_partial_match():
    # secret 1234, guess 4321 gives "----"
    assert score_guess("1234", "4321") == "----"

def test_score_guess_with_mixed_positions():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"
    # secret 1234, guess 2134 also gives "++--"
    assert score_guess("1234", "2134") == "++--"

def test_score_guess_exact_matches_consumed():
    # secret 1124, guess 5167 earns just "+" 
    assert score_guess("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++"
    assert score_guess("1111", "1112") == "+++"

def test_score_guess_with_duplicates():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

def test_score_guess_with_longer_secret():
    # secret 12345, guess 12345 gives "+++++"
    assert score_guess("12345", "12345") == "+++++"
    # secret 12345, guess 54321 gives "+----"
    assert score_guess("12345", "54321") == "+----"
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"

def test_score_guess_with_six_digit_exact():
    # secret 123456, guess 123456 gives "++++++"
    assert score_guess("123456", "123456") == "++++++"

def test_score_guess_with_six_digit_partial():
    # secret 123456, guess 654321 gives "------"
    assert score_guess("123456", "654321") == "------"

def test_score_guess_length_mismatch():
    # guess length differs from the secret's
    result = score_guess("1234", "12345")
    assert result == "guess must be the same length as the secret"

def test_score_guess_with_invalid_characters():
    # secret 1234, guess 1789 gives "+"
    assert score_guess("1234", "1789") == "+"

def test_secret_too_short():
    # secret "123" is too short
    result = score_guess("123", "1234")
    assert result == "code must be 4 to 6 characters long"

def test_secret_too_long():
    # secret "1234567" is too long
    result = score_guess("1234567", "123456")
    assert result == "code must be 4 to 6 characters long"

def test_secret_with_invalid_characters():
    # secret "1237" contains invalid character
    result = score_guess("1237", "1234")
    assert result == "code may only contain characters from '123456'"

def test_custom_alphabet():
    # secret "1278" with custom alphabet, guess "1287" gives "++--"
    result = score_guess("1278", "1287", alphabet="12345678")
    assert result == "++--"