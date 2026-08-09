# test_feedback_scorer.py

from solution import score_guess

def test_no_shared_digits():
    # secret 1234, guess 5678 gives ""
    assert score_guess("1234", "5678") == ""

def test_exact_matches():
    # secret 1234, guess 1578 gives "+"
    assert score_guess("1234", "1578") == "+"
    # secret 1234, guess 1234 gives "++++"
    assert score_guess("1234", "1234") == "++++"

def test_partial_matches():
    # secret 1234, guess 4321 gives "----"
    assert score_guess("1234", "4321") == "----"

def test_mixed_positions():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"
    # secret 1234, guess 2134 gives "++--"
    assert score_guess("1234", "2134") == "++--"

def test_exact_before_partial():
    # secret 1124, guess 5167 earns just "+"
    assert score_guess("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++"
    assert score_guess("1111", "1112") == "+++"

def test_duplicate_handling():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

def test_exact_consumption():
    # secret 1124, guess 1111 earns "++"
    assert score_guess("1124", "1111") == "++"

def test_five_digit_all_partial():
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"

def test_reusable_scorer():
    # The same scorer answers successive guesses independently
    assert score_guess("1234", "5678") == ""
    assert score_guess("1234", "1234") == "++++"

def test_secret_validation_short_length():
    # A secret shorter than 4 is rejected
    with pytest.raises(ValueError) as excinfo:
        score_guess("123")
    assert str(excinfo.value) == "code must be 4 to 6 characters long"

def test_secret_validation_long_length():
    # A secret longer than 6 is rejected
    with pytest.raises(ValueError) as excinfo:
        score_guess("1234567")
    assert str(excinfo.value) == "code must be 4 to 6 characters long"

def test_secret_validation_invalid_characters():
    # A secret containing characters outside the digit alphabet is rejected
    with pytest.raises(ValueError) as excinfo:
        score_guess("123a")
    assert str(excinfo.value) == "code may only contain characters from '123456'"

def test_guess_validation_length():
    # A guess whose length differs from the secret's is rejected
    with pytest.raises(ValueError) as excinfo:
        score_guess("1234", "12345")
    assert str(excinfo.value) == "guess must be the same length as the secret"

def test_guess_validation_invalid_characters():
    # Guess digits outside the alphabet are legal but can never match anything
    assert score_guess("1234", "1789") == "+"

def test_longer_secret_support():
    # Secrets of 5 digits
    assert score_guess("12345", "54321") == "+----"  # Central 3 is an exact match
    assert score_guess("12345", "12345") == "+++++"
    # Secrets of 6 digits
    assert score_guess("123456", "123456") == "++++++"
    assert score_guess("123456", "654321") == "------"

def test_custom_alphabet_support():
    # With an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--"
    assert score_guess("1278", "1287", custom_alphabet="12345678") == "++--"