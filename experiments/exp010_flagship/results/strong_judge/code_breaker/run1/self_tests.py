from solution import score_guess, validate_secret, validate_guess

# User Stories: US-1
def test_score_guess_no_digits_in_common():
    assert score_guess("1234", "5678") == ""  # No digits in common

def test_score_guess_exact_matches():
    assert score_guess("1234", "1578") == "+"  # 1 correct digit in correct position
    assert score_guess("1234", "1234") == "++++"  # All digits correct

def test_score_guess_partial_matches():
    assert score_guess("1234", "4321") == "----"  # All digits correct but in wrong positions

def test_score_guess_mixed_matches():
    assert score_guess("1234", "1243") == "++--"  # 2 correct digits in correct positions, 2 in wrong
    assert score_guess("1234", "2134") == "++--"  # Same as above, different order

def test_score_guess_consumed_matches():
    assert score_guess("1124", "5167") == "+"  # Only 1 matched digit
    assert score_guess("1111", "1112") == "+++"  # 3 matched digits, 1 partial

def test_score_guess_duplicates_handling():
    assert score_guess("1234", "5115") == "-"  # 1 digit matches, others do not
    assert score_guess("1122", "2211") == "----"  # All digits matched but in wrong positions

# User Stories: US-2
def test_reusable_scorer():
    assert score_guess("1234", "1234") == "++++"  # First guess
    assert score_guess("1234", "5678") == ""  # Second guess
    assert score_guess("1234", "1234") == "++++"  # Repeating first guess for deterministic behavior

# User Stories: US-3
def test_validate_secret_length():
    assert validate_secret("123") == "code must be 4 to 6 characters long"  # Too short
    assert validate_secret("1234567") == "code must be 4 to 6 characters long"  # Too long

def test_validate_secret_characters():
    assert validate_secret("123A") == "code may only contain characters from '123456'"  # Invalid character
    assert validate_secret("123456") == None  # Valid secret

# User Stories: US-4
def test_validate_guess_length():
    assert validate_guess("1234", "12345") == "guess must be the same length as the secret"  # Length mismatch
    assert validate_guess("1234", "123") == "guess must be the same length as the secret"  # Length mismatch (too short)

def test_score_guess_valid_guess_invalid_characters():
    assert score_guess("1234", "1789") == "+"  # Valid guess, but 7, 8, 9 cannot match anything

# User Stories: US-5
def test_score_guess_longer_codes():
    assert score_guess("12345", "12345") == "+++++"  # 5-digit match
    assert score_guess("123456", "123456") == "++++++"  # 6-digit match
    assert score_guess("12345", "23451") == "-----"  # All digits in wrong positions, 5-digit case
    assert score_guess("123456", "234561") == "------"  # All digits in wrong positions, 6-digit case

def test_score_guess_custom_alphabet():
    assert score_guess("1278", "1287", alphabet="12345678") == "++--"  # Custom alphabet 1-8