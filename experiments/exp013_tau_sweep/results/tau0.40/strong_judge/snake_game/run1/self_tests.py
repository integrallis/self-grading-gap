# test_snake_arcade.py

import pytest
from solution import start_game, tick, change_direction

# US-1: Starting a game on a valid grid
def test_start_game_valid_grid():
    # Starting a game on a 3x3 grid
    grid_width = 3
    grid_height = 3
    food_positions = [(1, 1)]
    state = start_game(grid_width, grid_height, food_positions)
    
    # Expected state
    expected_state = {
        'snake': [(0, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': False,
        'food': (1, 1)  # First supplied food
    }
    assert state == expected_state

def test_start_game_invalid_grid_width():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        start_game(0, 3, [(1, 1)])

def test_start_game_invalid_grid_height():
    with pytest.raises(Exception, match=r"^grid dimensions must be positive$"):
        start_game(3, 0, [(1, 1)])

def test_start_game_one_by_one_grid():
    state = start_game(1, 1, [])
    
    # Expected state for a 1x1 grid
    expected_state = {
        'snake': [(0, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': False,
        'food': None  # No food can be placed
    }
    assert state == expected_state
    
    # First tick should end the game
    state = tick(state)
    expected_state_after_tick = {
        'snake': [(0, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': True,
        'food': None
    }
    assert state == expected_state_after_tick

# US-2: Steering the snake tick by tick
def test_tick_moves_snake_forward():
    state = start_game(3, 3, [(1, 1)])
    next_state = tick(state)
    
    # The snake head moves from (0,0) to (1,0)
    expected_state = {
        'snake': [(1, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': False,
        'food': (1, 1)
    }
    assert next_state == expected_state

def test_change_direction_effects():
    state = start_game(3, 3, [(1, 1)])
    state = change_direction(state, 'down')
    next_state = tick(state)
    
    # The snake head moves down to (0,1)
    expected_state = {
        'snake': [(0, 1)],
        'heading': 'down',
        'score': 0,
        'game_over': False,
        'food': (1, 1)
    }
    assert next_state == expected_state

def test_change_direction_opposite_ignored():
    state = start_game(3, 3, [(1, 1)])
    state = change_direction(state, 'down')  # Change to down (valid)
    state = change_direction(state, 'up')    # Change to opposite (ignored)
    next_state = tick(state)
    
    # The snake still moves down
    expected_state = {
        'snake': [(0, 1)],
        'heading': 'down',
        'score': 0,
        'game_over': False,
        'food': (1, 1)
    }
    assert next_state == expected_state

def test_change_direction_invalid_direction():
    state = start_game(3, 3, [(1, 1)])
    with pytest.raises(Exception, match=r"^unknown direction: 'north'$"):
        change_direction(state, 'north')

# US-3: Eating food, growing, and scoring
def test_eating_food_grows_snake_and_scores():
    state = start_game(3, 3, [(1, 0)])  # Food positioned at (1, 0)
    state = tick(state)  # Move to (1,0) and eat food

    # Expected state after eating food
    expected_state = {
        'snake': [(1, 0), (0, 0)],  # Snake now has grown
        'heading': 'right',
        'score': 1,  # Score increased
        'game_over': False,
        'food': None  # No more food available
    }
    assert state == expected_state

    state = tick(state)  # The snake moves to (2,0) now
    next_expected_state = {
        'snake': [(2, 0), (1, 0)],  # Snake moves without growing
        'heading': 'right',
        'score': 1,
        'game_over': False,
        'food': None
    }
    assert state == next_expected_state

def test_food_selection_skips_occupied_cells():
    state = start_game(3, 3, [(1, 1), (1, 0)])  # Food first at (1, 1), then (1, 0) is occupied
    state = tick(state)  # Move to (1,0) and eat food
    state = tick(state)  # Snake now at (1,0); next food should skip (1,0)

    # Expected state after eating food
    expected_state = {
        'snake': [(1, 0), (0, 0)],  # Snake has grown
        'heading': 'right',
        'score': 1,  # Score increased
        'game_over': False,
        'food': None  # No more food available
    }
    assert state == expected_state

def test_multiple_food_growth():
    state = start_game(3, 3, [(1, 1), (1, 2), (2, 2)])  # Food in sequence
    state = tick(state)  # Move to (1,0)
    state = tick(state)  # Move to (1,1) - eat food
    state = tick(state)  # Move to (1,2) - eat food

    # Expected state after eating two foods
    expected_state = {
        'snake': [(1, 2), (1, 1), (0, 0)],  # Snake has grown by 2 segments
        'heading': 'right',
        'score': 2,  # Score increased by 2
        'game_over': False,
        'food': (2, 2)  # Next food position
    }
    state_after_eating = tick(state)  # Move to (2,2) and eat food again
    assert state_after_eating == expected_state

def test_food_exhaustion():
    state = start_game(3, 3, [(1, 1)])  # Start with one food
    state = tick(state)  # Move to (1,0)
    state = tick(state)  # Move to (1,1) - eat food
    
    # Expected state after eating food
    expected_state = {
        'snake': [(1, 1), (0, 0)],  # Snake has grown
        'heading': 'right',
        'score': 1,  # Score increased
        'game_over': False,
        'food': None  # No more food available
    }
    assert state == expected_state
    
    state = tick(state)  # Continue moving without food
    next_expected_state = {
        'snake': [(1, 1), (1, 0)],  # Snake continues moving
        'heading': 'right',
        'score': 1,  # Score remains the same
        'game_over': False,
        'food': None  # Still no food available
    }
    assert state == next_expected_state

# US-4: Ending the game on collisions
def test_game_over_on_edge_collision():
    state = start_game(2, 2, [(1, 1)])  # 2x2 grid with food at (1,1)
    state = tick(state)  # Move to (1,0)
    state = tick(state)  # Move to (1,1) - eat food
    state = tick(state)  # Move to (1,0) - now at edge
    state = change_direction(state, 'right')  # Attempt to move past edge (fatal)
    next_state = tick(state)  # Should not move out of bounds
    
    # Expected state should reflect game over
    expected_state = {
        'snake': [(1, 0)],
        'heading': 'right',
        'score': 1,
        'game_over': True,
        'food': None  # No more food available
    }
    assert next_state == expected_state

def test_game_over_on_self_collision():
    state = start_game(3, 3, [(1, 1)])  # Food in sequence
    state = tick(state)  # Move to (1,0)
    state = tick(state)  # Move to (1,1) - eat food
    state = change_direction(state, 'up')
    state = tick(state)  # Move to (0,1)
    state = change_direction(state, 'left')
    state = tick(state)  # Move to (0,0)
    state = change_direction(state, 'down')
    state = tick(state)  # Move to (1,0) - head collides with body
    
    # Expected state should reflect game over
    expected_state = {
        'snake': [(1, 0)],
        'heading': 'down',
        'score': 1,
        'game_over': True,
        'food': None  # No more food available
    }
    assert state == expected_state

def test_game_over_state_is_final():
    state = start_game(2, 2, [(1, 1)])
    state = tick(state)  # Move to (1,0)
    state = tick(state)  # Move to (1,1) - eat food
    state = tick(state)  # Move to (1,0)
    state = change_direction(state, 'down')  # Attempt to move past edge
    next_state = tick(state)  # Should end the game

    # Verify that further ticks do not change the state
    assert next_state['game_over'] is True
    no_change_state = tick(next_state)  # Further tick, should remain the same
    assert no_change_state == next_state

def test_tail_vacate_safety():
    state = start_game(3, 3, [(1, 0), (1, 1), (0, 1)])  # Food in sequence
    state = tick(state)  # Move to (1,0) - eat food
    state = tick(state)  # Move to (1,1) - eat food
    state = tick(state)  # Move to (0,1) - eat food

    # Now snake is at (0,1) with length 3
    state = change_direction(state, 'down')  # Change direction to down
    next_state = tick(state)  # Move to (1,1) - should be safe to enter tail cell (0,0)

    # Expected state after moving into tail cell
    expected_state = {
        'snake': [(1, 0), (1, 1), (0, 1)],  # Snake can safely move into tail
        'heading': 'down',
        'score': 3,
        'game_over': False,
        'food': None  # No more food available
    }
    assert next_state == expected_state

def test_start_game_food_at_occupied_cell():
    state = start_game(3, 3, [(0, 0), (1, 1)])  # Food at (0, 0) which is occupied
    # The first food should be skipped
    expected_state = {
        'snake': [(0, 0)],
        'heading': 'right',
        'score': 0,
        'game_over': False,
        'food': (1, 1)  # Next food position
    }
    assert state == expected_state