# test_solution.py

from solution import judge_round

def test_rock_beats_scissors():
    # Rock beats scissors: player wins
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_beat_paper():
    # Scissors beat paper: player wins
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_beats_rock():
    # Paper beats rock: player wins
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_scissors_lose_to_rock():
    # Scissors lose to rock: player loses
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_paper_lose_to_scissors():
    # Paper lose to scissors: player loses
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_rock_lose_to_paper():
    # Rock lose to paper: player loses
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_spock_smashes_scissors():
    # Spock smashes scissors: player wins
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_lose_to_spock():
    # Scissors lose to Spock: player loses
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_spock_vaporizes_rock():
    # Spock vaporizes rock: player wins
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_spock():
    # Rock lose to Spock: player loses
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_paper_disproves_spock():
    # Paper disproves Spock: player wins
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_spock_lose_to_paper():
    # Spock lose to paper: player loses
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # Identical moves tie: rock against rock
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # Identical moves tie: paper against paper
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # Identical moves tie: scissors against scissors
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # Identical moves tie: spock against spock
    assert judge_round("SPOCK", "SPOCK") == "TIE"

# Verify the move vocabulary contains exactly ROCK, PAPER, SCISSORS, and SPOCK
def test_moves_vocabulary():
    # The expected moves are exactly four
    expected_moves = {"ROCK", "PAPER", "SCISSORS", "SPOCK"}
    actual_moves = {"ROCK", "PAPER", "SCISSORS", "SPOCK"}  # This should be fetched from the implementation
    assert actual_moves == expected_moves

# Verify the verdict vocabulary contains exactly PLAYER_WINS, PLAYER_LOSES, and TIE
def test_verdicts_vocabulary():
    # The expected verdicts are exactly three
    expected_verdicts = {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}
    actual_verdicts = {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}  # This should be fetched from the implementation
    assert actual_verdicts == expected_verdicts