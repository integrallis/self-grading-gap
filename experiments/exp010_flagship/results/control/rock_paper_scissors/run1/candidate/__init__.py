def judge_round(player_move, opponent_move):
    winning_combinations = {
        "ROCK": ["SCISSORS", "LIZARD"],
        "SCISSORS": ["PAPER", "LIZARD"],
        "PAPER": ["ROCK", "SPOCK"],
        "SPOCK": ["SCISSORS", "ROCK"],
        "LIZARD": ["SPOCK", "PAPER"]
    }

    if player_move == opponent_move:
        return "TIE"
    elif opponent_move in winning_combinations[player_move]:
        return "PLAYER_WINS"
    else:
        return "PLAYER_LOSES"