# test_rover.py

import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.get_state() == ((0, 0), 'N', 'ok', None)  # Deployed at (0, 0) facing N

def test_deploy_with_position_and_heading():
    rover = Rover(5, 5, 'E')  # Deploy at (5, 5) facing E
    assert rover.get_state() == ((5, 5), 'E', 'ok', None)  # Reports its position and heading

def test_deploy_with_invalid_heading():
    rover = Rover(0, 0, 'X')  # Invalid heading
    assert rover.get_state() == "Unknown direction: X"

def test_deploy_with_zero_width_grid():
    rover = Rover(0, 0, 'N', width=0, height=100)  # Zero width
    assert rover.get_state() == "Grid dimensions must be positive"

def test_deploy_with_zero_height_grid():
    rover = Rover(0, 0, 'N', width=100, height=0)  # Zero height
    assert rover.get_state() == "Grid dimensions must be positive"

def test_deploy_with_one_by_one_grid():
    rover = Rover(0, 0, 'N', width=1, height=1)  # Valid 1x1 grid
    assert rover.get_state() == ((0, 0), 'N', 'ok', None)

def test_deploy_with_lowercase_heading():
    rover = Rover(0, 0, 'n')  # Lowercase heading
    assert rover.get_state() == ((0, 0), 'N', 'ok', None)

def test_drive_forward():
    rover = Rover(0, 0, 'N')  # Starting position (0, 0) facing N
    rover.drive('f')  # Move forward
    assert rover.get_state() == ((0, 99), 'N', 'ok', None)  # Moves to (0, 99)

def test_drive_backward():
    rover = Rover(0, 1, 'N')  # Starting position (0, 1) facing N
    rover.drive('b')  # Move backward
    assert rover.get_state() == ((0, 0), 'N', 'ok', None)  # Moves to (0, 0)

def test_drive_sequence():
    rover = Rover(0, 0, 'S')  # Starting position (0, 0) facing S
    rover.drive('fflff')  # Move sequence
    assert rover.get_state() == ((2, 2), 'E', 'ok', None)  # Ends at (2, 2) facing E

def test_drive_with_unknown_command():
    rover = Rover(0, 0, 'N')
    assert rover.drive('fxyz') == "Unknown command: x"

def test_turn_left():
    rover = Rover(0, 0, 'N')
    rover.drive('l')  # Turn left
    assert rover.get_state() == ((0, 0), 'W', 'ok', None)  # Now facing W

def test_turn_right():
    rover = Rover(0, 0, 'N')
    rover.drive('r')  # Turn right
    assert rover.get_state() == ((0, 0), 'E', 'ok', None)  # Now facing E

def test_edge_wrap_north():
    rover = Rover(0, 0, 'N')
    rover.drive('f')  # Move north
    assert rover.get_state() == ((0, 99), 'N', 'ok', None)  # Wraps to (0, 99)

def test_edge_wrap_south():
    rover = Rover(0, 99, 'S')
    rover.drive('f')  # Move south
    assert rover.get_state() == ((0, 0), 'S', 'ok', None)  # Wraps to (0, 0)

def test_edge_wrap_east():
    rover = Rover(99, 0, 'E')
    rover.drive('f')  # Move east
    assert rover.get_state() == ((0, 0), 'E', 'ok', None)  # Wraps to (0, 0)

def test_edge_wrap_west():
    rover = Rover(0, 0, 'W')
    rover.drive('f')  # Move west
    assert rover.get_state() == ((99, 0), 'W', 'ok', None)  # Wraps to (99, 0)

def test_obstacle_stop():
    rover = Rover(1, 1, 'N', obstacles=[(1, 0)])  # Set obstacle ahead
    rover.drive('f')  # Attempt to move into obstacle
    assert rover.get_state() == ((1, 1), 'N', 'blocked', (1, 0))  # Status changed to blocked

def test_obstacle_ignore_turn():
    rover = Rover(1, 1, 'N', obstacles=[(1, 0)])  # Set obstacle ahead
    rover.drive('l')  # Turn left
    assert rover.get_state() == ((1, 1), 'W', 'ok', None)  # Still ok after turn

def test_pass_near_obstacle():
    rover = Rover(1, 1, 'N', obstacles=[(0, 0)])  # Set obstacle nearby
    rover.drive('f')  # Move forward near obstacle
    assert rover.get_state() == ((1, 0), 'N', 'ok', None)  # Status stays ok

def test_obstacle_with_edge_wrap():
    rover = Rover(0, 99, 'S', obstacles=[(0, 0)])  # Set obstacle at (0, 0)
    rover.drive('f')  # Move south into obstacle
    assert rover.get_state() == ((0, 99), 'S', 'blocked', (0, 0))  # Blocked by obstacle at (0, 0)

def test_turn_surrounded_by_obstacles():
    rover = Rover(1, 1, 'N', obstacles=[(1, 0), (0, 1), (1, 2), (2, 1)])  # Surrounded by obstacles
    rover.drive('l')  # Turn left
    assert rover.get_state() == ((1, 1), 'W', 'ok', None)  # Turn succeeds, status remains ok

def test_backward_wrap_north():
    rover = Rover(0, 0, 'N')
    rover.drive('b')  # Move backward
    assert rover.get_state() == ((0, 1), 'N', 'ok', None)  # Moves to (0, 1)

def test_backward_wrap_south():
    rover = Rover(0, 99, 'S')
    rover.drive('b')  # Move backward
    assert rover.get_state() == ((0, 0), 'S', 'ok', None)  # Moves to (0, 0)

def test_backward_wrap_east():
    rover = Rover(99, 0, 'E')
    rover.drive('b')  # Move backward
    assert rover.get_state() == ((98, 0), 'E', 'ok', None)  # Moves to (98, 0)

def test_backward_wrap_west():
    rover = Rover(0, 0, 'W')
    rover.drive('b')  # Move backward
    assert rover.get_state() == ((99, 0), 'W', 'ok', None)  # Moves to (99, 0)

def test_blocked_multi_command():
    rover = Rover(1, 1, 'N', obstacles=[(1, 0)])  # Set obstacle ahead
    rover.drive('flr')  # Attempt to move into obstacle then turn
    assert rover.get_state() == ((1, 1), 'N', 'blocked', (1, 0))  # Blocked, turn not executed