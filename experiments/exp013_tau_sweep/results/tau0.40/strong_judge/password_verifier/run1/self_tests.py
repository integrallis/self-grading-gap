from solution import verify_password

def test_accepting_strong_passwords():
    # AC-1.1: A password longer than 8 characters that contains at least one uppercase letter, one lowercase letter, and one number is accepted
    assert verify_password("StrongPass1") == "Password is valid"  # meets all criteria
    # AC-1.2: The length rule is strict: a password of exactly 9 characters that meets the other rules is accepted
    assert verify_password("Abcdefg1H") == "Password is valid"  # meets all criteria

def test_refusing_weak_passwords_with_rule_specific_messages():
    # AC-2.1: A missing password is refused with the message "Password should not be null"
    assert verify_password(None) == "Password should not be null"  # missing password
    
    # AC-2.2: A password of 8 or fewer characters is refused
    assert verify_password("Short1") == "Password should be longer than 8 characters"  # too short
    assert verify_password("12345678") == "Password should be longer than 8 characters"  # too short
    assert verify_password("abcdefgh") == "Password should be longer than 8 characters"  # too short
    assert verify_password("ABCDEFGH") == "Password should be longer than 8 characters"  # too short
    assert verify_password("abcdefgH") == "Password should be longer than 8 characters"  # too short
    
    # AC-2.3: A password with no uppercase letter is refused
    assert verify_password("lowercase1") == "Password should have at least one uppercase letter"  # no uppercase
    # AC-2.4: A password with no lowercase letter is refused
    assert verify_password("UPPERCASE1") == "Password should have at least one lowercase letter"  # no lowercase
    # AC-2.5: A password with no number is refused
    assert verify_password("UppercaseX") == "Password should have at least one number"  # no number

    # AC-2.6: A password breaking several rules at once is refused for its shortness first
    assert verify_password("abc") == "Password should be longer than 8 characters"  # too short and missing rules