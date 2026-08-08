import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    # The rover should start at (0, 0) facing N on a 100 by 100 grid
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_valid_arguments():
    rover = Rover(10, 10, 'E')
    # The rover should be deployed to (0, 0) facing E on a 10 by 10 grid
    assert rover.position == (0, 0)
    assert rover.heading == 'E'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_lowercase_heading():
    rover = Rover(100, 100, 's')
    # The heading should be reported as uppercase
    assert rover.heading == 'S'

def test_deploy_with_unknown_heading():
    rover = Rover(100, 100, 'Z')
    # The rover should raise an error for unknown heading
    assert rover.heading == "Unknown direction: Z"

def test_deploy_with_zero_width_grid():
    rover = Rover(0, 100, 'N')
    # The rover should raise an error for zero width grid
    assert rover.heading == "Grid dimensions must be positive"

def test_deploy_with_zero_height_grid():
    rover = Rover(100, 0, 'N')
    # The rover should raise an error for zero height grid
    assert rover.heading == "Grid dimensions must be positive"

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    # A 1 by 1 grid should be accepted
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'ok'

def test_forward_move():
    rover = Rover(100, 100, 'N')
    rover.drive('f')
    # Moving forward from (0, 0) facing N should result in (0, 99)
    assert rover.position == (0, 99)

def test_backward_move():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.drive('b')
    # Moving backward from (0, 0) facing N should result in (0, 1)
    assert rover.position == (0, 1)

def test_sequential_commands():
    rover = Rover(100, 100, 'S')
    rover.drive('fflff')
    # Starting at (0, 0) facing S, the command string should end at (2, 2) facing E
    assert rover.position == (2, 2)
    assert rover.heading == 'E'

def test_unknown_command():
    rover = Rover(100, 100, 'N')
    assert rover.drive('x') == "Unknown command: x"

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.drive('l')
    # Turning left from N should result in facing W
    assert rover.heading == 'W'

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.drive('r')
    # Turning right from N should result in facing E
    assert rover.heading == 'E'

def test_edge_wrapping_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.drive('f')
    # Moving north from (0, 0) should wrap to (0, 99)
    assert rover.position == (0, 99)

def test_edge_wrapping_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.drive('f')
    # Moving south from (0, 99) should wrap to (0, 0)
    assert rover.position == (0, 0)

def test_edge_wrapping_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.drive('f')
    # Moving east from (99, 0) should wrap to (0, 0)
    assert rover.position == (0, 0)

def test_edge_wrapping_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.drive('f')
    # Moving west from (0, 0) should wrap to (99, 0)
    assert rover.position == (99, 0)

def test_backward_move_wrap():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.drive('b')
    # Moving backward from (0, 0) facing N should wrap to (0, 1)
    assert rover.position == (0, 1)

def test_obstacle_blocking_move():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.obstacles = [(0, 99)]  # Place an obstacle directly north
    rover.drive('f')
    # The rover should remain at (0, 0) and be blocked
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 99)

def test_move_after_obstacle():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.obstacles = [(0, 99)]  # Place an obstacle directly north
    rover.drive('f')
    rover.drive('f')
    # The rover should still be at (0, 0) and blocked after the first move
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 99)

def test_turning_with_obstacles():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.obstacles = [(0, 99), (1, 0), (0, 1), (1, 1)]  # Obstacle in every adjacent destination
    rover.drive('l')
    # The rover should be able to turn without being blocked
    assert rover.heading == 'W'
    assert rover.position == (0, 0)
    assert rover.status == 'ok'

def test_nearby_obstacles():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.obstacles = [(0, 1)]  # Place an obstacle adjacent
    rover.drive('f')
    # The rover should move to (0, 99) and not be blocked because the obstacle is not in the destination
    assert rover.position == (0, 99)
    assert rover.status == 'ok'
    assert rover.last_obstacle is None