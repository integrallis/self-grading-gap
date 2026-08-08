def password_verifier(password):
    if password is None:
        return "Password should not be null"
    if len(password) <= 8:
        return "Password should be longer than 8 characters"
    if not any(c.isupper() for c in password):
        return "Password should have at least one uppercase letter"
    if not any(c.islower() for c in password):
        return "Password should have at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return "Password should have at least one number"
    return True