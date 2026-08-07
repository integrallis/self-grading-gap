# test_rover.py

import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    # Deployed without arguments, the rover starts at (0, 0) facing N on a 100 by 100 grid
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_non_default_position():
    rover = Rover(10, 10, 'E', (5, 5))
    # Deployed with (10, 10) grid, initial heading 'E' and position (5, 5)
    assert rover.position == (5, 5)
    assert rover.heading == 'E'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_lowercase_heading():
    rover = Rover(10, 10, 's')
    # Heading 's' should be treated as 'S'
    assert rover.heading == 'S'

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError) as excinfo:
        Rover(10, 10, 'X')
    assert str(excinfo.value) == "Unknown direction: X"

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError) as excinfo:
        Rover(0, 10, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError) as excinfo:
        Rover(10, 0, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    # 1 by 1 grid is accepted
    assert rover.position == (0, 0)

def test_move_forward():
    rover = Rover(100, 100, 'N')
    rover.move('f')
    # Moving forward from (0, 0) facing N goes to (0, 99)
    assert rover.position == (0, 99)

def test_move_backward():
    rover = Rover(100, 100, 'N')
    rover.move('b')
    # Moving backward from (0, 0) facing N goes to (0, 1)
    assert rover.position == (0, 1)

def test_command_string_execution():
    rover = Rover(100, 100, 'S')
    rover.move('fflff')
    # Starting at (0, 0) facing S, fflff results in (2, 2) facing E
    assert rover.position == (2, 2)
    assert rover.heading == 'E'

def test_unknown_command():
    rover = Rover(100, 100, 'N')
    with pytest.raises(ValueError) as excinfo:
        rover.move('x')
    assert str(excinfo.value) == "Unknown command: x"

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.move('l')
    # Turning left from N results in W
    assert rover.heading == 'W'

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.move('r')
    # Turning right from N results in E
    assert rover.heading == 'E'

def test_turn_left_full_cycle():
    rover = Rover(100, 100, 'N')
    rover.move('l')
    assert rover.heading == 'W'
    rover.move('l')
    assert rover.heading == 'S'
    rover.move('l')
    assert rover.heading == 'E'
    rover.move('l')
    assert rover.heading == 'N'

def test_turn_right_full_cycle():
    rover = Rover(100, 100, 'N')
    rover.move('r')
    assert rover.heading == 'E'
    rover.move('r')
    assert rover.heading == 'S'
    rover.move('r')
    assert rover.heading == 'W'
    rover.move('r')
    assert rover.heading == 'N'

def test_edge_wrap_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('f')
    # Moving north from (0, 0) wraps to (0, 99)
    assert rover.position == (0, 99)

def test_edge_wrap_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.move('f')
    # Moving south from (0, 99) wraps to (0, 0)
    assert rover.position == (0, 0)

def test_edge_wrap_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.move('f')
    # Moving east from (99, 0) wraps to (0, 0)
    assert rover.position == (0, 0)

def test_edge_wrap_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.move('f')
    # Moving west from (0, 0) wraps to (99, 0)
    assert rover.position == (99, 0)

def test_backward_edge_wrap_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('b')
    # Moving backward from (0, 0) facing N goes to (0, 1)
    assert rover.position == (0, 1)

def test_backward_edge_wrap_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 0)
    rover.move('b')
    # Moving backward from (0, 0) facing S goes to (0, 99)
    assert rover.position == (0, 99)

def test_backward_edge_wrap_east():
    rover = Rover(100, 100, 'E')
    rover.position = (0, 0)
    rover.move('b')
    # Moving backward from (0, 0) facing E goes to (99, 0)
    assert rover.position == (99, 0)

def test_backward_edge_wrap_west():
    rover = Rover(100, 100, 'W')
    rover.position = (99, 0)
    rover.move('b')
    # Moving backward from (99, 0) facing W goes to (0, 0)
    assert rover.position == (0, 0)

def test_obstacle_blockage():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.move('f')
    # Moving to (0, 9) where there is an obstacle blocks the rover
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 9)

def test_obstacle_no_error_on_block():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.move('f')
    # The outcome is carried entirely in the rover's state
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'

def test_turns_are_not_blocked():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.move('l')
    # Turning left should not be blocked
    assert rover.heading == 'W'

def test_obstacle_near_but_not_into():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.move('b')
    # Moving backward to (0, 1) should not hit an obstacle
    assert rover.position == (0, 1)
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_obstacle_blocked_movement_stops_execution():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.move('f')
    # The next turn should not execute after a blockage
    assert rover.heading == 'N'
    rover.move('l')
    assert rover.heading == 'N'  # Heading should remain the same

def test_wrapped_destination_obstacle():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 9)}
    rover.position = (0, 0)
    rover.move('f')  # This will hit the obstacle wrapping from (0,0) to (0,9)
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 9)

def test_surrounded_rover_turn():
    rover = Rover(10, 10, 'N')
    rover.obstacles = {(0, 1), (1, 0), (0, 9), (9, 0)}
    rover.move('l')  # Should still be able to turn
    assert rover.heading == 'W'