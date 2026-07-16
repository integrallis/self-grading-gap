# test_solution.py

from solution import judge_round

def test_rock_beats_scissors():
    # Rock (player) beats Scissors (opponent) 
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_beats_paper():
    # Scissors (player) beats Paper (opponent)
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_beats_rock():
    # Paper (player) beats Rock (opponent)
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_spock_smashes_scissors():
    # Spock (player) beats Scissors (opponent)
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_spock_vaporizes_rock():
    # Spock (player) beats Rock (opponent)
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_paper_disproves_spock():
    # Paper (player) beats Spock (opponent)
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_scissors_against_rock():
    # Scissors (player) loses to Rock (opponent)
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_paper_against_scissors():
    # Paper (player) loses to Scissors (opponent)
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_rock_against_paper():
    # Rock (player) loses to Paper (opponent)
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_scissors_against_spock():
    # Scissors (player) loses to Spock (opponent)
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_rock_against_spock():
    # Rock (player) loses to Spock (opponent)
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_spock_against_paper():
    # Spock (player) loses to Paper (opponent)
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # Rock (player) against Rock (opponent) ties
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # Paper (player) against Paper (opponent) ties
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # Scissors (player) against Scissors (opponent) ties
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # Spock (player) against Spock (opponent) ties
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_rules_are_complete_and_symmetric():
    # Test all combinations of moves
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"
    
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"
    
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"
    
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"
    
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"
    
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

    assert judge_round("ROCK", "ROCK") == "TIE"
    assert judge_round("PAPER", "PAPER") == "TIE"
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"
    assert judge_round("SPOCK", "SPOCK") == "TIE"