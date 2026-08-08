import pytest
from solution import start_game, tick, change_heading

# US-1: Starting a game on a valid grid
def test_start_game_valid_grid():
    game = start_game(3, 2, [(1, 1)])
    # New game: snake at (0, 0), heading "right", score 0, not over, food at (1, 1)
    assert game['snake'] == [(0, 0)]
    assert game['heading'] == "right"
    assert game['score'] == 0
    assert not game['game_over']
    assert game['food'] == (1, 1)

def test_start_game_invalid_grid():
    with pytest.raises(Exception) as exc_info:
        start_game(0, 2, [(1, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as exc_info:
        start_game(3, 0, [(1, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as exc_info:
        start_game(-1, 2, [(1, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as exc_info:
        start_game(2, -2, [(1, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

def test_start_game_one_by_one_grid():
    game = start_game(1, 1, [(1, 1)])
    # Initial state: snake occupies (0, 0), heading "right", score 0, food is None
    assert game['snake'] == [(0, 0)]
    assert game['heading'] == "right"
    assert game['score'] == 0
    assert not game['game_over']
    assert game['food'] is None
    tick(game)  # First tick should be fatal
    assert game['game_over']

def test_setup_food_skips_snake():
    game = start_game(3, 3, [(0, 0), (1, 0)])  # Food at (0, 0) is occupied
    # Food should appear at (1, 0)
    assert game['food'] == (1, 0)

# US-2: Steering the snake tick by tick
def test_tick_advance_snake():
    game = start_game(3, 3, [(1, 1)])
    tick(game)  # Move right to (1, 0)
    assert game['snake'] == [(1, 0)]
    tick(game)  # Move right to (2, 0)
    assert game['snake'] == [(2, 0)]

def test_change_heading():
    game = start_game(3, 3, [(1, 1)])
    change_heading(game, "down")
    tick(game)  # Move down to (0, 1)
    assert game['snake'] == [(0, 1)]
    
    change_heading(game, "left")  # Attempt to turn left, should not move yet
    tick(game)  # Move down to (1, 1) - wall collision
    assert game['game_over']
    assert game['snake'] == [(0, 1)]  # Snake should not have moved

def test_opposite_heading_ignored():
    game = start_game(3, 3, [(1, 1)])
    change_heading(game, "down")
    change_heading(game, "up")  # Should be ignored
    tick(game)  # Move down to (0, 1)
    assert game['snake'] == [(0, 1)]

def test_unknown_heading():
    game = start_game(3, 3, [(1, 1)])
    with pytest.raises(Exception) as exc_info:
        change_heading(game, "north")
    assert str(exc_info.value) == "unknown direction: 'north'"

# US-3: Eating food, growing, and scoring
def test_eating_food():
    game = start_game(3, 3, [(1, 1), (2, 2)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    change_heading(game, "down")  # Change heading to down
    tick(game)  # Move down to (1, 1) - eat food
    assert game['snake'] == [(1, 1), (1, 0)]  # Grown snake
    assert game['score'] == 1  # Score increased
    assert game['food'] == (2, 2)  # Next food position

def test_growth_and_scoring():
    game = start_game(3, 3, [(1, 1), (2, 2)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    change_heading(game, "down")  # Change heading to down
    tick(game)  # Move down to (1, 1) - eat food
    tick(game)  # Move down to (1, 2) - no food
    assert game['snake'] == [(1, 1), (1, 0), (1, 2)]  # Grown snake
    assert game['score'] == 1  # Score after first food
    assert game['food'] == (2, 2)  # Next food position

    tick(game)  # Move down to (1, 3) - no food
    tick(game)  # Move right to (2, 3) - no food
    tick(game)  # Move right to (3, 3) - food at (2, 2)
    tick(game)  # Eat food at (2, 2)
    assert game['snake'] == [(2, 2), (1, 1), (1, 0), (1, 2)]  # Grown snake
    assert game['score'] == 2  # Score after second food
    assert game['food'] is None  # No more food

def test_no_food_left():
    game = start_game(3, 3, [(1, 1)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    change_heading(game, "down")  # Change heading to down
    tick(game)  # Move down to (1, 1) - eat food
    assert game['food'] is None  # No food left

# US-4: Ending the game on collisions
def test_game_over_edge_collision():
    game = start_game(2, 2, [(1, 1)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    tick(game)  # Move down to (1, 1)
    tick(game)  # Attempt to move right to (1, 2) - should not apply
    assert game['game_over']
    assert game['snake'] == [(1, 1)]  # Snake should be unchanged

def test_game_over_self_collision():
    game = start_game(3, 3, [(1, 1), (1, 2)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 1) - eat food
    tick(game)  # Move down to (1, 2)
    change_heading(game, "up")
    tick(game)  # Move up to (1, 1) - self collision
    assert game['game_over']
    assert game['snake'] == [(1, 1)]

def test_tail_chasing():
    game = start_game(3, 3, [(1, 1)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    change_heading(game, "down")
    tick(game)  # Move down to (1, 1) - eat food
    change_heading(game, "down")
    tick(game)  # Move down to (2, 1)
    change_heading(game, "left")
    tick(game)  # Move left to (2, 0)
    change_heading(game, "up")
    tick(game)  # Move up to (1, 0) - tail chasing allowed
    assert game['snake'] == [(1, 0), (1, 1)]

def test_game_over_no_change_after_game_over():
    game = start_game(3, 3, [(1, 1)])  # Food at (1, 1)
    tick(game)  # Move right to (1, 0)
    change_heading(game, "down")  # Change heading to down
    tick(game)  # Move down to (1, 1) - eat food
    tick(game)  # Move down to (1, 2) - no food
    tick(game)  # Move right to edge (2, 2) - game over
    assert game['game_over']
    snake_snapshot = game['snake'][:]
    score_snapshot = game['score']
    
    tick(game)  # No change after game over
    assert game['snake'] == snake_snapshot  # Snake remains the same
    assert game['score'] == score_snapshot  # Score remains the same