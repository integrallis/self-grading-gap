# test_solution.py

from solution import judge_round

def test_rock_beats_scissors():
    # Rock (PLAYER) beats Scissors (OPPONENT)
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_beats_paper():
    # Scissors (PLAYER) beats Paper (OPPONENT)
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_beats_rock():
    # Paper (PLAYER) beats Rock (OPPONENT)
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_spock_smashes_scissors():
    # Spock (PLAYER) beats Scissors (OPPONENT)
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_spock_vaporizes_rock():
    # Spock (PLAYER) beats Rock (OPPONENT)
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_paper_disproves_spock():
    # Paper (PLAYER) beats Spock (OPPONENT)
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_scissors_lose_to_rock():
    # Scissors (PLAYER) lose to Rock (OPPONENT)
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_paper_lose_to_scissors():
    # Paper (PLAYER) lose to Scissors (OPPONENT)
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_rock_lose_to_paper():
    # Rock (PLAYER) lose to Paper (OPPONENT)
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_scissors_lose_to_spock():
    # Scissors (PLAYER) lose to Spock (OPPONENT)
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_rock_lose_to_spock():
    # Rock (PLAYER) lose to Spock (OPPONENT)
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_spock_lose_to_paper():
    # Spock (PLAYER) lose to Paper (OPPONENT)
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # Rock (PLAYER) ties with Rock (OPPONENT)
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # Paper (PLAYER) ties with Paper (OPPONENT)
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # Scissors (PLAYER) ties with Scissors (OPPONENT)
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # Spock (PLAYER) ties with Spock (OPPONENT)
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_symmetric_verdicts():
    # Testing symmetric verdicts for each pairing
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

    assert judge_round("PAPER", "SPOCK") == "PLAYER_LOSES"
    assert judge_round("SPOCK", "PAPER") == "PLAYER_WINS"