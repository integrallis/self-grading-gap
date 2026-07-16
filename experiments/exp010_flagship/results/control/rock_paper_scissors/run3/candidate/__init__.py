def judge_round(player_move, opponent_move):
    if player_move == opponent_move:
        return "TIE"

    winning_moves = {
        "ROCK": ["SCISSORS", "LIZARD"],
        "PAPER": ["ROCK", "SPOCK"],
        "SCISSORS": ["PAPER", "LIZARD"],
        "SPOCK": ["SCISSORS", "ROCK"],
        "LIZARD": ["SPOCK", "PAPER"]
    }

    if opponent_move in winning_moves[player_move]:
        return "PLAYER_WINS"
    else:
        return "PLAYER_LOSES"