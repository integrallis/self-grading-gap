from solution import start_game, tick, change_heading

def test_start_game_valid_grid():
    # Game starts on a 3x3 grid
    game = start_game(3, 3, [(1, 1)])
    assert game['snake'] == [(0, 0)]  # AC-1.1: snake starts at (0, 0)
    assert game['heading'] == "right"  # AC-1.1: initial heading is "right"
    assert game['score'] == 0  # AC-1.1: initial score is 0
    assert not game['game_over']  # AC-1.1: game is not over
    assert game['food'] == (1, 1)  # AC-1.1: first food position is (1, 1)

def test_start_game_invalid_grid_width():
    # Game fails to start on a grid with zero width
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        start_game(0, 3, [(1, 1)])

def test_start_game_invalid_grid_height():
    # Game fails to start on a grid with zero height
    with pytest.raises(ValueError, match="grid dimensions must be positive"):
        start_game(3, 0, [(1, 1)])

def test_tick_moves_snake():
    # Start game and tick once
    game = start_game(3, 3, [(1, 1)])
    game = tick(game)
    assert game['snake'] == [(1, 0)]  # AC-2.1: snake moves to (1, 0)
    assert game['score'] == 0  # AC-2.1: score remains 0
    assert game['food'] == (1, 1)  # AC-2.1: food remains at (1, 1)

def test_change_heading_effect():
    # Change heading and tick
    game = start_game(3, 3, [(1, 1)])
    game = change_heading(game, "down")
    game = tick(game)
    assert game['snake'] == [(0, 1)]  # AC-2.2: snake moves down to (0, 1)

def test_change_heading_opposite():
    # Change heading to opposite direction
    game = start_game(3, 3, [(1, 1)])
    game = change_heading(game, "left")  # Current is "right", changing to "left" is ignored
    game = tick(game)
    assert game['snake'] == [(1, 0)]  # AC-2.3: snake still moves right to (1, 0)

def test_change_heading_invalid_direction():
    # Attempt to change to an invalid direction
    game = start_game(3, 3, [(1, 1)])
    with pytest.raises(ValueError, match="unknown direction: 'north'"):
        change_heading(game, "north")

def test_eat_food_growth():
    # Snake eats food and grows
    game = start_game(3, 3, [(1, 1), (2, 2)])
    game = tick(game)  # Move to (1, 0)
    game = tick(game)  # Move to (1, 1) and eat food
    assert game['snake'] == [(1, 1), (1, 0)]  # AC-3.2: snake grows to 2 segments
    assert game['score'] == 1  # AC-3.2: score increases to 1
    assert game['food'] == (2, 2)  # AC-3.2: next food position is (2, 2)

def test_no_food_after_supply():
    # No food left after eating all supplied food
    game = start_game(3, 3, [(1, 1)])
    game = tick(game)  # Move to (1, 0)
    game = tick(game)  # Move to (1, 1) and eat food
    game = tick(game)  # Move to (2, 0)
    assert game['food'] is None  # AC-3.4: no food on board

def test_game_over_edge_collision():
    # Snake collides with the wall
    game = start_game(1, 1, [(1, 1)])  # 1x1 grid
    game = tick(game)  # Move to (0, 0)
    with pytest.raises(ValueError, match="game over"):
        tick(game)  # Out of bounds

def test_game_over_self_collision():
    # Snake collides with itself
    game = start_game(3, 3, [(1, 1)])
    game = tick(game)  # Move to (1, 0)
    game = tick(game)  # Move to (1, 1) and eat food
    game = tick(game)  # Move to (2, 0)
    game = change_heading(game, "up")  # Change heading to go back
    game = tick(game)  # Move to (1, 0)
    assert game['game_over']  # AC-4.2: game over due to self-collision

def test_game_stays_over_after_collision():
    # Game remains over after a collision
    game = start_game(3, 3, [(1, 1)])
    game = tick(game)  # Move to (1, 0)
    game = tick(game)  # Move to (1, 1) and eat food
    game = tick(game)  # Move to (2, 0)
    game = change_heading(game, "up")  # Change heading to go back
    game = tick(game)  # Move to (1, 0) and collide
    assert game['game_over']  # AC-4.4: game is over
    game = tick(game)  # Further ticks do nothing
    assert game['snake'] == [(1, 0), (1, 1)]  # Snake remains the same
    assert game['score'] == 1  # Score remains the same