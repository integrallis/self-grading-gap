# test_feedback_scorer.py

from solution import score_feedback, validate_secret, validate_guess

# US-1: Score a guess against the secret
def test_guess_sharing_no_digits_with_secret():
    # secret 1234, guess 5678 gives ""
    assert score_feedback("1234", "5678") == ""

def test_guess_with_exact_matches():
    # secret 1234, guess 1578 gives "+"
    assert score_feedback("1234", "1578") == "+"
    # secret 1234, guess 1234 gives "++++"
    assert score_feedback("1234", "1234") == "++++"

def test_guess_with_partial_matches():
    # secret 1234, guess 4321 gives "----"
    assert score_feedback("1234", "4321") == "----"

def test_guess_with_pluses_before_minuses():
    # secret 1234, guess 1243 gives "++--"
    assert score_feedback("1234", "1243") == "++--"
    # secret 1234, guess 2134 gives "++--"
    assert score_feedback("1234", "2134") == "++--"

def test_exact_matches_consumed_before_partial():
    # secret 1124, guess 5167 earns just "+"
    assert score_feedback("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++"
    assert score_feedback("1111", "1112") == "+++"

def test_duplicated_digits_earn_only_as_many_symbols_as_secret():
    # secret 1234, guess 5115 gives "-"
    assert score_feedback("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_feedback("1122", "2211") == "----"

# US-2: Reusable scorer
def test_scores_successive_guesses_independently():
    # secret 1234, guess 1234 gives "++++"
    assert score_feedback("1234", "1234") == "++++"
    # secret 1234, guess 5678 gives ""
    assert score_feedback("1234", "5678") == ""

# US-3: Secret validation
def test_secret_too_short():
    # secret shorter than 4 characters
    assert validate_secret("123") == "code must be 4 to 6 characters long"

def test_secret_too_long():
    # secret longer than 6 characters
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"

def test_secret_with_invalid_characters():
    # secret containing characters outside the digit alphabet
    assert validate_secret("123A") == "code may only contain characters from '123456'"

# US-4: Guess validation and tolerance
def test_guess_length_mismatch():
    # guess whose length differs from the secret's
    assert validate_guess("1234", "123") == "guess must be the same length as the secret"
    assert validate_guess("1234", "12345") == "guess must be the same length as the secret"

def test_guess_with_invalid_characters_tolerated():
    # guess digits outside the alphabet are legal but can never match anything
    assert score_feedback("1234", "1789") == "+"

# US-5: Longer codes and wider alphabets
def test_five_digit_secret():
    # secret 12345, guess 12345 gives "+++++"
    assert score_feedback("12345", "12345") == "+++++"
    # secret 12345, guess 54321 gives "-----"
    assert score_feedback("12345", "54321") == "-----"

def test_six_digit_secret():
    # secret 123456, guess 123456 gives "++++++"
    assert score_feedback("123456", "123456") == "++++++"
    # secret 123456, guess 654321 gives "------"
    assert score_feedback("123456", "654321") == "------"

def test_custom_alphabet():
    # with an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--"
    assert score_feedback("1278", "1287") == "++--"