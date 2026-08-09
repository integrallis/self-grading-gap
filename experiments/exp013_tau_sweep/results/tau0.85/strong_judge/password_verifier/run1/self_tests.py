from solution import verify_password

def test_accept_strong_password():
    # A password longer than 8 characters that contains at least one uppercase letter,
    # one lowercase letter, and one number is accepted, and verification reports success.
    assert verify_password("ValidPass1") == True  # Expect success as specified

    # The length rule is strict: a password of exactly 9 characters that meets the other rules is accepted.
    assert verify_password("Abcdefg1H") == True  # Expect success as specified

def test_refuse_weak_password_null():
    # A missing password is refused with the message exactly "Password should not be null".
    assert verify_password(None) == "Password should not be null"

def test_refuse_weak_password_too_short():
    # A password of 8 or fewer characters is refused with the message exactly
    # "Password should be longer than 8 characters"; exactly 8 characters is still too short.
    assert verify_password("Short1") == "Password should be longer than 8 characters"
    assert verify_password("Short12") == "Password should be longer than 8 characters"
    assert verify_password("Shorts!") == "Password should be longer than 8 characters"
    assert verify_password("Shorts1") == "Password should be longer than 8 characters"
    assert verify_password("Short12!") == "Password should be longer than 8 characters"
    assert verify_password("Short") == "Password should be longer than 8 characters"
    assert verify_password("Short12") == "Password should be longer than 8 characters"

def test_refuse_weak_password_no_uppercase():
    # A password with no uppercase letter is refused with the message exactly
    # "Password should have at least one uppercase letter".
    assert verify_password("lowercase1") == "Password should have at least one uppercase letter"

def test_refuse_weak_password_no_lowercase():
    # A password with no lowercase letter is refused with the message exactly
    # "Password should have at least one lowercase letter".
    assert verify_password("UPPERCASE1") == "Password should have at least one lowercase letter"

def test_refuse_weak_password_no_number():
    # A password with no number is refused with the message exactly
    # "Password should have at least one number".
    assert verify_password("NoNumber") == "Password should be longer than 8 characters"  # Exact length rule applies first
    assert verify_password("NoNumber!") == "Password should have at least one number"

def test_refuse_weak_password_multiple_issues():
    # A password breaking several rules at once is refused for its shortness first:
    # a too-short password is reported against the length rule even when it also lacks
    # an uppercase letter and a number.
    assert verify_password("short") == "Password should be longer than 8 characters"
    assert verify_password("short1") == "Password should be longer than 8 characters"
    assert verify_password("SHORT") == "Password should be longer than 8 characters"
    assert verify_password("short!") == "Password should be longer than 8 characters"
    assert verify_password("short123") == "Password should be longer than 8 characters"