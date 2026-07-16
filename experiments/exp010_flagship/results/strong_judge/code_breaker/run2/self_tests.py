# test_feedback_scorer.py

from solution import score_feedback, validate_secret, validate_guess

# Test cases for scoring feedback of guesses against a secret
def test_score_feedback_no_shared_digits():
    # secret 1234, guess 5678 gives ""
    assert score_feedback("1234", "5678") == ""

def test_score_feedback_exact_match():
    # secret 1234, guess 1578 gives "+"
    assert score_feedback("1234", "1578") == "+"

def test_score_feedback_full_correct_guess():
    # secret 1234, guess 1234 gives "++++"
    assert score_feedback("1234", "1234") == "++++"

def test_score_feedback_partial_correct_guess():
    # secret 1234, guess 4321 gives "----"
    assert score_feedback("1234", "4321") == "----"

def test_score_feedback_mixed_correct_and_partial():
    # secret 1234, guess 1243 gives "++--"
    assert score_feedback("1234", "1243") == "++--"

def test_score_feedback_another_mixed_correct_and_partial():
    # secret 1234, guess 2134 gives "++--"
    assert score_feedback("1234", "2134") == "++--"

def test_score_feedback_with_exact_and_partial():
    # secret 1124, guess 5167 earns just "+"
    assert score_feedback("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++".
    assert score_feedback("1111", "1112") == "+++"

def test_score_feedback_with_duplicates():
    # secret 1234, guess 5115 gives "-"
    assert score_feedback("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_feedback("1122", "2211") == "----"

# Test cases for reusable scorer
def test_reusable_scorer():
    # The same scorer answers successive guesses independently
    secret = "1234"
    assert score_feedback(secret, "5678") == ""
    assert score_feedback(secret, "1243") == "++--"
    assert score_feedback(secret, "4321") == "----"
    assert score_feedback(secret, "5678") == ""  # Verify repeatability

# Test cases for secret validation
def test_validate_secret_length_too_short():
    # A secret shorter than 4 characters is rejected
    assert validate_secret("123") == "code must be 4 to 6 characters long"

def test_validate_secret_length_too_long():
    # A secret longer than 6 characters is rejected
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"

def test_validate_secret_invalid_characters():
    # A secret containing characters outside the digit alphabet is rejected
    assert validate_secret("123a") == "code may only contain characters from '123456'"
    assert validate_secret("1237") == "code may only contain characters from '123456'"

def test_validate_secret_length_boundary_valid():
    # Valid boundary lengths accepted
    assert validate_secret("1234") == ""
    assert validate_secret("123456") == ""
    assert validate_secret("12345") == ""  # Test valid secret of length 5

# Test cases for guess validation
def test_validate_guess_length_different_short():
    # A guess whose length differs from the secret's is rejected
    assert validate_guess("1234", "12") == "guess must be the same length as the secret"

def test_validate_guess_length_different_long():
    # A guess whose length differs from the secret's is rejected
    assert validate_guess("1234", "12345") == "guess must be the same length as the secret"

def test_validate_guess_invalid_characters():
    # Guess digits outside the alphabet are legal but can never match anything
    assert score_feedback("1234", "1789") == "+"

# Test cases for longer codes and wider alphabets
def test_score_feedback_five_digit_secret():
    # A secret of 5 digits, secret 12345, guess 12345 gives "+++++"
    assert score_feedback("12345", "12345") == "+++++"
    # secret 12345, guess 23451 gives "-----"
    assert score_feedback("12345", "23451") == "-----"

def test_score_feedback_six_digit_secret():
    # A secret of 6 digits, secret 123456, guess 123456 gives "++++++"
    assert score_feedback("123456", "123456") == "++++++"
    # secret 123456, guess 234561 gives "------"
    assert score_feedback("123456", "234561") == "------"

def test_score_feedback_custom_alphabet():
    # With an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--"
    assert score_feedback("1278", "1287", alphabet="12345678") == "++--"