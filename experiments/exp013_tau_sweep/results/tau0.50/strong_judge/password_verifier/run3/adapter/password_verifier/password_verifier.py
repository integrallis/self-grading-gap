# file: password_verifier/password_verifier.py
from candidate import password_verifier as _password_verifier


class PasswordVerifier:
    def verify(self, password):
        return _password_verifier(password)
