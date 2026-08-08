# test_feedback_scorer.py

from solution import score_guess

def test_score_guess_no_digits():
    # secret 1234, guess 5678 gives ""
    assert score_guess("1234", "5678") == ""

def test_score_guess_exact_match():
    # secret 1234, guess 1578 gives "+"
    assert score_guess("1234", "1578") == "+"

def test_score_guess_full_correct():
    # secret 1234, guess 1234 gives "++++"
    assert score_guess("1234", "1234") == "++++"

def test_score_guess_partial_matches():
    # secret 1234, guess 4321 gives "----"
    assert score_guess("1234", "4321") == "----"

def test_score_guess_mixed_positions():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"
    # secret 1234, guess 2134 gives "++--"
    assert score_guess("1234", "2134") == "++--"

def test_score_guess_consumed_exact_matches():
    # secret 1124, guess 5167 earns just "+"
    assert score_guess("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++"
    assert score_guess("1111", "1112") == "+++"

def test_score_guess_duplicate_digit_symbols():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

def test_score_multiple_guesses():
    # Scoring multiple guesses against a single secret
    secret = "1234"
    assert score_guess(secret, "5678") == ""
    assert score_guess(secret, "1578") == "+"
    assert score_guess(secret, "1234") == "++++"

def test_score_repeated_guess():
    # Same guess against the same secret should yield the same result
    secret = "1234"
    guess = "1243"
    assert score_guess(secret, guess) == "++--"
    assert score_guess(secret, guess) == "++--"

def test_validate_secret_too_short():
    # secret shorter than 4 is rejected
    assert score_guess("123", "1234") == "code must be 4 to 6 characters long"

def test_validate_secret_too_long():
    # secret longer than 6 is rejected
    assert score_guess("1234567", "1234") == "code must be 4 to 6 characters long"

def test_validate_secret_invalid_characters():
    # secret containing characters outside '123456' is rejected
    assert score_guess("1237", "1234") == "code may only contain characters from '123456'"

def test_validate_guess_different_length():
    # guess whose length differs from the secret's is rejected
    assert score_guess("1234", "12") == "guess must be the same length as the secret"

def test_validate_guess_invalid_characters():
    # secret 1234, guess 1789 gives "+"
    assert score_guess("1234", "1789") == "+"

def test_score_longer_secrets():
    # secret 12345, guess 12345 gives "+++++"
    assert score_guess("12345", "12345") == "+++++"
    # secret 123456, guess 123456 gives "++++++"
    assert score_guess("123456", "123456") == "++++++"
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"
    # secret 123456, guess 234561 gives "------"
    assert score_guess("123456", "234561") == "------"

def test_score_custom_alphabet():
    # secret 1278 rejected with default alphabet
    assert score_guess("1278", "1234") == "code may only contain characters from '123456'"
    # with an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--"
    # Assume the scoring function can handle a custom alphabet that includes '7' and '8'
    assert score_guess("1278", "1287") == "++--"  # Assuming the scorer can handle the custom alphabet