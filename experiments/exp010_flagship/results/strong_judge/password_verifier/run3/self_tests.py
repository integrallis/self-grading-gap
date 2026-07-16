from solution import verify_password_strength

def test_accepting_strong_passwords():
    # AC-1.1
    assert verify_password_strength("Valid1234") == "Accepted"  # meets all rules
    # AC-1.2
    assert verify_password_strength("StrongPass1") == "Accepted"  # length is 11, meets all rules

def test_refusing_weak_passwords_with_rule_specific_messages():
    # AC-2.1
    assert verify_password_strength(None) == "Password should not be null"  # missing password
    # AC-2.2
    assert verify_password_strength("Short1") == "Password should be longer than 8 characters"  # 6 characters
    assert verify_password_strength("Abcdefg1") == "Password should be longer than 8 characters"  # 8 characters
    # AC-2.3
    assert verify_password_strength("lowercase1") == "Password should have at least one uppercase letter"  # no uppercase
    # AC-2.4
    assert verify_password_strength("UPPERCASE1") == "Password should have at least one lowercase letter"  # no lowercase
    # AC-2.5
    assert verify_password_strength("NoNumberX") == "Password should have at least one number"  # no number
    # AC-2.6
    assert verify_password_strength("short") == "Password should be longer than 8 characters"  # too short, also lacks uppercase and number
    assert verify_password_strength("short1") == "Password should be longer than 8 characters"  # too short, also lacks uppercase
    assert verify_password_strength("SHORT") == "Password should be longer than 8 characters"  # too short, also lacks lowercase and number