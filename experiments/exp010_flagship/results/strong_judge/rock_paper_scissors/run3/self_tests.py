# test_solution.py

from solution import judge_round

def test_classic_rock_beats_scissors():
    # ROCK beats SCISSORS
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_classic_scissors_beat_paper():
    # SCISSORS beats PAPER
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_classic_paper_beats_rock():
    # PAPER beats ROCK
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_classic_scissors_lose_to_rock():
    # SCISSORS lose to ROCK
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_classic_paper_lose_to_scissors():
    # PAPER lose to SCISSORS
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_classic_rock_lose_to_paper():
    # ROCK lose to PAPER
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_spock_smashes_scissors():
    # SPOCK beats SCISSORS
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_spock_vaporizes_rock():
    # SPOCK beats ROCK
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_paper_disproves_spock():
    # PAPER beats SPOCK
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_scissors_lose_to_spock():
    # SCISSORS lose to SPOCK
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_rock_lose_to_spock():
    # ROCK lose to SPOCK
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_spock_lose_to_paper():
    # SPOCK lose to PAPER
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # ROCK vs ROCK ties
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # PAPER vs PAPER ties
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # SCISSORS vs SCISSORS ties
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # SPOCK vs SPOCK ties
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_symmetric_verdicts():
    # Testing symmetry: ROCK vs PAPER and PAPER vs ROCK
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"
    
    # Testing symmetry: SCISSORS vs ROCK and ROCK vs SCISSORS
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"
    
    # Testing symmetry: SCISSORS vs PAPER and PAPER vs SCISSORS
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"
    
    # Testing symmetry: SPOCK vs SCISSORS and SCISSORS vs SPOCK
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"
    
    # Testing symmetry: SPOCK vs ROCK and ROCK vs SPOCK
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"
    
    # Testing symmetry: PAPER vs SPOCK and SPOCK vs PAPER
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_move_vocabulary():
    # Test that the moves are exactly ROCK, PAPER, SCISSORS, and SPOCK
    expected_moves = {"ROCK", "PAPER", "SCISSORS", "SPOCK"}
    actual_moves = set(dir(solution))  # Assuming the moves are defined in the solution module
    assert actual_moves == expected_moves

def test_verdict_vocabulary():
    # Test that the verdicts are exactly PLAYER_WINS, PLAYER_LOSES, and TIE
    expected_verdicts = {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}
    actual_verdicts = set(dir(solution))  # Assuming the verdicts are defined in the solution module
    assert actual_verdicts == expected_verdicts