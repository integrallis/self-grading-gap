def start_game():
    return {'score': 301, 'turn': 1, 'darts_remaining': 3, 'finished': False}

def throw_dart(game, score, is_double=False, is_triple=False):
    if game['finished']:
        return game
    # Calculate the score based on the dart type
    if is_double:
        score *= 2
    elif is_triple:
        score *= 3
    # Check for bust
    if game['score'] - score < 0 or (game['score'] - score == 0 and not is_double):
        game['score'] = 301
        game['darts_remaining'] = 3
        game['turn'] += 1
        return game
    # Update the score
    game['score'] -= score
    game['darts_remaining'] -= 1
    # Check for winning condition
    if game['score'] == 0 and is_double:
        game['finished'] = True
        return game
    # End turn if all darts are thrown
    if game['darts_remaining'] == 0:
        game['turn'] += 1
        game['darts_remaining'] = 3
    return game
