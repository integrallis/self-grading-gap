import pytest
from solution import Game  # Assuming we have a Game class to handle the game logic

def test_starting_game_on_valid_grid():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    assert game.snake == [(0, 0)]  # AC-1.1: Snake starts at (0, 0)
    assert game.heading == "right"  # AC-1.1: Default heading is "right"
    assert game.score == 0  # AC-1.1: Initial score is 0
    assert not game.is_game_over  # AC-1.1: Game is not over
    assert game.food == (1, 1)  # AC-1.1: First food position is (1, 1)

def test_invalid_grid_dimensions():
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        Game(width=0, height=5, food_positions=[(1, 1)])  # Invalid width
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        Game(width=5, height=0, food_positions=[(1, 1)])  # Invalid height
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        Game(width=-1, height=5, food_positions=[(1, 1)])  # Invalid width
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        Game(width=5, height=-1, food_positions=[(1, 1)])  # Invalid height

def test_tick_advances_snake():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    game.tick()  # Move snake
    assert game.snake == [(1, 0)]  # AC-2.1: Snake head moves to (1, 0)
    assert game.score == 0  # AC-2.1: Score remains unchanged

def test_change_heading():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    game.change_heading("down")  # Change heading to "down"
    game.tick()
    assert game.snake == [(0, 1)]  # AC-2.1: Snake head moves to (0, 1)
    
    game.change_heading("left")  # Change heading to "left"
    game.tick()
    assert game.snake == [(0, 1), (0, 0)]  # AC-2.2: Next tick is now left
    assert game.heading == "left"  # AC-2.2: Heading is "left"

def test_ignore_opposite_heading():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    game.change_heading("down")  # Change heading to "down"
    game.tick()  # Move to (0, 1)
    game.change_heading("up")  # Attempt to change to "up" (opposite)
    game.tick()  # Move again
    assert game.snake == [(0, 2)]  # AC-2.3: Snake still moves down

def test_unknown_direction():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    with pytest.raises(ValueError, match="unknown direction: 'north'"):
        game.change_heading("north")  # AC-2.4: Invalid direction

def test_eating_food():
    game = Game(width=5, height=5, food_positions=[(1, 1), (2, 2)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1) - eat food
    assert game.snake == [(1, 1), (1, 0)]  # AC-3.2: Snake grows at food
    assert game.score == 1  # AC-3.2: Score increases by 1
    assert game.food == (2, 2)  # AC-3.2: Next food is now at (2, 2)

def test_food_appears_correctly():
    game = Game(width=5, height=5, food_positions=[(1, 1), (1, 0), (2, 2)])
    assert game.food == (1, 1)  # AC-3.1: First food is (1, 1)
    game.tick()  # Move to (1, 0)
    assert game.food == (1, 0)  # AC-3.1: Next food is (1, 0)

def test_end_game_on_collision_with_self():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1) - eat food
    game.tick()  # Move to (2, 1)
    game.change_heading("up")  # Change direction
    game.tick()  # Move to (2, 0)
    game.change_heading("down")  # Attempt to move down into self
    game.tick()  # Move into (1, 0), which is occupied by the snake's body
    assert game.is_game_over  # AC-4.2: Game is over

def test_moving_out_of_bounds_ends_game():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    for _ in range(5):  # Move right 5 times
        game.tick()
    assert not game.is_game_over  # Before moving out
    game.change_heading("right")
    game.tick()  # Move out of bounds
    assert game.is_game_over  # AC-4.1: Game ends when moving out of bounds

def test_game_stays_over_after_end():
    game = Game(width=5, height=5, food_positions=[(1, 1)])
    game.change_heading("right")
    for _ in range(6):  # Move right out of bounds
        game.tick()
    assert game.is_game_over  # Game should be over
    snake_before = game.snake[:]
    score_before = game.score
    game.tick()  # Attempt to tick again
    assert game.snake == snake_before  # AC-4.4: Snake remains the same
    assert game.score == score_before  # AC-4.4: Score remains the same