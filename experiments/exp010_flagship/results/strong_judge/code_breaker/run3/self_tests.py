# test_solution.py
import pytest
from solution import score_guess, validate_secret, validate_guess

# Tests for scoring guesses against the secret

def test_no_matching_digits():
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

def test_mixed_feedback():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"
    # secret 1234, guess 2134 gives "++--"
    assert score_guess("1234", "2134") == "++--"

def test_consume_exact_matches_first():
    # secret 1124, guess 5167 earns just "+"
    assert score_guess("1124", "5167") == "+"
    # secret 1111, guess 1112 earns "+++"
    assert score_guess("1111", "1112") == "+++"

def test_duplicate_digit_scoring():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

# Tests for reusable scorer

def test_reusable_scorer():
    # The same scorer answers successive guesses independently
    secret = "1234"
    assert score_guess(secret, "5678") == ""
    assert score_guess(secret, "1234") == "++++"

# Tests for secret validation

def test_invalid_secret_length():
    # secret shorter than 4 or longer than 6 characters is rejected
    assert validate_secret("123") == "code must be 4 to 6 characters long"
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"

def test_invalid_secret_characters():
    # secret containing characters outside the digit alphabet is rejected
    assert validate_secret("1237") == "code may only contain characters from '123456'"

# Tests for guess validation and tolerance

def test_invalid_guess_length():
    # guess whose length differs from the secret's is rejected
    assert validate_guess("1234", "123") == "guess must be the same length as the secret"
    # guess whose length is longer than the secret's is rejected
    assert validate_guess("1234", "12345") == "guess must be the same length as the secret"

def test_guess_invalid_characters():
    # Guess digits outside the alphabet are legal but can never match anything
    assert score_guess("1234", "1789") == "+"

# Tests for longer codes and wider alphabets

def test_five_digit_secret():
    # secret 12345 scores guess 12345 as "+++++"
    assert score_guess("12345", "12345") == "+++++"
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"

def test_six_digit_secret():
    # secret 123456 scores guess 123456 as "++++++"
    assert score_guess("123456", "123456") == "++++++"
    # secret 123456, guess 234561 gives "------"
    assert score_guess("123456", "234561") == "------"

def test_custom_alphabet():
    # with an alphabet of 1 through 8, secret 1278 scores guess 1287 as "++--"
    assert score_guess("1278", "1287") == "++--"