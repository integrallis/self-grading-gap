import pytest
from solution import start_game, tick, change_heading

def test_start_game_valid_grid():
    # Starting a game on a 3x3 grid should initialize the snake at (0, 0) heading "right", score 0, game not over, food at (0, 1)
    game_state = start_game(3, 3, [(0, 1)])
    assert game_state['snake'] == [(0, 0)]  # Snake starts at (0, 0)
    assert game_state['heading'] == "right"  # Initial heading
    assert game_state['score'] == 0  # Initial score
    assert not game_state['game_over']  # Game is not over
    assert game_state['food'] == (0, 1)  # First food position

def test_start_game_invalid_grid_width():
    # Invalid grid width should raise an error
    with pytest.raises(Exception) as exc:
        start_game(0, 3, [(0, 1)])
    assert str(exc.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_height():
    # Invalid grid height should raise an error
    with pytest.raises(Exception) as exc:
        start_game(3, 0, [(0, 1)])
    assert str(exc.value) == "grid dimensions must be positive"

def test_start_game_one_by_one_grid():
    # A one-by-one grid should have the snake at (0, 0) and food should not be placed, the first tick is fatal
    game_state = start_game(1, 1, [(0, 0)])
    assert game_state['snake'] == [(0, 0)]  # Snake fills the grid
    assert game_state['food'] is None  # No food should be there since it's occupied
    assert not game_state['game_over']  # Game is not over yet
    game_state = tick(game_state)  # First tick should be fatal
    assert game_state['game_over']  # Game is over

def test_tick_moves_snake_forward():
    # Initial state with snake at (0, 0) heading "right", ticking should move snake to (1, 0) and eat food
    game_state = start_game(3, 3, [(1, 0)])
    game_state = tick(game_state)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake grows to [(1, 0), (0, 0)]
    assert game_state['score'] == 1  # Score increases to 1
    assert game_state['food'] is None  # No more food after eating

def test_tick_changes_heading():
    # Change heading to "down" and tick should move snake down to (0, 1) and eat food
    game_state = start_game(3, 3, [(0, 1)])
    change_heading(game_state, "down")
    game_state = tick(game_state)
    assert game_state['snake'] == [(0, 1), (0, 0)]  # Snake grows to [(0, 1), (0, 0)]
    assert game_state['score'] == 1  # Score increases to 1
    assert game_state['food'] == (1, 0)  # Next food position

def test_tick_ignored_opposite_heading():
    # If heading is "right", changing to "left" should be ignored
    game_state = start_game(3, 3, [(1, 0)])
    change_heading(game_state, "left")  # Ignored
    game_state = tick(game_state)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake still moves to (1, 0) and grows

def test_tick_unknown_heading():
    # Changing to an unknown direction should raise an error
    game_state = start_game(3, 3, [(0, 1)])
    with pytest.raises(Exception) as exc:
        change_heading(game_state, "north")
    assert str(exc.value) == "unknown direction: 'north'"

def test_eating_food_grows_snake():
    # After moving to food at (1, 0), snake should grow and score increase
    game_state = start_game(3, 3, [(1, 0), (2, 0)])
    game_state = tick(game_state)  # Move to (1, 0) to eat food
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake grows to 2 segments
    assert game_state['score'] == 1  # Score increases to 1
    assert game_state['food'] == (2, 0)  # Next food position

def test_food_selection_skips_occupied():
    # If food is at a position occupied by the snake, it should skip it
    game_state = start_game(3, 3, [(1, 0), (0, 1)])
    game_state = tick(game_state)  # Move to (1, 0) to eat food
    assert game_state['food'] == (0, 1)  # Food at (0, 1) should be next

def test_no_food_after_all_eaten():
    # After all food is eaten, there should be no food on the board
    game_state = start_game(3, 3, [(1, 0)])
    game_state = tick(game_state)  # Move to eat the food
    game_state = tick(game_state)  # No food left to eat
    assert game_state['food'] is None  # No food on board now
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake remains the same
    assert game_state['score'] == 1  # Score remains the same

def test_game_over_edge_collision():
    # Moving past the grid edge should end the game
    game_state = start_game(1, 1, [])
    game_state = tick(game_state)  # First tick should be fatal
    assert game_state['game_over']  # Game is over
    assert game_state['snake'] == [(0, 0)]  # Snake does not move out of bounds

def test_game_over_self_collision():
    # Snake colliding with itself should end the game
    game_state = start_game(3, 3, [(1, 0)])
    game_state = tick(game_state)  # Move to (1, 0)
    game_state = tick(game_state)  # Move to (2, 0)
    change_heading(game_state, "up")  # Change heading to chase itself
    game_state = tick(game_state)  # Move to (1, 0) again
    assert game_state['game_over']  # Game is over

def test_tick_no_change_after_game_over():
    # After the game is over, further ticks should change nothing
    game_state = start_game(1, 1, [])
    game_state = tick(game_state)  # First tick should be fatal
    last_snake = game_state['snake']
    last_score = game_state['score']
    last_food = game_state['food']
    game_state = tick(game_state)  # Should remain unchanged
    assert game_state['snake'] == last_snake
    assert game_state['score'] == last_score
    assert game_state['food'] == last_food

def test_tick_changes_heading_up():
    # Change heading to "up" from (1, 1) should keep snake in place and game over remains true
    game_state = start_game(3, 3, [(0, 1)])
    change_heading(game_state, "up")
    game_state = tick(game_state)
    assert game_state['snake'] == [(0, 1), (0, 0)]  # Snake remains the same
    assert game_state['score'] == 0  # Score remains 0
    assert game_state['food'] == (0, 1)  # Food remains (0, 1)

def test_tick_changes_heading_left():
    # Change heading to "left" while heading is "right", should be ignored
    game_state = start_game(3, 3, [(1, 0)])
    change_heading(game_state, "left")  # Ignored
    game_state = tick(game_state)  # Should still move to (1, 0)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake still moves to [(1, 0), (0, 0)]

def test_tick_changes_heading_right():
    # Change heading to "right" and tick should move snake right
    game_state = start_game(3, 3, [(0, 0)])
    change_heading(game_state, "right")
    game_state = tick(game_state)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake grows to [(1, 0), (0, 0)]
    assert game_state['score'] == 1  # Score increases to 1
    assert game_state['food'] is None  # No more food after eating

def test_tick_opposite_direction_ignored():
    # Change heading to "left" while heading is "right", should be ignored
    game_state = start_game(3, 3, [(1, 0)])
    change_heading(game_state, "left")  # Ignored
    game_state = tick(game_state)  # Should still move to (1, 0)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake still moves to [(1, 0), (0, 0)]