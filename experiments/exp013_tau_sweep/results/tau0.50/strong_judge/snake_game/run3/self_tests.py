import pytest
from solution import SnakeGame  # Assuming the main class is named SnakeGame

def test_starting_game_on_valid_grid():
    # AC-1.1
    game = SnakeGame(3, 3, [(1, 1)])
    assert game.get_snake() == [(0, 0)]  # Snake starts at (0, 0)
    assert game.get_heading() == "right"  # Initial heading is "right"
    assert game.get_score() == 0  # Initial score is 0
    assert not game.is_game_over()  # Game is not over
    assert game.get_food() == (1, 1)  # First food is at (1, 1)

def test_invalid_grid_dimensions():
    # AC-1.2
    with pytest.raises(Exception) as excinfo:
        SnakeGame(0, 5, [(1, 1)])
    assert str(excinfo.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as excinfo:
        SnakeGame(5, 0, [(1, 1)])
    assert str(excinfo.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as excinfo:
        SnakeGame(-1, 5, [(1, 1)])
    assert str(excinfo.value) == "grid dimensions must be positive"

    with pytest.raises(Exception) as excinfo:
        SnakeGame(5, -1, [(1, 1)])
    assert str(excinfo.value) == "grid dimensions must be positive"

def test_one_by_one_grid():
    # AC-1.2
    game = SnakeGame(1, 1, [(0, 0)])  # Food is at (0, 0), but snake occupies it
    assert game.get_snake() == [(0, 0)]  # Snake occupies the only cell
    assert game.get_score() == 0  # Initial score is 0
    assert not game.is_game_over()  # Game is not over
    game.tick()  # First tick should end the game
    assert game.is_game_over()  # Game should be over

def test_tick_moves_snake():
    # AC-2.1
    game = SnakeGame(3, 3, [(1, 1)])
    game.tick()  # Move snake
    assert game.get_snake() == [(1, 0)]  # Snake should now be at (1, 0)

def test_multi_segment_movement():
    # AC-2.1
    game = SnakeGame(3, 3, [(1, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1), eat food
    game.change_heading("down")
    game.tick()  # Move to (1, 2)
    game.change_heading("down")
    game.tick()  # Attempt to move to (1, 3), should not move beyond grid
    assert game.get_snake() == [(1, 2), (1, 1)]  # Length unchanged
    assert game.get_score() == 1  # Score is 1

def test_change_heading():
    # AC-2.2
    game = SnakeGame(3, 3, [(1, 1)])
    game.change_heading("down")
    game.tick()  # Move snake
    assert game.get_snake() == [(0, 1)]  # Snake should now be at (0, 1)

def test_ignore_opposite_heading():
    # AC-2.3
    game = SnakeGame(3, 3, [(1, 1)])
    game.change_heading("down")  # Change heading to down
    game.tick()  # Move down to (0, 1)
    game.change_heading("up")  # Change to opposite, should be ignored
    game.tick()  # Move down again
    assert game.get_snake() == [(0, 2)]  # Snake should still be moving down

def test_unknown_heading():
    # AC-2.4
    game = SnakeGame(3, 3, [(1, 1)])
    with pytest.raises(Exception) as excinfo:
        game.change_heading("north")
    assert str(excinfo.value) == "unknown direction: 'north'"

def test_eating_food():
    # AC-3.1, AC-3.2
    game = SnakeGame(3, 3, [(1, 1), (2, 0)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1) and eat food
    assert game.get_snake() == [(1, 1), (1, 0)]  # Snake grows head-first
    assert game.get_score() == 1  # Score increases by 1
    assert game.get_food() == (2, 0)  # Next food appears at (2, 0)

def test_food_skips_snake_occupied_positions():
    # AC-3.1
    game = SnakeGame(3, 3, [(0, 0), (1, 1), (2, 2)])
    assert game.get_food() == (1, 1)  # First food should skip (0, 0)

def test_later_food_skips_occupied_by_grown_snake():
    # AC-3.1
    game = SnakeGame(3, 3, [(1, 1), (2, 0), (2, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1) and eat food
    game.change_heading("down")
    game.tick()  # Move to (2, 1)
    game.change_heading("down")
    game.tick()  # Attempt to move down to (3, 1), should not produce food
    assert game.get_food() == (2, 0)  # Should still have food at (2, 0)

def test_multi_food():
    # AC-3.3
    game = SnakeGame(3, 3, [(1, 1), (2, 0), (2, 1)])
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1) and eat food
    game.change_heading("down")
    game.tick()  # Move to (2, 1) and eat food
    assert game.get_snake() == [(2, 1), (1, 1), (1, 0)]  # Grown snake
    assert game.get_score() == 2  # Score is 2 now

def test_no_food_after_all_eaten():
    # AC-3.4
    game = SnakeGame(3, 3, [(1, 1), (2, 2)])
    game.tick()  # Moves to (1, 0)
    game.change_heading("down")
    game.tick()  # Eats food at (1, 1)
    game.change_heading("down")
    game.tick()  # Moves to (2, 1)
    game.change_heading("right")
    game.tick()  # Moves to (2, 2) and eats food
    game.change_heading("down")
    game.tick()  # Attempting to move down now to (3, 2) should not produce food
    assert game.get_food() is None  # No food should be present

def test_collision_with_wall():
    # AC-4.1
    game = SnakeGame(3, 3, [(1, 1)])
    game.change_heading("down")
    game.tick()  # Moves to (1, 1)
    game.change_heading("down")  # Change heading to down
    game.tick()  # Move to (2, 1)
    game.change_heading("down")  # Move down to (3, 1) and collide
    game.tick()  # This should end the game
    assert game.is_game_over()  # Game should be over
    assert game.get_snake() == [(1, 1), (1, 0)]  # Snake should not have moved past grid

def test_collision_with_self():
    # AC-4.2
    game = SnakeGame(3, 3, [(1, 1), (1, 0)])
    game.change_heading("down")
    game.tick()  # Moves to (1, 1) and eats food
    game.change_heading("down")  # Change heading to down
    game.tick()  # Moves to (1, 0) and eats food
    game.change_heading("up")  # Change to up, colliding with self
    game.tick()  # Should end the game
    assert game.is_game_over()  # Game should be over

def test_tail_vacating_collision():
    # AC-4.3
    game = SnakeGame(3, 3, [(1, 1), (1, 0)])
    game.change_heading("down")
    game.tick()  # Move to (1, 0)
    game.change_heading("down")
    game.tick()  # Move to (1, 1) and eat food
    game.change_heading("down")
    game.tick()  # Move to (2, 1)
    game.change_heading("up")  # Change heading to up
    game.tick()  # Move to (1, 1) again (tail vacated)
    assert not game.is_game_over()  # Should not be game over
    game.change_heading("down")  # Move back down
    game.tick()  # Move to (2, 1) again
    assert game.get_snake() == [(2, 1), (1, 1), (1, 0)]  # Snake is still intact

def test_no_change_after_game_over():
    # AC-4.4
    game = SnakeGame(3, 3, [(1, 1)])
    game.change_heading("down")
    game.tick()  # Moves to (1, 1)
    game.change_heading("down")
    game.tick()  # This should end the game
    assert game.is_game_over()  # Confirm game is over
    current_snake = game.get_snake()
    current_score = game.get_score()
    game.tick()  # Further ticks should have no effect
    assert game.get_snake() == current_snake  # Snake should remain the same
    assert game.get_score() == current_score  # Score should remain the same