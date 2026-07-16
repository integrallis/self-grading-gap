import pytest
from solution import start_game, tick, change_direction

def test_start_game_valid_grid():
    # Starting a game on a 3x3 grid should place the snake at (0, 0) heading "right", score 0, not over, with food at (1, 0)
    snake, heading, score, game_over, food = start_game(3, 3, [(1, 0)])
    assert snake == [(0, 0)]  # AC-1.1: snake starts at (0, 0)
    assert heading == "right"  # AC-1.1: heading is "right"
    assert score == 0  # AC-1.1: score is 0
    assert not game_over  # AC-1.1: game is not over
    assert food == (1, 0)  # AC-1.1: first food is at (1, 0)

def test_start_game_invalid_grid():
    # Starting a game with non-positive dimensions should raise an error
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        start_game(0, 3, [(1, 0)])  # AC-1.2: width 0 is invalid
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        start_game(3, -1, [(1, 0)])  # AC-1.2: height -1 is invalid

def test_tick_moves_snake():
    # Given a game with a snake at (0, 0) heading "right", ticking should move the snake to (1, 0)
    snake, heading, score, game_over, food = start_game(3, 3, [(2, 0)])
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)
    assert snake == [(1, 0)]  # AC-2.1: snake moves to (1, 0)

def test_change_direction():
    # Changing direction to "up" should take effect on the next tick
    snake, heading, score, game_over, food = start_game(3, 3, [(2, 0)])
    change_direction(snake, heading, "up")
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)
    assert snake == [(1, 0)]  # Still at (1, 0) after the first tick
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)
    assert snake == [(1, -1)]  # AC-2.1: snake moves to (1, -1) which is invalid, game should not change

def test_change_direction_opposite():
    # Changing to the opposite direction should be ignored
    snake, heading, score, game_over, food = start_game(3, 3, [(2, 0)])
    change_direction(snake, heading, "left")  # heading is "right", left is opposite
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)
    assert snake == [(1, 0)]  # Should still be moving right

def test_change_direction_invalid():
    # An unrecognized direction should raise an error
    snake, heading, score, game_over, food = start_game(3, 3, [(2, 0)])
    with pytest.raises(ValueError, match="unknown direction: 'north'"):
        change_direction(snake, heading, "north")  # AC-2.4: invalid direction

def test_eating_food():
    # The snake should grow and increase score when it eats food
    snake, heading, score, game_over, food = start_game(3, 3, [(1, 0), (2, 0)])
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Move to food at (1, 0)
    assert snake == [(1, 0), (0, 0)]  # Snake grows to 2 segments
    assert score == 1  # Score increases by 1
    assert food == (2, 0)  # Next food is now at (2, 0)

def test_food_appears_correctly():
    # New food should not appear on the snake's body
    snake, heading, score, game_over, food = start_game(3, 3, [(0, 0), (1, 0), (2, 0)])
    assert food == (1, 0)  # First food at (1, 0)
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Eat food
    assert food == (2, 0)  # Next food at (2, 0)
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Eat food again
    assert food is None  # No more food after the last one

def test_end_game_collision_with_self():
    # Colliding with itself should end the game
    snake, heading, score, game_over, food = start_game(3, 3, [(1, 0), (0, 0)])
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Move to (1, 0) where it already is
    assert game_over  # Game should be over

def test_end_game_collision_with_wall():
    # Moving out of bounds should end the game
    snake, heading, score, game_over, food = start_game(3, 3, [(1, 0)])
    change_direction(snake, heading, "up")  # Try to move out of bounds
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)
    assert game_over  # Game should be over

def test_no_change_after_game_over():
    # After game over, the state should not change
    snake, heading, score, game_over, food = start_game(3, 3, [(1, 0)])
    change_direction(snake, heading, "up")
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Game over
    old_state = (snake, heading, score, game_over)
    snake, heading, score, game_over, food = tick(snake, heading, score, game_over)  # Try to tick again
    assert (snake, heading, score, game_over) == old_state  # State should remain unchanged