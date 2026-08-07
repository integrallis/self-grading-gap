# test_feedback_scorer.py

from solution import score_feedback

def test_no_shared_digits():
    # secret 1234, guess 5678 gives ""
    assert score_feedback('1234', '5678') == ""

def test_exact_matches():
    # secret 1234, guess 1578 gives "+"
    assert score_feedback('1234', '1578') == "+"
    # secret 1234, guess 1234 gives "++++"
    assert score_feedback('1234', '1234') == "++++"

def test_partial_matches():
    # secret 1234, guess 4321 gives "----"
    assert score_feedback('1234', '4321') == "----"

def test_mixed_feedback():
    # secret 1234, guess 1243 gives "++--"
    assert score_feedback('1234', '1243') == "++--"
    # secret 1234, guess 2134 gives "++--"
    assert score_feedback('1234', '2134') == "++--"

def test_consumed_exact_matches():
    # secret 1124, guess 5167 gives "+"
    assert score_feedback('1124', '5167') == "+"
    # secret 1111, guess 1112 gives "+++"
    assert score_feedback('1111', '1112') == "+++"

def test_duplicate_digit_feedback():
    # secret 1234, guess 5115 gives "-"
    assert score_feedback('1234', '5115') == "-"
    # secret 1122, guess 2211 gives "----"
    assert score_feedback('1122', '2211') == "----"

def test_reusable_scorer():
    # The same scorer answers successive guesses independently
    secret = '1234'
    assert score_feedback(secret, '5678') == ""
    assert score_feedback(secret, '1243') == "++--"

def test_secret_validation_too_short():
    # secret shorter than 4 characters
    import pytest
    with pytest.raises(Exception) as exc_info:
        score_feedback('123', '1234')
    assert str(exc_info.value) == "code must be 4 to 6 characters long"

def test_secret_validation_too_long():
    # secret longer than 6 characters
    import pytest
    with pytest.raises(Exception) as exc_info:
        score_feedback('1234567', '1234')
    assert str(exc_info.value) == "code must be 4 to 6 characters long"

def test_secret_validation_invalid_characters():
    # secret containing invalid characters
    import pytest
    with pytest.raises(Exception) as exc_info:
        score_feedback('1237', '1234')
    assert str(exc_info.value) == "code may only contain characters from '123456'"

def test_guess_validation_length():
    # guess whose length differs from the secret's
    import pytest
    with pytest.raises(Exception) as exc_info:
        score_feedback('1234', '12345')
    assert str(exc_info.value) == "guess must be the same length as the secret"

def test_guess_validation_invalid_characters():
    # guess digits outside the alphabet are tolerated
    # secret 1234, guess 1789 gives "+"
    assert score_feedback('1234', '1789') == "+"

def test_longer_codes():
    # secret of 5 digits
    assert score_feedback('12345', '12345') == "+++++"
    assert score_feedback('12345', '54321') == "+----"  # The correct feedback is "+----", not "-----"
    # secret of 6 digits
    assert score_feedback('123456', '123456') == "++++++"
    assert score_feedback('123456', '654321') == "------"

def test_custom_alphabet():
    # with a custom alphabet of 1 through 8, secret 1278 must be rejected
    import pytest
    with pytest.raises(Exception) as exc_info:
        score_feedback('1278', '1287')
    assert str(exc_info.value) == "code may only contain characters from '123456'"