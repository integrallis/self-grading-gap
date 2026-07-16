# test_feedback_scorer.py

from solution import score_guess, validate_secret, validate_guess

# User Stories: Score a guess against the secret
def test_score_guess_no_matching_digits():
    assert score_guess("1234", "5678") == ""  # AC-1.1: no digits match

def test_score_guess_exact_matches():
    assert score_guess("1234", "1578") == "+"  # AC-1.2: one exact match
    assert score_guess("1234", "1234") == "++++"  # fully correct guess

def test_score_guess_partial_matches():
    assert score_guess("1234", "4321") == "----"  # AC-1.3: all digits match but in wrong positions

def test_score_guess_mixed_matches():
    assert score_guess("1234", "1243") == "++--"  # AC-1.4: two exact, two partial
    assert score_guess("1234", "2134") == "++--"  # AC-1.4: two exact, two partial

def test_score_guess_consumed_matches():
    assert score_guess("1124", "5167") == "+"  # AC-1.5: one exact consumed
    assert score_guess("1111", "1112") == "+++"  # AC-1.5: three exact matches

def test_score_guess_duplicate_digit_handling():
    assert score_guess("1234", "5115") == "-"  # AC-1.6: one partial match, but no exact
    assert score_guess("1122", "2211") == "----"  # AC-1.6: all matches accounted

# User Stories: Reusable scorer
def test_score_guess_reusable_scorer():
    assert score_guess("1234", "1234") == "++++"  # AC-2.1: first guess
    assert score_guess("1234", "1243") == "++--"  # AC-2.1: second guess

# User Stories: Secret validation
def test_validate_secret_length():
    assert validate_secret("123") == "code must be 4 to 6 characters long"  # AC-3.1: too short
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"  # AC-3.1: too long

def test_validate_secret_characters():
    assert validate_secret("123a") == "code may only contain characters from '123456'"  # AC-3.2: invalid character
    assert validate_secret("123456") == None  # valid secret

# User Stories: Guess validation and tolerance
def test_validate_guess_length():
    assert validate_guess("1234", "12") == "guess must be the same length as the secret"  # AC-4.1: different lengths

def test_validate_guess_characters():
    assert validate_guess("1234", "1789") == None  # AC-4.2: valid guess with tolerated characters

# User Stories: Longer codes and wider alphabets
def test_score_guess_longer_codes():
    assert score_guess("12345", "12345") == "+++++"  # AC-5.1: fully correct 5-digit guess
    assert score_guess("123456", "123456") == "++++++"  # fully correct 6-digit guess

def test_score_guess_custom_alphabet():
    assert score_guess("1278", "1287") == "++--"  # AC-5.2: custom alphabet scoring