from solution import password_verifier

def test_accepting_strong_passwords():
    # AC-1.1: A password longer than 8 characters that contains at least one uppercase letter, one lowercase letter, and one number is accepted
    assert password_verifier("Abcdefg1h") == "Password is valid"  # valid
    # AC-1.2: The length rule is strict: a password of exactly 9 characters that meets the other rules is accepted
    assert password_verifier("Aabcdefg1") == "Password is valid"  # valid

def test_refusing_weak_passwords_with_messages():
    # AC-2.1: A missing password is refused with the message "Password should not be null"
    assert password_verifier(None) == "Password should not be null"  # null password
    # AC-2.2: A password of 8 or fewer characters is refused with the message "Password should be longer than 8 characters"
    assert password_verifier("Abcdefg") == "Password should be longer than 8 characters"  # 7 characters
    assert password_verifier("Abcdefg1") == "Password should be longer than 8 characters"  # 8 characters
    # AC-2.3: A password with no uppercase letter is refused with the message "Password should have at least one uppercase letter"
    assert password_verifier("abcdefg1") == "Password should have at least one uppercase letter"  # no uppercase
    # AC-2.4: A password with no lowercase letter is refused with the message "Password should have at least one lowercase letter"
    assert password_verifier("ABCDEFG1") == "Password should have at least one lowercase letter"  # no lowercase
    # AC-2.5: A password with no number is refused with the message "Password should have at least one number"
    assert password_verifier("Abcdefgh") == "Password should have at least one number"  # no number
    # AC-2.6: A password breaking several rules at once is refused for its shortness first
    assert password_verifier("ABCDEFG") == "Password should be longer than 8 characters"  # too short, no lowercase, no number
    assert password_verifier("abcdefg") == "Password should be longer than 8 characters"  # too short, no uppercase, no number
    assert password_verifier("ABCDEF1") == "Password should have at least one lowercase letter"  # too short, no lowercase