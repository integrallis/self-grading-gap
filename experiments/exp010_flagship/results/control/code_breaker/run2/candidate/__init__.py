def score_guess(secret, guess):
    if len(secret) != len(guess):
        return ""
    correct_position = ""  
    secret_counts = {}
    guess_counts = {}

    # First pass: check for correct positions
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            correct_position += "+"
        else:
            secret_counts[secret[i]] = secret_counts.get(secret[i], 0) + 1
            guess_counts[guess[i]] = guess_counts.get(guess[i], 0) + 1

    # Second pass: count wrong positions
    wrong_position = ""
    for digit in guess_counts:
        if digit in secret_counts:
            wrong_position += "-" * min(secret_counts[digit], guess_counts[digit])

    return correct_position + wrong_position


def validate_secret(secret):
    if not (4 <= len(secret) <= 6):
        return "code must be 4 to 6 characters long"
    if any(c not in '123456' for c in secret):
        return "code may only contain characters from '123456'"
    return None


def validate_guess(secret, guess):
    if len(secret) != len(guess):
        return "guess must be the same length as the secret"
    if any(c not in '123456' for c in guess):
        return score_guess(secret, guess)
    return None