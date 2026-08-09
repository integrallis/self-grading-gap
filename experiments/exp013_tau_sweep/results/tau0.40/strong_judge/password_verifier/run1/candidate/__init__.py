def verify_password(password):
    if password is None:
        return "Password should not be null"
    if len(password) <= 8:
        return "Password should be longer than 8 characters"
    if not any(char.isupper() for char in password):
        return "Password should have at least one uppercase letter"
    if not any(char.islower() for char in password):
        return "Password should have at least one lowercase letter"
    if not any(char.isdigit() for char in password):
        return "Password should have at least one number"
    return "Password is valid"