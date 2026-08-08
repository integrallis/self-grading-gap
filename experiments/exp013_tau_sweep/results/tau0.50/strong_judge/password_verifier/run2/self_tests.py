# your complete test file
from solution import verify_password

def test_accepting_strong_passwords():
    # AC-1.1: A password longer than 8 characters that contains at least one uppercase letter, one lowercase letter, and one number is accepted
    assert verify_password("StrongPass1")  # No expected value defined

    # AC-1.2: The length rule is strict: a password of exactly 9 characters that meets the other rules is accepted
    assert verify_password("Valid9Pwd")  # No expected value defined

def test_refusing_weak_passwords_with_rule_specific_messages():
    # AC-2.1: A missing password is refused with the message exactly "Password should not be null"
    assert verify_password(None) == "Password should not be null"
    
    # AC-2.2: A password of 8 or fewer characters is refused with the message exactly "Password should be longer than 8 characters"
    assert verify_password("Short7") == "Password should be longer than 8 characters"  # Length 6
    assert verify_password("Short8") == "Password should be longer than 8 characters"  # Length 6
    assert verify_password("Abcdefg1") == "Password should be longer than 8 characters"  # Length 8
    
    # AC-2.3: A password with no uppercase letter is refused with the message exactly "Password should have at least one uppercase letter"
    assert verify_password("lowercase1") == "Password should have at least one uppercase letter"
    
    # AC-2.4: A password with no lowercase letter is refused with the message exactly "Password should have at least one lowercase letter"
    assert verify_password("UPPERCASE1") == "Password should have at least one lowercase letter"
    
    # AC-2.5: A password with no number is refused with the message exactly "Password should have at least one number"
    assert verify_password("NoNumberHere") == "Password should have at least one number"
    
    # AC-2.6: A password breaking several rules at once is refused for its shortness first
    assert verify_password("short!") == "Password should be longer than 8 characters"  # Length 6
    assert verify_password("!@#$%^&*") == "Password should be longer than 8 characters"  # Length 8