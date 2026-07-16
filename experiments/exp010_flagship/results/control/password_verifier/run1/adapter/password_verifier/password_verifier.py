# file: password_verifier/password_verifier.py
from candidate import password_verifier


class PasswordVerifier:
    def verify(self, password):
        return password_verifier(password)
