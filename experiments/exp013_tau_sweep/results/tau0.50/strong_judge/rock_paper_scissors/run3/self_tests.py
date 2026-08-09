from solution import judge_round

def test_rock_beats_scissors():
    # Rock against scissors is a win for the player.
    assert judge_round("ROCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_lose_to_rock():
    # Scissors against rock is a loss for the player.
    assert judge_round("SCISSORS", "ROCK") == "PLAYER_LOSES"

def test_scissors_beats_paper():
    # Scissors against paper is a win for the player.
    assert judge_round("SCISSORS", "PAPER") == "PLAYER_WINS"

def test_paper_lose_to_scissors():
    # Paper against scissors is a loss for the player.
    assert judge_round("PAPER", "SCISSORS") == "PLAYER_LOSES"

def test_paper_beats_rock():
    # Paper against rock is a win for the player.
    assert judge_round("PAPER", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_paper():
    # Rock against paper is a loss for the player.
    assert judge_round("ROCK", "PAPER") == "PLAYER_LOSES"

def test_spock_smashes_scissors():
    # Spock against scissors is a win for the player.
    assert judge_round("SPOCK", "SCISSORS") == "PLAYER_WINS"

def test_scissors_lose_to_spock():
    # Scissors against Spock is a loss for the player.
    assert judge_round("SCISSORS", "SPOCK") == "PLAYER_LOSES"

def test_spock_vaporizes_rock():
    # Spock against rock is a win for the player.
    assert judge_round("SPOCK", "ROCK") == "PLAYER_WINS"

def test_rock_lose_to_spock():
    # Rock against Spock is a loss for the player.
    assert judge_round("ROCK", "SPOCK") == "PLAYER_LOSES"

def test_paper_disproves_spock():
    # Paper against Spock is a win for the player.
    assert judge_round("PAPER", "SPOCK") == "PLAYER_WINS"

def test_spock_lose_to_paper():
    # Spock against paper is a loss for the player.
    assert judge_round("SPOCK", "PAPER") == "PLAYER_LOSES"

def test_identical_moves_tie_rock():
    # Rock against rock ties.
    assert judge_round("ROCK", "ROCK") == "TIE"

def test_identical_moves_tie_paper():
    # Paper against paper ties.
    assert judge_round("PAPER", "PAPER") == "TIE"

def test_identical_moves_tie_scissors():
    # Scissors against scissors ties.
    assert judge_round("SCISSORS", "SCISSORS") == "TIE"

def test_identical_moves_tie_spock():
    # Spock against spock ties.
    assert judge_round("SPOCK", "SPOCK") == "TIE"

def test_all_pairings():
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

def test_move_vocabulary():
    # The moves must be exactly ROCK, PAPER, SCISSORS, and SPOCK.
    from solution import MOVES
    assert MOVES == {"ROCK", "PAPER", "SCISSORS", "SPOCK"}

def test_verdict_vocabulary():
    # The verdicts must be exactly PLAYER_WINS, PLAYER_LOSES, and TIE.
    from solution import VERDICTS
    assert VERDICTS == {"PLAYER_WINS", "PLAYER_LOSES", "TIE"}