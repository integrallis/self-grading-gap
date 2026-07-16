# test_solution.py

from solution import *  # Import everything from solution package

def test_rock_beats_scissors():
    # ROCK beats SCISSORS -> PLAYER_WINS
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_beat_paper():
    # SCISSORS beats PAPER -> PLAYER_WINS
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_beats_rock():
    # PAPER beats ROCK -> PLAYER_WINS
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_scissors_lose_to_rock():
    # SCISSORS lose to ROCK -> PLAYER_LOSES
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_paper_lose_to_scissors():
    # PAPER lose to SCISSORS -> PLAYER_LOSES
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_rock_lose_to_paper():
    # ROCK lose to PAPER -> PLAYER_LOSES
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_spock_smashes_scissors():
    # SPOCK smashes SCISSORS -> PLAYER_WINS
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_lose_to_spock():
    # SCISSORS lose to SPOCK -> PLAYER_LOSES
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_spock_vaporizes_rock():
    # SPOCK vaporizes ROCK -> PLAYER_WINS
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_spock():
    # ROCK lose to SPOCK -> PLAYER_LOSES
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_paper_disproves_spock():
    # PAPER disproves SPOCK -> PLAYER_WINS
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_spock_lose_to_paper():
    # SPOCK lose to PAPER -> PLAYER_LOSES
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # ROCK against ROCK -> TIE
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # PAPER against PAPER -> TIE
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # SCISSORS against SCISSORS -> TIE
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # SPOCK against SPOCK -> TIE
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_different_moves_never_tie():
    # Different moves -> not TIE (example: ROCK vs PAPER)
    assert judge_round("ROCK", "PAPER") != "TIE"

def test_all_combinations_have_one_verdict():
    moves = ["ROCK", "PAPER", "SCISSORS", "SPOCK"]
    verdicts = set()
    for move1 in moves:
        for move2 in moves:
            verdict = judge_round(move1, move2)
            assert verdict in ["PLAYER_WINS", "PLAYER_LOSES", "TIE"]
            verdicts.add(verdict)
    assert len(verdicts) == 3  # Should contain exactly 3 unique verdicts

def test_symmetry_of_verdicts():
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"