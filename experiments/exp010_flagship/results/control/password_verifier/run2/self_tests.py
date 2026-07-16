from solution import verify_password

def test_accepts_strong_password():
    # A password longer than 8 characters that contains 
    # at least one uppercase letter, one lowercase letter, 
    # and one number is accepted.
    assert verify_password("Valid1Password") == True

def test_accepts_nine_characters_strong_password():
    # A password of exactly 9 characters that meets the 
    # other rules is accepted.
    assert verify_password("A1b234567") == True

def test_refuses_missing_password():
    # A missing password is refused with the message 
    # "Password should not be null".
    assert verify_password(None) == "Password should not be null"

def test_refuses_too_short_password():
    # A password of 8 or fewer characters is refused with 
    # the message "Password should be longer than 8 characters".
    assert verify_password("Short1") == "Password should be longer than 8 characters"
    assert verify_password("Short12") == "Password should be longer than 8 characters"
    assert verify_password("Short8!") == "Password should be longer than 8 characters"
    assert verify_password("Short!") == "Password should be longer than 8 characters"

def test_refuses_no_uppercase_letter():
    # A password with no uppercase letter is refused with 
    # the message "Password should have at least one uppercase letter".
    assert verify_password("lowercase1") == "Password should have at least one uppercase letter"
    assert verify_password("lowercase!") == "Password should have at least one uppercase letter"

def test_refuses_no_lowercase_letter():
    # A password with no lowercase letter is refused with 
    # the message "Password should have at least one lowercase letter".
    assert verify_password("UPPERCASE1") == "Password should have at least one lowercase letter"
    assert verify_password("UPPERCASE!") == "Password should have at least one lowercase letter"

def test_refuses_no_number():
    # A password with no number is refused with the message 
    # "Password should have at least one number".
    assert verify_password("NoNumber!") == "Password should have at least one number"
    assert verify_password("NoNumber") == "Password should have at least one number"

def test_refuses_multiple_rules():
    # A password breaking several rules at once is refused 
    # for its shortness first: 
    # a too-short password is reported against the length rule 
    # even when it also lacks an uppercase letter and a number.
    assert verify_password("short") == "Password should be longer than 8 characters"
    assert verify_password("short1") == "Password should be longer than 8 characters"
    assert verify_password("SHORT!") == "Password should be longer than 8 characters"
    assert verify_password("shortnumber!") == "Password should be longer than 8 characters"