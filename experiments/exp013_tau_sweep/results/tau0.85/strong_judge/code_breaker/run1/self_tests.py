# test_solution.py

from solution import score_guess

def test_score_guess_no_digits_shared():
    # secret 1234, guess 5678 gives ""
    assert score_guess("1234", "5678") == ""

def test_score_guess_one_digit_correct():
    # secret 1234, guess 1578 gives "+"
    assert score_guess("1234", "1578") == "+"

def test_score_guess_all_correct():
    # secret 1234, guess 1234 gives "++++"
    assert score_guess("1234", "1234") == "++++"

def test_score_guess_all_digits_different_positions():
    # secret 1234, guess 4321 gives "----"
    assert score_guess("1234", "4321") == "----"

def test_score_guess_correct_and_partial():
    # secret 1234, guess 1243 gives "++--"
    assert score_guess("1234", "1243") == "++--"

def test_score_guess_first_case_partial():
    # secret 1124, guess 5167 earns just "+" because of exact matches
    assert score_guess("1124", "5167") == "+"

def test_score_guess_second_case_partial():
    # secret 1111, guess 1112 earns "+++" because of exact matches
    assert score_guess("1111", "1112") == "+++"

def test_score_guess_duplicate_digit_partial():
    # secret 1234, guess 5115 gives "-"
    assert score_guess("1234", "5115") == "-"

def test_score_guess_duplicate_digit_full():
    # secret 1122, guess 2211 gives "----"
    assert score_guess("1122", "2211") == "----"

def test_score_guess_two_successive_guesses():
    # secret 1234, guess 1234 gives "++++", then guess 1243 gives "++--"
    assert score_guess("1234", "1234") == "++++"
    assert score_guess("1234", "1243") == "++--"

def test_score_guess_length_mismatch():
    # guess whose length differs from the secret's returns an error message
    try:
        score_guess("1234", "123")
    except Exception as e:
        assert str(e) == "guess must be the same length as the secret"

def test_score_guess_invalid_characters():
    # secret 1234, guess 1789 gives "+"
    assert score_guess("1234", "1789") == "+"

def test_score_guess_five_digit_secret():
    # secret 12345, guess 12345 gives "+++++"
    assert score_guess("12345", "12345") == "+++++"

def test_score_guess_five_digit_all_partial():
    # secret 12345, guess 23451 gives "-----"
    assert score_guess("12345", "23451") == "-----"

def test_score_guess_six_digit_secret():
    # secret 123456, guess 123456 gives "++++++"
    assert score_guess("123456", "123456") == "++++++"

def test_score_guess_six_digit_all_partial():
    # secret 123456, guess 234561 gives "------"
    assert score_guess("123456", "234561") == "------"

def test_score_guess_five_digit_custom_alphabet():
    # secret 1278, guess 1287 gives "++--" with custom alphabet
    assert score_guess("1278", "1287", alphabet="12345678") == "++--"

def test_score_guess_secret_too_short():
    # secret "123" gives rejection message
    try:
        score_guess("123")
    except Exception as e:
        assert str(e) == "code must be 4 to 6 characters long"

def test_score_guess_secret_too_long():
    # secret "1234567" gives rejection message
    try:
        score_guess("1234567")
    except Exception as e:
        assert str(e) == "code must be 4 to 6 characters long"

def test_score_guess_secret_invalid_characters():
    # secret "123A" gives rejection message
    try:
        score_guess("123A")
    except Exception as e:
        assert str(e) == "code may only contain characters from '123456'"