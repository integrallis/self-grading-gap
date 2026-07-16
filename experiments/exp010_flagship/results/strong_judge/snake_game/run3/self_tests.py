# test_snake_arcade_engine.py

import pytest
from solution import game_engine  # Assuming the public API is named game_engine

def test_starting_a_game_on_a_valid_grid():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    assert game.snake == [(0, 0)]  # AC-1.1: snake starts at (0, 0)
    assert game.heading == "right"  # AC-1.1: initial heading is "right"
    assert game.score == 0  # AC-1.1: initial score is 0
    assert not game.is_over  # AC-1.1: game is not over
    assert game.food == (1, 1)  # AC-1.1: first food is at (1, 1)

def test_invalid_grid_dimensions():
    with pytest.raises(Exception, match="grid dimensions must be positive"):
        game_engine(width=0, height=5, food=[(1, 1)])  # AC-1.2
    with pytest.raises(Exception, match="grid dimensions must be positive"):
        game_engine(width=5, height=0, food=[(1, 1)])  # AC-1.2
    with pytest.raises(Exception, match="grid dimensions must be positive"):
        game_engine(width=-1, height=5, food=[(1, 1)])  # AC-1.2
    with pytest.raises(Exception, match="grid dimensions must be positive"):
        game_engine(width=5, height=-1, food=[(1, 1)])  # AC-1.2
    # Test a valid 1x1 grid
    game = game_engine(width=1, height=1, food=[(0, 0)])
    assert game.snake == [(0, 0)]  # Snake occupies the only cell
    game.tick()  # First tick
    assert game.is_over  # Game should be over after the first tick

def test_steering_the_snake_tick_by_tick():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    
    # AC-2.1: Snake moves right
    game.tick()  # Move to (1, 0)
    assert game.snake == [(1, 0)]  # Head at (1, 0)
    
    # AC-2.2: Change heading to down
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    assert game.snake == [(1, 1), (1, 0)]  # Snake grows by one segment
    
    # AC-2.3: Ignore opposite heading
    game.change_heading("up")  # This should be ignored
    game.tick()  # Move to (1, 2)
    assert game.snake == [(1, 2), (1, 1)]  # Head at (1, 2), tail follows
    
    # AC-2.4: Unrecognized heading
    with pytest.raises(Exception, match="unknown direction: 'north'"):
        game.change_heading("north")

def test_eating_food_growing_and_scoring():
    game = game_engine(width=5, height=5, food=[(1, 1), (1, 2)])
    assert game.score == 0  # Initial score
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1), eat food
    assert game.score == 1  # Score increases by 1
    assert game.snake == [(1, 1), (1, 0)]  # Snake grows by one segment
    assert game.food == (1, 2)  # Next food should be (1, 2)
    
    game.tick()  # Move to (1, 2), eat food
    assert game.score == 2  # Score increases by 1
    assert game.snake == [(1, 2), (1, 1), (1, 0)]  # Snake grows by one segment
    game.tick()  # Move to (1, 3)
    assert game.food is None  # No more food available

def test_ending_the_game_on_collisions():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    
    # Move the snake to a position where it runs into itself
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    game.change_heading("left")
    game.tick()  # Move to (0, 1)
    game.change_heading("down")
    game.tick()  # Move to (0, 2)
    game.change_heading("right")
    game.tick()  # Move to (1, 2)
    
    # Now the snake will run into itself
    game.change_heading("up")
    game.tick()  # Move into its own body
    assert game.is_over  # Game should be over

    # Further ticks change nothing
    game.tick()
    assert game.snake == [(1, 2), (0, 1), (1, 1)]  # Snake remains the same
    assert game.score == 1  # Score remains the same
    assert game.is_over  # Game still over

def test_wall_collision():
    game = game_engine(width=5, height=5, food=[(4, 4)])
    
    # Move to the edge of the grid and change heading to go out of bounds
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1)
    game.change_heading("down")  # Next is out of bounds
    game.tick()  # This tick should not move
    assert game.snake == [(1, 1), (1, 0)]  # Snake remains unchanged
    assert game.is_over  # Game should be over

def test_self_collision():
    game = game_engine(width=5, height=5, food=[(2, 0)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1)
    game.change_heading("right")
    game.tick()  # Move to (2, 1)
    game.change_heading("up")
    game.tick()  # Move to (2, 0), eat food
    game.change_heading("left")
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1)
    game.change_heading("left")
    game.tick()  # Move to (0, 1)

    game.change_heading("down")  # Move into its own body
    game.tick()  # This tick should not move
    assert game.snake == [(0, 1), (1, 1), (2, 1)]  # Snake remains unchanged
    assert game.is_over  # Game should be over

def test_food_skipping():
    game = game_engine(width=5, height=5, food=[(0, 0), (1, 1), (2, 2)])
    assert game.snake == [(0, 0)]  # Initial position occupied by snake
    assert game.food == (1, 1)  # Food should be at (1, 1) after setup
    game.tick()  # Snake moves to (1, 0), first tick is safe
    assert not game.is_over  # Game should still be active
    game.tick()  # Move to (1, 1), eat food
    assert game.food == (2, 2)  # Next food should be (2, 2)

def test_exhausted_food_sequence():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1), eat food
    assert game.score == 1  # Score increases by 1
    assert game.food is None  # No more food available
    game.tick()  # Move to (1, 2)
    assert game.snake == [(1, 2), (1, 1), (1, 0)]  # Snake remains same length
    assert game.score == 1  # Score remains the same

def test_tail_chasing():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    game.change_heading("left")
    game.tick()  # Move to (0, 1)
    game.change_heading("down")
    game.tick()  # Move to (0, 2)
    game.change_heading("right")
    game.tick()  # Move to (1, 2)
    game.change_heading("left")
    game.tick()  # Move to (0, 2)
    game.change_heading("down")
    game.tick()  # Move to (0, 3)
    game.change_heading("up")
    game.tick()  # Move into the cell vacated by tail, still active
    assert not game.is_over  # Game should still be active

def test_opposite_heading_ignored():
    game = game_engine(width=5, height=5, food=[(1, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("left")  # Opposite heading
    game.tick()  # Should still be at (1, 1)
    assert game.snake == [(1, 1), (1, 0)]  # Snake should not change heading

def test_food_skipped_if_occupied_after_growth():
    game = game_engine(width=5, height=5, food=[(1, 1), (1, 2)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1), eat food
    game.tick()  # Move to (1, 2), but it is occupied by the snake
    assert game.food == (1, 2)  # Next food should be (1, 2) but is skipped
    game.tick()  # Move to (1, 3)
    assert game.food is None  # No more food available