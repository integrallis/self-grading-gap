from solution import password_verifier

def test_accepting_strong_passwords():
    # AC-1.1: Password longer than 8 characters, with uppercase, lowercase, and number
    assert password_verifier("ValidPassword1") == "Password is valid"  # valid case

    # AC-1.2: Exactly 9 characters, with uppercase, lowercase, and number
    assert password_verifier("Pass12345") == "Password is valid"  # valid case


def test_refusing_weak_passwords():
    # AC-2.1: Missing password
    assert password_verifier(None) == "Password should not be null"  # null case

    # AC-2.2: Password of 8 or fewer characters
    assert password_verifier("Short1") == "Password should be longer than 8 characters"  # too short
    assert password_verifier("Short12") == "Password should be longer than 8 characters"  # too short
    assert password_verifier("Shorter") == "Password should be longer than 8 characters"  # no number
    assert password_verifier("Shorter1") == "Password should be longer than 8 characters"  # no uppercase

    # AC-2.3: No uppercase letter
    assert password_verifier("lowercase1") == "Password should have at least one uppercase letter"  # no uppercase

    # AC-2.4: No lowercase letter
    assert password_verifier("UPPERCASE1") == "Password should have at least one lowercase letter"  # no lowercase

    # AC-2.5: No number
    assert password_verifier("NoNumber") == "Password should have at least one number"  # no number

    # AC-2.6: Password breaking several rules at once (too short case first)
    assert password_verifier("Short") == "Password should be longer than 8 characters"  # too short, no uppercase, no number
    assert password_verifier("ShortUPPER") == "Password should be longer than 8 characters"  # too short, no number
    assert password_verifier("short1") == "Password should be longer than 8 characters"  # too short, no uppercase