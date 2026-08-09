import pytest
from solution import SnakeGame  # Assuming the class handling the game is called SnakeGame

def test_start_game_valid_grid():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    assert game.snake == [(0, 0)]  # AC-1.1: One-segment snake at (0, 0)
    assert game.heading == "right"  # AC-1.1: Heading "right"
    assert game.score == 0  # AC-1.1: Score is zero
    assert not game.is_game_over  # AC-1.1: Game is not over
    assert game.food == (1, 0)  # AC-1.1: First food on board

def test_start_game_invalid_grid_zero_width():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        SnakeGame(width=0, height=5, food_positions=[(1, 0)])

def test_start_game_invalid_grid_zero_height():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        SnakeGame(width=5, height=0, food_positions=[(1, 0)])

def test_start_game_invalid_grid_negative_width():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        SnakeGame(width=-5, height=5, food_positions=[(1, 0)])

def test_start_game_invalid_grid_negative_height():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        SnakeGame(width=5, height=-5, food_positions=[(1, 0)])

def test_start_game_valid_grid_one_by_one():
    game = SnakeGame(width=1, height=1, food_positions=[(0, 0)])
    assert game.snake == [(0, 0)]  # Snake fills the grid
    assert not game.is_game_over  # Game is not over initially
    game.tick()  # First tick should end the game
    assert game.is_game_over  # Game should be over after the tick

def test_tick_moves_snake():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    game.tick()  # Move the snake right
    assert game.snake == [(1, 0), (0, 0)]  # AC-2.1: Snake head moved to (1, 0) and grew
    assert not game.is_game_over  # Game is still ongoing

def test_change_heading():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    game.change_heading("down")  # Change heading to down
    game.tick()  # Move the snake
    assert game.snake == [(0, 1)]  # AC-2.1: Snake head moved down to (0, 1)

def test_change_heading_ignored_opposite():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    game.tick()  # Move right
    game.change_heading("left")  # Change heading to left (opposite)
    game.tick()  # Attempt to move
    assert game.snake == [(2, 0)]  # AC-2.3: Snake remains at (2, 0)

def test_invalid_heading():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    with pytest.raises(Exception, match="unknown direction: 'north'"):
        game.change_heading("north")

def test_eat_food_and_grow():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0), (2, 0)])
    game.tick()  # Move to (1, 0) to eat food
    assert game.snake == [(1, 0), (0, 0)]  # AC-3.2: Snake grows after eating
    assert game.score == 1  # AC-3.2: Score increases by 1
    assert game.food == (2, 0)  # Next food appears

def test_food_selection_skips_occupied_position():
    game = SnakeGame(width=5, height=5, food_positions=[(0, 0), (1, 0), (2, 0)])
    assert game.food == (1, 0)  # Initial food should skip occupied (0, 0)
    game.tick()  # Move to (1, 0) to eat food
    assert game.food == (2, 0)  # Next food should be at (2, 0)

def test_multiple_foods():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0), (2, 0)])
    game.tick()  # Move to (1, 0) to eat food
    game.tick()  # Move to (2, 0) to eat food
    assert game.score == 2  # Score should be 2 after eating two foods
    assert game.snake == [(2, 0), (1, 0), (0, 0)]  # Snake should have grown to 3 segments

def test_no_food_left():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0), (2, 0)])
    game.tick()  # Eat food at (1, 0)
    game.tick()  # Move to (2, 0) and eat food
    game.tick()  # Move to (3, 0) (no food left)
    assert game.food is None  # AC-3.4: No food left on the board

def test_game_over_edge_collision():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    for _ in range(5):
        game.tick()  # Move right to the edge
    assert game.is_game_over  # AC-4.1: Game ends at edge
    assert game.snake == [(4, 0), (3, 0)]  # Snake should be at edge position

def test_game_over_self_collision():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0), (2, 0), (2, 1), (1, 1)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Grow snake to [(1, 0), (0, 0)]
    game.change_heading("down")  # Change heading to down
    game.tick()  # Move to (1, 1)
    game.change_heading("left")  # Change heading to left
    game.tick()  # Move to (0, 1)
    game.change_heading("up")  # Change heading to up
    game.tick()  # Move to (1, 0) (self-collision)
    assert game.is_game_over  # AC-4.2: Game ends due to self-collision

def test_tick_after_game_over():
    game = SnakeGame(width=5, height=5, food_positions=[(1, 0)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (2, 0)
    game.tick()  # Move to (3, 0) (no food left)
    game.tick()  # Move to edge (game over)
    game.tick()  # Attempt to tick after game over
    assert game.snake == [(4, 0), (3, 0)]  # AC-4.4: Snake remains the same
    assert game.score == 1  # Score is still 1
    assert game.is_game_over  # Game is still over

def test_tail_chasing():
    game = SnakeGame(width=2, height=2, food_positions=[(1, 0), (1, 1), (0, 1)])
    game.tick()  # Move to (1, 0)
    game.tick()  # Move to (1, 1)
    game.change_heading("up")  # Change heading to up
    game.tick()  # Move to (0, 1)
    game.change_heading("left")  # Change heading to left
    game.tick()  # Move to (0, 0) (tail is at (1, 1))
    game.change_heading("down")  # Change heading to down
    game.tick()  # Move to (1, 1) (tail vacated)
    assert not game.is_game_over  # Game continues, tail cell being vacated is safe