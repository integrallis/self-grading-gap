# test_feedback_scorer.py

from solution import score_guess, validate_secret, validate_guess

def test_score_guess_no_digits():
    # secret 1234, guess 5678 gives ""
    assert score_guess("1234", "5678") == ""

def test_score_guess_all_correct():
    # secret 1234, guess 1234 gives "++++"
    assert score_guess("1234", "1234") == "++++"

def test_score_guess_some_correct():
    # secret 1234, guess 1578 gives "+"
    assert score_guess("1234", "1578") == "+"

def test_score_guess_all_incorrect_positions():
    # secret 1234, guess 4321 gives "----"
    assert score_guess("1234", "4321") == "----"

def test_score_guess_some_correct_some_incorrect():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"

def test_score_guess_ordering_with_misplaced():
    # secret 1234, guess 2134 gives "++--"
    assert score_guess("1234", "2134") == "++--"

def test_score_guess_some_correct_inexact_matches():
    # secret 1124, guess 5167 earns just "+" because 1 is an exact match
    assert score_guess("1124", "5167") == "+"

def test_score_guess_partial_and_exact_matches():
    # secret 1111, guess 1112 earns "+++"
    assert score_guess("1111", "1112") == "+++"

def test_score_guess_with_duplicates():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"

def test_score_guess_with_duplicates_and_multiple():
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

def test_validate_secret_too_short():
    # secret shorter than 4 characters is rejected
    try:
        validate_secret("123")
    except ValueError as e:
        assert str(e) == "code must be 4 to 6 characters long"

def test_validate_secret_too_long():
    # secret longer than 6 characters is rejected
    try:
        validate_secret("1234567")
    except ValueError as e:
        assert str(e) == "code must be 4 to 6 characters long"

def test_validate_secret_invalid_characters():
    # secret containing characters outside the digit alphabet is rejected
    try:
        validate_secret("123A")
    except ValueError as e:
        assert str(e) == "code may only contain characters from '123456'"

def test_validate_guess_length_mismatch_short():
    # guess whose length differs from the secret's is rejected
    try:
        validate_guess("1234", "12")
    except ValueError as e:
        assert str(e) == "guess must be the same length as the secret"

def test_validate_guess_length_mismatch_long():
    # guess whose length differs from the secret's is rejected
    try:
        validate_guess("1234", "12345")
    except ValueError as e:
        assert str(e) == "guess must be the same length as the secret"

def test_validate_guess_invalid_characters():
    # guess digits outside the alphabet are legal but can never match anything
    assert score_guess("1234", "1789") == "+"

def test_score_guess_with_longer_secret():
    # secret 12345, guess 12345 gives "+++++"
    assert score_guess("12345", "12345") == "+++++"

def test_score_guess_with_six_digit_secret():
    # secret 123456, guess 123456 gives "++++++"
    assert score_guess("123456", "123456") == "++++++"

def test_score_guess_all_partial_five_digit():
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"

def test_score_guess_all_partial_six_digit():
    # secret 123456, guess 234561 gives "------"
    assert score_guess("123456", "234561") == "------"

def test_score_guess_with_custom_alphabet():
    # using custom alphabet with secret 1278, guess 1287 gives "++--"
    assert score_guess("1278", "1287", alphabet="12345678") == "++--"

def test_reusable_scorer():
    # same scorer answers successive guesses independently
    assert score_guess("1234", "1234") == "++++"
    assert score_guess("1234", "1234") == "++++"