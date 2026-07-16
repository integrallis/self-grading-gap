# test_snake_arcade_engine.py

import pytest
from solution import start_game, tick, change_heading

def test_start_game_valid_grid():
    # Starting a game on a 3x3 grid should initialize the snake at (0, 0) heading "right"
    # with score 0, not over, and food at (0, 1).
    game_state = start_game(3, 3, [(0, 1)])
    assert game_state['snake'] == [(0, 0)]
    assert game_state['heading'] == 'right'
    assert game_state['score'] == 0
    assert game_state['game_over'] is False
    assert game_state['food'] == (0, 1)

def test_start_game_invalid_grid_negative_width():
    # Attempting to start a game on a grid with negative width should raise an error.
    with pytest.raises(Exception) as exc_info:
        start_game(-1, 3, [(0, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_negative_height():
    # Attempting to start a game on a grid with negative height should raise an error.
    with pytest.raises(Exception) as exc_info:
        start_game(3, -1, [(0, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_zero_width():
    # Attempting to start a game on a grid with zero width should raise an error.
    with pytest.raises(Exception) as exc_info:
        start_game(0, 3, [(0, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

def test_start_game_invalid_grid_zero_height():
    # Attempting to start a game on a grid with zero height should raise an error.
    with pytest.raises(Exception) as exc_info:
        start_game(3, 0, [(0, 1)])
    assert str(exc_info.value) == "grid dimensions must be positive"

def test_tick_moves_snake_forward():
    # Starting a game and ticking should move the snake from (0, 0) to (1, 0).
    game_state = start_game(3, 3, [(0, 1)])
    game_state = tick(game_state)
    assert game_state['snake'] == [(1, 0)]  # Snake should move to (1, 0)

def test_tick_with_heading_change():
    # Change heading to "down" and tick; snake should move accordingly.
    game_state = start_game(3, 3, [(0, 1)])
    game_state = change_heading(game_state, 'down')
    game_state = tick(game_state)
    assert game_state['snake'] == [(0, 1), (0, 0)]  # Snake should now be at (0, 1)

def test_tick_ignores_opposite_heading():
    # Change heading to "left", which is opposite of the current "right" heading; it should be ignored.
    game_state = start_game(3, 3, [(0, 1)])
    game_state = change_heading(game_state, 'left')
    game_state = tick(game_state)
    assert game_state['heading'] == 'right'  # Heading should remain "right"

def test_tick_with_invalid_heading():
    # Changing to an unknown direction should raise an error.
    game_state = start_game(3, 3, [(0, 1)])
    with pytest.raises(Exception) as exc_info:
        change_heading(game_state, 'north')
    assert str(exc_info.value) == "unknown direction: 'north'"

def test_eating_food_grows_snake_and_scores():
    # After eating food, the snake should grow and score should increase.
    game_state = start_game(3, 3, [(1, 0), (2, 0)])
    game_state = tick(game_state)  # Move to (1, 0), eat food
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake grows to 2 segments
    assert game_state['score'] == 1  # Score should be 1
    assert game_state['food'] == (2, 0)  # Next food should be at (2, 0)

def test_no_food_after_exhaustion():
    # After all food is eaten, the snake should continue moving without food.
    game_state = start_game(3, 3, [(1, 0)])  # Only one food
    game_state = tick(game_state)  # Eat food
    game_state = tick(game_state)  # Continue moving
    assert game_state['food'] is None  # No food should be present
    assert game_state['snake'] == [(2, 0), (1, 0)]  # Snake should now be at (2, 0)

def test_multi_segment_snake_moving_away_from_food():
    # A multi-segment snake should move forward and drop its old tail cell when moving away from food.
    game_state = start_game(3, 3, [(0, 1), (1, 1)])
    game_state = tick(game_state)  # Move to (0, 1), eat food
    game_state = tick(game_state)  # Move to (1, 1), which is food
    assert game_state['snake'] == [(1, 1), (0, 1)]  # Snake should now be at (1, 1)
    assert game_state['score'] == 1  # Score should be 1

def test_game_over_on_wall_collision():
    # Moving past the wall should end the game.
    game_state = start_game(1, 1, [(0, 0)])  # Minimal grid, snake occupies (0,0)
    game_state = tick(game_state)  # This should trigger game over
    assert game_state['game_over'] is True  # Game should be over
    assert game_state['snake'] == [(0, 0)]  # Snake should not move

def test_game_over_on_self_collision():
    # Snake should end the game if it collides with itself.
    game_state = start_game(3, 3, [(1, 0), (0, 1), (0, 0)])
    game_state = tick(game_state)  # Move to (1, 0), which is occupied
    game_state = change_heading(game_state, 'down')  # Now head to (0, 0)
    game_state = tick(game_state)  # This should trigger self-collision
    assert game_state['game_over'] is True  # Game should be over

def test_no_changes_after_game_over():
    # Once the game is over, further ticks should not change the game state.
    game_state = start_game(1, 1, [(0, 0)])  # Minimal grid
    game_state = tick(game_state)  # This should trigger game over
    previous_snake = game_state['snake'][:]
    previous_score = game_state['score']
    previous_game_over = game_state['game_over']
    
    game_state = tick(game_state)  # Attempt to tick again
    
    assert game_state['snake'] == previous_snake  # State should remain unchanged
    assert game_state['score'] == previous_score  # Score should remain unchanged
    assert game_state['game_over'] == previous_game_over  # Game over state should remain unchanged

def test_food_skipped_at_start():
    # Food at (0, 0) should be skipped during setup because the initial snake occupies it.
    game_state = start_game(3, 3, [(0, 0), (0, 1)])
    assert game_state['food'] == (0, 1)  # The first food is at (0, 1)

def test_food_skipped_later():
    # Later supplied food positions occupied by a grown snake should be skipped.
    game_state = start_game(3, 3, [(1, 0), (0, 0)])
    game_state = tick(game_state)  # Move to (1, 0), eat food
    assert game_state['food'] == (2, 0)  # Next food is at (2, 0)
    game_state = tick(game_state)  # Move to (2, 0), eat food
    assert game_state['food'] is None  # No food should be present

def test_repeated_food_eating():
    # Eating multiple food items should grow the snake and increase the score for each.
    game_state = start_game(3, 3, [(1, 0), (2, 0)])
    game_state = tick(game_state)  # Move to (1, 0), eat food
    assert game_state['snake'] == [(1, 0), (0, 0)]
    assert game_state['score'] == 1
    game_state = tick(game_state)  # Move to (2, 0), eat food
    assert game_state['snake'] == [(2, 0), (1, 0), (0, 0)]
    assert game_state['score'] == 2

def test_opposite_heading_ignored_for_multi_segment_snake():
    # An opposite heading change for a multi-segment snake should be ignored.
    game_state = start_game(3, 3, [(1, 0), (0, 0)])
    game_state = change_heading(game_state, 'left')  # Opposite to "right"
    game_state = tick(game_state)  # Move to (1, 0)
    assert game_state['snake'] == [(1, 0), (0, 0)]  # Snake remains unchanged
    assert game_state['heading'] == 'right'  # Heading should remain "right"

def test_tail_chasing():
    # The head should be able to enter the tail cell being vacated the same tick.
    game_state = start_game(3, 3, [(1, 0), (0, 0)])
    game_state = tick(game_state)  # Move to (1, 0), eat food
    game_state = tick(game_state)  # Move to (2, 0)
    game_state = change_heading(game_state, 'left')  # Move towards the tail
    game_state = tick(game_state)  # Head enters the tail at (1, 0)
    assert game_state['snake'] == [(2, 0), (1, 0)]
    assert game_state['game_over'] is False  # Game should not be over