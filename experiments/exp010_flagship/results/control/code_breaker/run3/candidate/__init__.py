def score_guess(secret, guess):
    exact_matches = sum(s == g for s, g in zip(secret, guess))
    partial_matches = 0
    secret_counts = {}
    guess_counts = {}

    for s in secret:
        if s not in secret_counts:
            secret_counts[s] = 0
        secret_counts[s] += 1
    
    for g in guess:
        if g not in guess_counts:
            guess_counts[g] = 0
        guess_counts[g] += 1

    for digit in guess_counts:
        if digit in secret_counts:
            partial_matches += min(secret_counts[digit], guess_counts[digit])

    partial_matches -= exact_matches

    return "+" * exact_matches + "-" * partial_matches


def validate_secret(secret):
    if not (4 <= len(secret) <= 6):
        return "code must be 4 to 6 characters long"
    if not all(c in '0123456' for c in secret):
        return "code may only contain characters from '123456'"
    return None


def validate_guess(secret, guess):
    if len(guess) != len(secret):
        return "guess must be the same length as the secret"
    if not all(c in '0123456' or c not in secret for c in guess):
        return "guess may only contain characters from '123456'"
    return None
