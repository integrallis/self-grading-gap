# test_solution.py

from solution import judge_round, ROCK, PAPER, SCISSORS, SPOCK, PLAYER_WINS, PLAYER_LOSES, TIE

def test_rock_beats_scissors():
    # Rock (PLAYER) against Scissors (OPPONENT) is a win for the player.
    assert judge_round(ROCK, SCISSORS) == PLAYER_WINS

def test_scissors_lose_to_rock():
    # Scissors (PLAYER) against Rock (OPPONENT) is a loss for the player.
    assert judge_round(SCISSORS, ROCK) == PLAYER_LOSES

def test_scissors_beat_paper():
    # Scissors (PLAYER) against Paper (OPPONENT) is a win for the player.
    assert judge_round(SCISSORS, PAPER) == PLAYER_WINS

def test_paper_lose_to_scissors():
    # Paper (PLAYER) against Scissors (OPPONENT) is a loss for the player.
    assert judge_round(PAPER, SCISSORS) == PLAYER_LOSES

def test_paper_beats_rock():
    # Paper (PLAYER) against Rock (OPPONENT) is a win for the player.
    assert judge_round(PAPER, ROCK) == PLAYER_WINS

def test_rock_lose_to_paper():
    # Rock (PLAYER) against Paper (OPPONENT) is a loss for the player.
    assert judge_round(ROCK, PAPER) == PLAYER_LOSES

def test_spock_smashes_scissors():
    # Spock (PLAYER) against Scissors (OPPONENT) is a win for the player.
    assert judge_round(SPOCK, SCISSORS) == PLAYER_WINS

def test_scissors_lose_to_spock():
    # Scissors (PLAYER) against Spock (OPPONENT) is a loss for the player.
    assert judge_round(SCISSORS, SPOCK) == PLAYER_LOSES

def test_spock_vaporizes_rock():
    # Spock (PLAYER) against Rock (OPPONENT) is a win for the player.
    assert judge_round(SPOCK, ROCK) == PLAYER_WINS

def test_rock_lose_to_spock():
    # Rock (PLAYER) against Spock (OPPONENT) is a loss for the player.
    assert judge_round(ROCK, SPOCK) == PLAYER_LOSES

def test_paper_disproves_spock():
    # Paper (PLAYER) against Spock (OPPONENT) is a win for the player.
    assert judge_round(PAPER, SPOCK) == PLAYER_WINS

def test_spock_lose_to_paper():
    # Spock (PLAYER) against Paper (OPPONENT) is a loss for the player.
    assert judge_round(SPOCK, PAPER) == PLAYER_LOSES

def test_identical_moves_tie_rock():
    # Rock (PLAYER) against Rock (OPPONENT) is a tie.
    assert judge_round(ROCK, ROCK) == TIE

def test_identical_moves_tie_paper():
    # Paper (PLAYER) against Paper (OPPONENT) is a tie.
    assert judge_round(PAPER, PAPER) == TIE

def test_identical_moves_tie_scissors():
    # Scissors (PLAYER) against Scissors (OPPONENT) is a tie.
    assert judge_round(SCISSORS, SCISSORS) == TIE

def test_identical_moves_tie_spock():
    # Spock (PLAYER) against Spock (OPPONENT) is a tie.
    assert judge_round(SPOCK, SPOCK) == TIE

def test_all_possible_pairings_yield_a_verdict():
    # Test all possible pairings of moves and their verdicts.
    assert judge_round(ROCK, ROCK) == TIE
    assert judge_round(ROCK, PAPER) == PLAYER_LOSES
    assert judge_round(ROCK, SCISSORS) == PLAYER_WINS
    assert judge_round(ROCK, SPOCK) == PLAYER_LOSES
    assert judge_round(PAPER, ROCK) == PLAYER_WINS
    assert judge_round(PAPER, PAPER) == TIE
    assert judge_round(PAPER, SCISSORS) == PLAYER_LOSES
    assert judge_round(PAPER, SPOCK) == PLAYER_WINS
    assert judge_round(SCISSORS, ROCK) == PLAYER_LOSES
    assert judge_round(SCISSORS, PAPER) == PLAYER_WINS
    assert judge_round(SCISSORS, SCISSORS) == TIE
    assert judge_round(SCISSORS, SPOCK) == PLAYER_LOSES
    assert judge_round(SPOCK, ROCK) == PLAYER_WINS
    assert judge_round(SPOCK, PAPER) == PLAYER_LOSES
    assert judge_round(SPOCK, SCISSORS) == PLAYER_WINS
    assert judge_round(SPOCK, SPOCK) == TIE

def test_swapped_pairings_reverse_verdicts():
    # Test that swapped pairings yield reversed verdicts.
    assert judge_round(ROCK, SCISSORS) == PLAYER_WINS
    assert judge_round(SCISSORS, ROCK) == PLAYER_LOSES
    assert judge_round(SCISSORS, PAPER) == PLAYER_WINS
    assert judge_round(PAPER, SCISSORS) == PLAYER_LOSES
    assert judge_round(PAPER, ROCK) == PLAYER_WINS
    assert judge_round(ROCK, PAPER) == PLAYER_LOSES
    assert judge_round(SPOCK, SCISSORS) == PLAYER_WINS
    assert judge_round(SCISSORS, SPOCK) == PLAYER_LOSES
    assert judge_round(SPOCK, ROCK) == PLAYER_WINS
    assert judge_round(ROCK, SPOCK) == PLAYER_LOSES
    assert judge_round(PAPER, SPOCK) == PLAYER_WINS
    assert judge_round(SPOCK, PAPER) == PLAYER_LOSES