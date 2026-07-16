import pytest
from solution import start_game, tick, change_direction

def test_start_game_valid_grid():
    # Starting a game on a 5x5 grid
    game_state = start_game(5, 5, [(1, 1), (2, 2)])
    assert game_state['snake'] == [(0, 0)]  # AC-1.1: Snake starts at (0, 0)
    assert game_state['heading'] == 'right'  # AC-1.1: Initial heading is "right"
    assert game_state['score'] == 0  # AC-1.1: Initial score is 0
    assert not game_state['game_over']  # AC-1.1: Game is not over
    assert game_state['food'] == (1, 1)  # AC-1.1: First food is at (1, 1)

def test_start_game_invalid_grid_zero_width():
    with pytest.raises(Exception) as excinfo:
        start_game(0, 5, [(0, 0)])
    assert str(excinfo.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_zero_height():
    with pytest.raises(Exception) as excinfo:
        start_game(5, 0, [(0, 0)])
    assert str(excinfo.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_negative_dimension():
    with pytest.raises(Exception) as excinfo:
        start_game(-1, 5, [(0, 0)])
    assert str(excinfo.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_negative_height():
    with pytest.raises(Exception) as excinfo:
        start_game(5, -1, [(0, 0)])
    assert str(excinfo.value) == "grid dimensions must be positive"

def test_tick_moves_snake_forward():
    # Starting a game on a 5x5 grid with food at (1, 1)
    game_state = start_game(5, 5, [(1, 1)])
    game_state = tick(game_state)  # First tick
    assert game_state['snake'] == [(1, 0)]  # AC-2.1: Head moves to (1, 0)
    assert game_state['food'] == (1, 1)  # Food remains at (1, 1)

def test_change_direction_effect_on_next_tick():
    # Starting a game
    game_state = start_game(5, 5, [(1, 1)])
    game_state = change_direction(game_state, 'down')
    game_state = tick(game_state)  # First tick after direction change
    assert game_state['snake'] == [(0, 1)]  # AC-2.2: Head moves down to (0, 1)

def test_change_direction_effect_on_next_tick_up():
    # Starting a game
    game_state = start_game(5, 5, [(1, 1)])
    game_state = change_direction(game_state, 'up')
    game_state = tick(game_state)  # First tick after direction change
    assert game_state['snake'] == [(0, -1)]  # AC-2.2: Head moves up to (0, -1)

def test_change_direction_effect_on_next_tick_left():
    # Starting a game
    game_state = start_game(5, 5, [(1, 1)])
    game_state = change_direction(game_state, 'left')
    game_state = tick(game_state)  # First tick after direction change
    assert game_state['snake'] == [(-1, 0)]  # AC-2.2: Head moves left to (-1, 0)

def test_change_direction_effect_on_next_tick_right():
    # Starting a game
    game_state = start_game(5, 5, [(1, 1)])
    game_state = change_direction(game_state, 'right')
    game_state = tick(game_state)  # First tick after direction change
    assert game_state['snake'] == [(1, 1)]  # AC-2.2: Head remains at (1, 1)

def test_change_direction_ignored_opposite():
    # Starting a game
    game_state = start_game(5, 5, [(1, 1)])
    game_state = change_direction(game_state, 'down')
    game_state = change_direction(game_state, 'up')  # Ignored
    game_state = tick(game_state)  # First tick
    assert game_state['snake'] == [(0, 1)]  # AC-2.3: Still moving down to (0, 1)

def test_change_direction_invalid_direction():
    game_state = start_game(5, 5, [(1, 1)])
    with pytest.raises(Exception) as excinfo:
        change_direction(game_state, 'north')
    assert str(excinfo.value) == "unknown direction: 'north'"

def test_start_game_food_skipped():
    game_state = start_game(5, 5, [(0, 0), (1, 1)])  # Food starts at (0, 0)
    assert game_state['food'] == (1, 1)  # Should skip (0, 0) and move to (1, 1)

def test_eating_food_grows_snake_and_scores():
    game_state = start_game(5, 5, [(1, 1), (2, 2)])
    game_state = tick(game_state)  # Move to (1, 0)
    game_state = change_direction(game_state, 'down')  # Prepare to eat food at (1, 1)
    game_state = tick(game_state)  # Move to (1, 1) and eat food
    assert game_state['snake'] == [(1, 1), (1, 0)]  # AC-3.2: Snake grows to 2 segments
    assert game_state['score'] == 1  # AC-3.2: Score increases to 1
    assert game_state['food'] == (2, 2)  # AC-3.2: Next food is at (2, 2)

def test_eating_multiple_foods_accumulates_growth_and_score():
    game_state = start_game(5, 5, [(1, 1), (2, 2), (3, 3)])
    game_state = tick(game_state)  # Move to (1, 0)
    game_state = change_direction(game_state, 'down')  # Prepare to eat food at (1, 1)
    game_state = tick(game_state)  # Move to (1, 1) and eat food
    assert game_state['snake'] == [(1, 1), (1, 0)]  # AC-3.2: Snake grows to 2 segments
    assert game_state['score'] == 1  # AC-3.2: Score increases to 1
    game_state = tick(game_state)  # Move to (1, 2)
    game_state = change_direction(game_state, 'down')  # Prepare to eat food at (2, 2)
    game_state = tick(game_state)  # Move to (2, 2) and eat food
    assert game_state['snake'] == [(2, 2), (1, 1), (1, 0)]  # AC-3.2: Snake grows to 3 segments
    assert game_state['score'] == 2  # AC-3.2: Score increases to 2
    assert game_state['food'] == (3, 3)  # AC-3.2: Next food is at (3, 3)

def test_no_food_after_sequence_runs_out():
    game_state = start_game(5, 5, [(1, 1), (2, 2)])
    game_state = tick(game_state)  # Move to (1, 0)
    game_state = change_direction(game_state, 'down')  # Prepare to eat food
    game_state = tick(game_state)  # Move to (1, 1) and eat food
    game_state = tick(game_state)  # Move to (1, 2) where no food is
    assert game_state['food'] == (2, 2)  # AC-3.4: Food should still be at (2, 2)

def test_game_over_on_edge_collision():
    game_state = start_game(1, 1, [(0, 0)])  # 1x1 grid
    game_state = tick(game_state)  # Moves into edge
    assert game_state['game_over']  # AC-4.1: Game should be over
    assert game_state['snake'] == [(0, 0)]  # Snake remains unchanged after fatal move

def test_game_over_on_self_collision():
    game_state = start_game(5, 5, [(1, 1)])
    game_state = tick(game_state)  # Move to (1, 0)
    game_state = change_direction(game_state, 'down')  # Move to (1, 1) and eat food
    game_state = tick(game_state)  # Move to (1, 1) and eat food
    game_state = change_direction(game_state, 'right')  # Move to (2, 1)
    game_state = tick(game_state)  # Move to (2, 1)
    game_state = change_direction(game_state, 'up')  # Change direction to up
    game_state = tick(game_state)  # Move to (2, 0)
    game_state = change_direction(game_state, 'left')  # Prepare to self-collide
    game_state = tick(game_state)  # Move to (1, 0) -> self-collision
    assert not game_state['game_over']  # AC-4.2: Game should not be over

def test_tick_no_change_after_game_over():
    game_state = start_game(1, 1, [(0, 0)])  # 1x1 grid
    game_state = tick(game_state)  # Game over
    previous_snake = list(game_state['snake'])  # Snapshot the snake
    previous_score = game_state['score']
    previous_game_over = game_state['game_over']
    game_state = tick(game_state)  # Another tick
    assert game_state['snake'] == previous_snake  # AC-4.4: Snake should remain unchanged
    assert game_state['score'] == previous_score  # Score should remain unchanged
    assert game_state['game_over'] == previous_game_over  # Game over state should remain unchanged