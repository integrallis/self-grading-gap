from solution.password_verifier import password_verifier

def test_accepting_strong_passwords():
    # AC-1.1: A password longer than 8 characters that contains at least one uppercase letter, one lowercase letter, and one number is accepted
    assert password_verifier("StrongPass1")  # meets all criteria

    # AC-1.2: The length rule is strict: a password of exactly 9 characters that meets the other rules is accepted
    assert password_verifier("ValidPwd1")  # meets all criteria

    # AC-1.2: Testing exactly 8 characters satisfying character-class rules
    assert password_verifier("Abcdefg1") == "Password should be longer than 8 characters"  # exactly 8 characters


def test_refusing_weak_passwords_with_rule_specific_messages():
    # AC-2.1: A missing password is refused with the message exactly "Password should not be null"
    assert password_verifier(None) == "Password should not be null"  # null password

    # AC-2.2: A password of 8 or fewer characters is refused with the message exactly "Password should be longer than 8 characters"
    assert password_verifier("Short1") == "Password should be longer than 8 characters"  # 7 characters
    assert password_verifier("Eight1") == "Password should be longer than 8 characters"  # 8 characters

    # AC-2.3: A password with no uppercase letter is refused with the message exactly "Password should have at least one uppercase letter"
    assert password_verifier("lowercase1") == "Password should have at least one uppercase letter"  # no uppercase

    # AC-2.4: A password with no lowercase letter is refused with the message exactly "Password should have at least one lowercase letter"
    assert password_verifier("UPPERCASE1") == "Password should have at least one lowercase letter"  # no lowercase

    # AC-2.5: A password with no number is refused with the message exactly "Password should have at least one number"
    assert password_verifier("NoNumberHere") == "Password should have at least one number"  # no number

    # AC-2.6: A password breaking several rules at once is refused for its shortness first
    assert password_verifier("Short") == "Password should be longer than 8 characters"  # too short, also no uppercase and no number
    assert password_verifier("short") == "Password should be longer than 8 characters"  # too short, also no uppercase and no number
    assert password_verifier("ShortNoNumber") == "Password should have at least one number"  # has uppercase and lowercase, but no number