import pytest
from solution import SnakeGame

def test_starting_game_valid_grid():
    game = SnakeGame(5, 5, [(1, 1), (2, 2)])
    assert game.snake == [(0, 0)]  # Starting position
    assert game.heading == "right"  # Initial heading
    assert game.score == 0  # Initial score
    assert not game.is_over  # Game is not over
    assert game.food == (1, 1)  # First food position

def test_starting_game_invalid_grid_width():
    game = SnakeGame(0, 5, [(1, 1)])
    assert game == "grid dimensions must be positive"

def test_starting_game_invalid_grid_height():
    game = SnakeGame(5, 0, [(1, 1)])
    assert game == "grid dimensions must be positive"

def test_starting_game_invalid_grid_both():
    game = SnakeGame(0, 0, [(1, 1)])
    assert game == "grid dimensions must be positive"

def test_starting_game_valid_grid_one_by_one():
    game = SnakeGame(1, 1, [(0, 0)])
    assert game.snake == [(0, 0)]  # Snake fills the grid
    game.tick()  # First tick should be fatal
    assert game.is_over  # Game is over after first tick

def test_steering_snake_tick():
    game = SnakeGame(5, 5, [(1, 1)])
    game.tick()  # Move to (1, 0)
    assert game.snake == [(1, 0)]  # New position
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    assert game.snake == [(1, 1), (1, 0)]  # Snake grows
    assert game.food == (2, 2)  # Next food position
    game.change_heading("left")
    game.tick()  # Move to (0, 1)
    assert game.snake == [(0, 1), (1, 1)]  # New position

def test_steering_snake_invalid_direction():
    game = SnakeGame(5, 5, [(1, 1)])
    assert game.change_heading("north") == "unknown direction: 'north'"

def test_steering_snake_opposite_direction():
    game = SnakeGame(5, 5, [(1, 1)])
    game.change_heading("left")  # Attempt to change direction
    game.tick()  # Move to (1, 0)
    game.change_heading("right")  # Opposite direction, should be ignored
    game.tick()  # Should still go left
    assert game.snake == [(1, 0)]  # Position should not change

def test_steering_snake_opposite_direction_multi_segment():
    game = SnakeGame(5, 5, [(1, 1), (1, 0)])
    game.change_heading("down")  # Move to (1, 1)
    game.tick()  # Move to (1, 1), eat food
    game.change_heading("up")  # Attempt to reverse direction
    game.tick()  # Should still go down
    assert game.snake == [(1, 1), (1, 0)]  # Position should not change

def test_eating_food_growth():
    game = SnakeGame(5, 5, [(1, 1), (2, 2)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    assert game.snake == [(1, 1), (1, 0)]  # Snake grows
    assert game.score == 1  # Score increases
    assert game.food == (2, 2)  # Next food position

def test_eating_food_no_more_food():
    game = SnakeGame(5, 5, [(1, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    game.tick()  # Move to (1, 2) with no food
    assert game.food is None  # No food left on board

def test_eating_food_skipped():
    game = SnakeGame(5, 5, [(0, 0), (1, 1), (2, 2)])
    assert game.food == (1, 1)  # Check first food
    game.tick()  # Move to (0, 1)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    assert game.snake == [(1, 1), (0, 1)]  # Snake grows
    assert game.food == (2, 2)  # Next food position

def test_collisions_with_edges():
    game = SnakeGame(5, 5, [(1, 1)])
    game.change_heading("up")  # Attempt to move out of bounds
    game.tick()  # Should not move
    assert game.snake == [(0, 0)]  # Position should not change
    assert game.is_over  # Game should be over

def test_collisions_with_self():
    game = SnakeGame(5, 5, [(1, 1), (1, 0)])
    game.change_heading("down")  # Move into self
    game.tick()  # Should not move
    assert game.snake == [(1, 1), (1, 0)]  # Position should not change
    assert game.is_over  # Game should be over

def test_collisions_with_self_after_growth():
    game = SnakeGame(5, 5, [(1, 1)])
    game.change_heading("down")  # Move to (1, 1), eat food
    game.tick()
    game.change_heading("down")  # Move to (2, 1)
    game.tick()  # Move to (2, 1)
    game.change_heading("up")  # Move to (1, 1)
    game.tick()  # Move into self
    assert game.is_over  # Game should be over

def test_game_over_state_is_final():
    game = SnakeGame(5, 5, [(1, 1)])
    game.change_heading("up")
    game.tick()  # Move out of bounds
    game.tick()  # Further ticks should do nothing
    assert game.snake == [(0, 0)]  # Position should not change
    assert game.score == 0  # Score should not change
    assert game.is_over  # Should still be over

def test_tail_chasing():
    game = SnakeGame(5, 5, [(1, 1), (1, 0)])
    game.change_heading("down")
    game.tick()  # Move to (1, 1), snake grows
    game.change_heading("left")
    game.tick()  # Move to (0, 1)
    game.change_heading("up")
    game.tick()  # Move to (0, 0)
    game.change_heading("down")  # Move to vacated tail
    game.tick()
    assert game.snake == [(0, 0), (0, 1), (1, 1)]  # Snake can enter vacated tail cell