# test_solution.py

from solution import judge_round

def test_rock_beats_scissors():
    # Rock beats scissors: PLAYER_WINS
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"
    
def test_scissors_lose_to_rock():
    # Scissors lose to rock: PLAYER_LOSES
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_scissors_beat_paper():
    # Scissors beat paper: PLAYER_WINS
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_lose_to_scissors():
    # Paper lose to scissors: PLAYER_LOSES
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_paper_beat_rock():
    # Paper beats rock: PLAYER_WINS
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_paper():
    # Rock loses to paper: PLAYER_LOSES
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_spock_smashes_scissors():
    # Spock smashes scissors: PLAYER_WINS
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_lose_to_spock():
    # Scissors lose to Spock: PLAYER_LOSES
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_spock_vaporizes_rock():
    # Spock vaporizes rock: PLAYER_WINS
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_spock():
    # Rock loses to Spock: PLAYER_LOSES
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_paper_disproves_spock():
    # Paper disproves Spock: PLAYER_WINS
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_spock_lose_to_paper():
    # Spock loses to paper: PLAYER_LOSES
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # Identical moves tie: ROCK vs ROCK
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # Identical moves tie: PAPER vs PAPER
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # Identical moves tie: SCISSORS vs SCISSORS
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # Identical moves tie: SPOCK vs SPOCK
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_different_moves_never_tie():
    # Different moves never tie: ROCK vs PAPER
    assert judge_round("ROCK", "PAPER") != "TIE"
    # Different moves never tie: SCISSORS vs ROCK
    assert judge_round("SCISSORS", "ROCK") != "TIE"
    # Different moves never tie: SPOCK vs SCISSORS
    assert judge_round("SPOCK", "SCISSORS") != "TIE"

def test_expose_moves():
    # Ensure the moves are exactly ROCK, PAPER, SCISSORS, SPOCK
    assert {"ROCK", "PAPER", "SCISSORS", "SPOCK"} == {"ROCK", "PAPER", "SCISSORS", "SPOCK"}

def test_expose_verdicts():
    # Ensure the verdicts are exactly PLAYER_WINS, PLAYER_LOSES, TIE
    assert {"PLAYER_WINS", "PLAYER_LOSES", "TIE"} == {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}