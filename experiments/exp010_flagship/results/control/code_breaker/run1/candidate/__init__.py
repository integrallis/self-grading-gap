def score_feedback(secret, guess):
    if len(secret) < 4 or len(secret) > 6:
        return "code must be 4 to 6 characters long"
    if not secret.isdigit() or not all(c in '0123456789' for c in secret):
        return "code may only contain characters from '123456'"
    if len(guess) != len(secret):
        return "guess must be the same length as the secret"

    score = []
    secret_used = [False] * len(secret)
    guess_used = [False] * len(guess)

    # First pass for exact matches
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            score.append('+')
            secret_used[i] = True
            guess_used[i] = True
        else:
            score.append('')  # No placeholder needed here

    # Second pass for partial matches
    for i in range(len(secret)):
        if not guess_used[i]:
            for j in range(len(secret)):
                if not secret_used[j] and guess[i] == secret[j]:
                    score[i] = '-'
                    secret_used[j] = True
                    break
    return ''.join(filter(None, score))


def validate_secret(secret):
    if len(secret) < 4 or len(secret) > 6:
        return "code must be 4 to 6 characters long"
    if not secret.isdigit() or not all(c in '0123456789' for c in secret):
        return "code may only contain characters from '123456'"
    return None


def validate_guess(secret, guess):
    if len(guess) != len(secret):
        return "guess must be the same length as the secret"
    return None
