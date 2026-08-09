from solution import password_verifier

def test_accepts_strong_password():
    # A password longer than 8 characters containing upper, lower, and number
    assert password_verifier("StrongPass1") == "Password is accepted"  # Accepted report

def test_accepts_nine_character_password():
    # Exactly 9 characters long, meeting all other requirements
    assert password_verifier("Valid9Pwd") == "Password is accepted"  # Accepted report

def test_refuses_null_password():
    # Missing password
    assert password_verifier(None) == "Password should not be null"  # Refused for null

def test_refuses_short_password():
    # Password of 8 characters
    assert password_verifier("Short8") == "Password should be longer than 8 characters"  # Refused for length

def test_refuses_password_missing_uppercase():
    # Password without any uppercase letters
    assert password_verifier("nouppercase1") == "Password should have at least one uppercase letter"  # Refused for missing uppercase

def test_refuses_password_missing_lowercase():
    # Password without any lowercase letters
    assert password_verifier("NOLOWERCASE1") == "Password should have at least one lowercase letter"  # Refused for missing lowercase

def test_refuses_password_missing_number():
    # Password without any numbers
    assert password_verifier("NoNumberPassword") == "Password should have at least one number"  # Refused for missing number

def test_refuses_password_missing_uppercase_and_number():
    # Short password that is missing both an uppercase letter and a number
    assert password_verifier("shortpw") == "Password should be longer than 8 characters"  # Refused for length

def test_refuses_password_missing_lowercase_and_number():
    # Short password that is missing both a lowercase letter and a number
    assert password_verifier("SHORTPW") == "Password should be longer than 8 characters"  # Refused for length

def test_refuses_password_missing_uppercase_and_lowercase():
    # Short password that is missing both uppercase and lowercase letters
    assert password_verifier("12345678") == "Password should be longer than 8 characters"  # Refused for length