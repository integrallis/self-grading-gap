# test_solution.py

from solution import judge_round, ROCK, PAPER, SCISSORS, SPOCK, PLAYER_WINS, PLAYER_LOSES, TIE

def test_rock_beats_scissors():
    # Rock beats scissors: player wins
    assert judge_round(ROCK, SCISSORS) == PLAYER_WINS

def test_scissors_lose_to_rock():
    # Scissors against rock: player loses
    assert judge_round(SCISSORS, ROCK) == PLAYER_LOSES

def test_scissors_beats_paper():
    # Scissors beat paper: player wins
    assert judge_round(SCISSORS, PAPER) == PLAYER_WINS

def test_paper_lose_to_scissors():
    # Paper against scissors: player loses
    assert judge_round(PAPER, SCISSORS) == PLAYER_LOSES

def test_paper_beats_rock():
    # Paper beats rock: player wins
    assert judge_round(PAPER, ROCK) == PLAYER_WINS

def test_rock_lose_to_paper():
    # Rock against paper: player loses
    assert judge_round(ROCK, PAPER) == PLAYER_LOSES

def test_spock_smashes_scissors():
    # Spock smashes scissors: player wins
    assert judge_round(SPOCK, SCISSORS) == PLAYER_WINS

def test_scissors_lose_to_spock():
    # Scissors against Spock: player loses
    assert judge_round(SCISSORS, SPOCK) == PLAYER_LOSES

def test_spock_vaporizes_rock():
    # Spock vaporizes rock: player wins
    assert judge_round(SPOCK, ROCK) == PLAYER_WINS

def test_rock_lose_to_spock():
    # Rock against Spock: player loses
    assert judge_round(ROCK, SPOCK) == PLAYER_LOSES

def test_paper_disproves_spock():
    # Paper disproves Spock: player wins
    assert judge_round(PAPER, SPOCK) == PLAYER_WINS

def test_spock_lose_to_paper():
    # Spock against paper: player loses
    assert judge_round(SPOCK, PAPER) == PLAYER_LOSES

def test_identical_moves_tie_rock():
    # Identical moves tie: rock against rock
    assert judge_round(ROCK, ROCK) == TIE

def test_identical_moves_tie_paper():
    # Identical moves tie: paper against paper
    assert judge_round(PAPER, PAPER) == TIE

def test_identical_moves_tie_scissors():
    # Identical moves tie: scissors against scissors
    assert judge_round(SCISSORS, SCISSORS) == TIE

def test_identical_moves_tie_spock():
    # Identical moves tie: Spock against Spock
    assert judge_round(SPOCK, SPOCK) == TIE

def test_different_moves_never_tie():
    # Different moves never tie
    assert judge_round(ROCK, SCISSORS) == PLAYER_WINS
    assert judge_round(PAPER, SCISSORS) == PLAYER_LOSES
    assert judge_round(SPOCK, ROCK) == PLAYER_WINS
    assert judge_round(SPOCK, PAPER) == PLAYER_LOSES

def test_moves_are_exactly_four():
    # Check that moves are exactly ROCK, PAPER, SCISSORS, and SPOCK
    assert {ROCK, PAPER, SCISSORS, SPOCK} == {"ROCK", "PAPER", "SCISSORS", "SPOCK"}

def test_verdicts_are_exactly_three():
    # Check that verdicts are exactly PLAYER_WINS, PLAYER_LOSES, and TIE
    assert {PLAYER_WINS, PLAYER_LOSES, TIE} == {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}