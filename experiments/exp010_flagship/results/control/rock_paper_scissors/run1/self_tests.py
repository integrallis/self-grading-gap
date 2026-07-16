# test_solution.py

from solution import judge_round

# User Stories: Judging the classic pairings
def test_rock_beats_scissors():
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"  # ROCK beats SCISSORS
def test_scissors_lose_to_rock():
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"  # SCISSORS lose to ROCK

def test_scissors_beat_paper():
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"  # SCISSORS beat PAPER
def test_paper_lose_to_scissors():
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"  # PAPER loses to SCISSORS

def test_paper_beats_rock():
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"  # PAPER beats ROCK
def test_rock_lose_to_paper():
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"  # ROCK loses to PAPER

# User Stories: Judging Spock's pairings
def test_spock_smashes_scissors():
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"  # SPOCK smashes SCISSORS
def test_scissors_lose_to_spock():
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"  # SCISSORS lose to SPOCK

def test_spock_vaporizes_rock():
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"  # SPOCK vaporizes ROCK
def test_rock_lose_to_spock():
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"  # ROCK loses to SPOCK

def test_paper_disproves_spock():
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"  # PAPER disproves SPOCK
def test_spock_lose_to_paper():
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"  # SPOCK loses to PAPER

# User Stories: Tying on identical moves
def test_identical_moves_tie_rock():
    assert judge_round("ROCK", "ROCK") == "TIE"  # ROCK against ROCK ties
def test_identical_moves_tie_paper():
    assert judge_round("PAPER", "PAPER") == "TIE"  # PAPER against PAPER ties
def test_identical_moves_tie_scissors():
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"  # SCISSORS against SCISSORS ties
def test_identical_moves_tie_spock():
    assert judge_round("SPOCK", "SPOCK") == "TIE"  # SPOCK against SPOCK ties

# User Stories: Completing and balancing the rule book
def test_all_pairings():
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"  # ROCK loses to PAPER
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"  # ROCK beats SCISSORS
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"  # ROCK loses to SPOCK
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"  # PAPER beats ROCK
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"  # PAPER loses to SCISSORS
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"  # PAPER disproves SPOCK
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"  # SCISSORS lose to ROCK
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"  # SCISSORS beat PAPER
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"  # SCISSORS lose to SPOCK
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"  # SPOCK vaporizes ROCK
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"  # SPOCK loses to PAPER
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"  # SPOCK smashes SCISSORS

# User Stories: Closing the move and verdict vocabularies
def test_valid_moves():
    # Testing the exact moves
    assert judge_round("ROCK", "PAPER") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
    assert judge_round("PAPER", "SCISSORS") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
    assert judge_round("SCISSORS", "ROCK") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
    assert judge_round("SPOCK", "SCISSORS") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
    assert judge_round("SPOCK", "ROCK") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
    assert judge_round("PAPER", "SPOCK") in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]