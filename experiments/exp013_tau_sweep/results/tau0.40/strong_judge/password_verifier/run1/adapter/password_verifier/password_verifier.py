# file: password_verifier/password_verifier.py
from candidate import verify_password


class PasswordVerifier:
    def verify(self, password):
        return verify_password(password)
