def start_game():
    return {'score': 301, 'finished': False, 'turn': 1, 'darts_remaining': 3}

def throw_dart(game, *args):
    if game['finished']:
        return game  # No action if the game is finished

    current_score = game['score']
    darts_remaining = game['darts_remaining']
    turn = game['turn']

    if len(args) == 1:
        points = args[0]
    else:
        multiplier = 1
        if args[0] == 'double':
            multiplier = 2
        elif args[0] == 'triple':
            multiplier = 3
        points = args[1] * multiplier

    if current_score - points < 0:
        # Bust: Restore score and reset darts
        game['score'] = 301
        game['darts_remaining'] = 3
    elif current_score - points == 0 and (len(args) == 2 and args[0] == 'double' and args[1] == 1):
        # Winning throw with double
        game['score'] = 0
        game['finished'] = True
    elif current_score - points == 0:
        # Cannot end on a non-double
        game['score'] = current_score
        game['darts_remaining'] = 3
    else:
        game['score'] -= points
        game['darts_remaining'] -= 1

    # Check if darts remaining is 0 to end turn
    if game['darts_remaining'] == 0:
        game['turn'] += 1
        game['darts_remaining'] = 3

    return game
