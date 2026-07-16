def judge_round(player_move, opponent_move):
    # Define the winning conditions
    winning_combinations = {
        "ROCK": ["SCISSORS", "LIZARD"],
        "SCISSORS": ["PAPER", "LIZARD"],
        "PAPER": ["ROCK", "SPOCK"],
        "SPOCK": ["SCISSORS", "PAPER", "ROCK"],
        "LIZARD": ["SPOCK", "PAPER"]
    }

    # Check for tie
    if player_move == opponent_move:
        return "TIE"

    # Check if player wins
    if opponent_move in winning_combinations[player_move]:
        return "PLAYER_WINS"

    # Otherwise, player loses
    return "PLAYER_LOSES"