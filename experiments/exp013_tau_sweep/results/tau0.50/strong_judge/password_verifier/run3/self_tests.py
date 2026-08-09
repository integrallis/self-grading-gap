from solution import password_verifier

def test_accepts_strong_password():
    # A password longer than 8 characters that meets all rules
    assert password_verifier("StrongPassword1")  # Acceptance is unspecified

def test_accepts_password_of_exactly_nine_characters():
    # A password of exactly 9 characters that meets all rules
    assert password_verifier("Abcdefg1!")  # Acceptance is unspecified

def test_refuses_missing_password():
    # A missing password should return the specific message
    assert password_verifier(None) == "Password should not be null"

def test_refuses_password_with_eight_or_fewer_characters():
    # A password of 8 characters is still too short
    assert password_verifier("Short1!") == "Password should be longer than 8 characters"
    assert password_verifier("Short") == "Password should be longer than 8 characters"
    assert password_verifier("Abcdef1!") == "Password should be longer than 8 characters"  # exactly 8 characters

def test_refuses_password_without_uppercase_letter():
    # A password lacking an uppercase letter
    assert password_verifier("lowercase1") == "Password should have at least one uppercase letter"

def test_refuses_password_without_lowercase_letter():
    # A password lacking a lowercase letter
    assert password_verifier("UPPERCASE1") == "Password should have at least one lowercase letter"

def test_refuses_password_without_number():
    # A password lacking a number
    assert password_verifier("NoNumber!") == "Password should have at least one number"

def test_refuses_password_that_breaks_multiple_rules():
    # A password that is too short and also lacks uppercase and numbers
    assert password_verifier("short") == "Password should be longer than 8 characters"