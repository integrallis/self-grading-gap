# test_code_breaking_feedback_scorer.py

from solution import score_guess, validate_secret, validate_guess

# US-1: Score a guess against the secret

def test_score_empty_feedback_no_digits():
    assert score_guess("1234", "5678") == ""  # No digits in common

def test_score_plus_one_correct_position():
    assert score_guess("1234", "1578") == "+"  # 1 is correct and in the correct position

def test_score_plus_multiple_correct_positions():
    assert score_guess("1234", "1234") == "++++"  # All digits are correct

def test_score_minus_for_digits_in_wrong_position():
    assert score_guess("1234", "4321") == "----"  # All digits are correct but in wrong positions

def test_score_plus_before_minus():
    assert score_guess("1234", "1243") == "++--"  # 1 and 2 are correct, 3 and 4 are wrong positions

def test_score_exact_and_partial_matches():
    assert score_guess("1124", "5167") == "+"  # Only 1 is correct and in the right position
    assert score_guess("1111", "1112") == "+++"  # Three 1s are correct, one guess not used

def test_score_duplicates_consume_only_secret_copies():
    assert score_guess("1234", "5115") == "-"  # Only one 5 exists, guess has two
    assert score_guess("1122", "2211") == "----"  # All digits are correct

# US-2: Reusable scorer
def test_score_multiple_guesses_independently():
    assert score_guess("1234", "5678") == ""  # First guess
    assert score_guess("1234", "1243") == "++--"  # Second guess

# US-3: Secret validation
def test_validate_secret_too_short():
    assert validate_secret("123") == "code must be 4 to 6 characters long"  # Secret too short

def test_validate_secret_too_long():
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"  # Secret too long

def test_validate_secret_invalid_characters():
    assert validate_secret("123A") == "code may only contain characters from '123456'"  # Invalid character

# US-4: Guess validation and tolerance
def test_validate_guess_different_length():
    assert validate_guess("1234", "12345") == "guess must be the same length as the secret"  # Length mismatch

def test_validate_guess_invalid_characters():
    assert validate_guess("1234", "1789") == "+"  # Invalid characters in guess

# US-5: Longer codes and wider alphabets
def test_score_five_digit_secret():
    assert score_guess("12345", "12345") == "+++++"  # All digits correct

def test_score_six_digit_secret():
    assert score_guess("123456", "123456") == "++++++"  # All digits correct

def test_score_custom_alphabet():
    assert score_guess("1278", "1287") == "++--"  # Using custom alphabet