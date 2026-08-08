import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    # Expected: (0, 0) facing N, status "ok", no obstacles
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_valid_arguments():
    rover = Rover(10, 10, 'S')
    # Expected: (0, 0) facing S, status "ok", no obstacles
    assert rover.position == (0, 0)
    assert rover.heading == 'S'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_deploy_with_lowercase_heading():
    rover = Rover(10, 10, 'e')
    # Expected: (0, 0) facing E, status "ok", no obstacles
    assert rover.heading == 'E'

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError, match=r"^Unknown direction: X$"):
        Rover(10, 10, 'X')

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError, match=r"^Grid dimensions must be positive$"):
        Rover(0, 10, 'N')

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError, match=r"^Grid dimensions must be positive$"):
        Rover(10, 0, 'N')

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    # Expected: (0, 0) facing N, status "ok", no obstacles
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_move_forward_north():
    rover = Rover(100, 100, 'N')
    rover.move('f')
    # Expected: (0, 99) facing N
    assert rover.position == (0, 99)
    assert rover.heading == 'N'  # Heading should remain unchanged

def test_move_backward_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 1)
    rover.move('b')
    # Expected: (0, 0) facing N
    assert rover.position == (0, 0)
    assert rover.heading == 'N'  # Heading should remain unchanged

def test_move_forward_east():
    rover = Rover(100, 100, 'E')
    rover.move('f')
    # Expected: (1, 0) facing E
    assert rover.position == (1, 0)
    assert rover.heading == 'E'  # Heading should remain unchanged

def test_move_backward_east():
    rover = Rover(100, 100, 'E')
    rover.position = (1, 0)
    rover.move('b')
    # Expected: (0, 0) facing E
    assert rover.position == (0, 0)
    assert rover.heading == 'E'  # Heading should remain unchanged

def test_move_forward_south():
    rover = Rover(100, 100, 'S')
    rover.move('f')
    # Expected: (0, 1) facing S
    assert rover.position == (0, 1)
    assert rover.heading == 'S'  # Heading should remain unchanged

def test_move_backward_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 1)
    rover.move('b')
    # Expected: (0, 0) facing S
    assert rover.position == (0, 0)
    assert rover.heading == 'S'  # Heading should remain unchanged

def test_move_forward_west():
    rover = Rover(100, 100, 'W')
    rover.move('f')
    # Expected: (99, 0) facing W
    assert rover.position == (99, 0)
    assert rover.heading == 'W'  # Heading should remain unchanged

def test_move_backward_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.move('b')
    # Expected: (1, 0) facing W
    assert rover.position == (1, 0)
    assert rover.heading == 'W'  # Heading should remain unchanged

def test_command_execution_sequence():
    rover = Rover(100, 100, 'S')
    rover.move('fflff')
    # Expected: (2, 2) facing E
    assert rover.position == (2, 2)
    assert rover.heading == 'E'

def test_unknown_command():
    with pytest.raises(ValueError, match=r"^Unknown command: X$"):
        rover = Rover(100, 100, 'N')
        rover.move('fX')

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.move('l')
    # Expected: facing W
    assert rover.heading == 'W'
    assert rover.position == (0, 0)  # Position should remain unchanged

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.move('r')
    # Expected: facing E
    assert rover.heading == 'E'
    assert rover.position == (0, 0)  # Position should remain unchanged

def test_edge_wrap_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('f')
    # Expected: (0, 99) facing N
    assert rover.position == (0, 99)
    assert rover.heading == 'N'  # Heading should remain unchanged

def test_edge_wrap_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.move('f')
    # Expected: (0, 0) facing S
    assert rover.position == (0, 0)
    assert rover.heading == 'S'  # Heading should remain unchanged

def test_edge_wrap_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.move('f')
    # Expected: (0, 0) facing E
    assert rover.position == (0, 0)
    assert rover.heading == 'E'  # Heading should remain unchanged

def test_edge_wrap_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.move('f')
    # Expected: (99, 0) facing W
    assert rover.position == (99, 0)
    assert rover.heading == 'W'  # Heading should remain unchanged

def test_blocked_move():
    rover = Rover(100, 100, 'N')
    rover.obstacles = {(0, 99)}
    rover.move('f')
    # Expected: (0, 0) facing N, status "blocked", last_obstacle (0, 99)
    assert rover.position == (0, 0)
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 99)

def test_blocked_move_same_command_string():
    rover = Rover(100, 100, 'N')
    rover.obstacles = {(0, 99)}
    rover.move('fl')
    # Expected: (0, 0) facing N, status "blocked", last_obstacle (0, 99)
    assert rover.position == (0, 0)
    assert rover.heading == 'N'
    assert rover.status == 'blocked'
    assert rover.last_obstacle == (0, 99)

def test_turning_while_blocked():
    rover = Rover(100, 100, 'N')
    rover.obstacles = {(0, 99)}
    rover.move('f')
    # Turning should still be allowed
    rover.move('l')
    assert rover.heading == 'W'
    assert rover.position == (0, 0)  # Position should remain unchanged

def test_route_adjacent_to_obstacle():
    rover = Rover(100, 100, 'N')
    rover.obstacles = {(0, 1)}
    rover.move('f')
    rover.move('f')
    # Expected: Position (0, 98), status "ok", no last obstacle
    assert rover.position == (0, 98)
    assert rover.status == 'ok'
    assert rover.last_obstacle is None

def test_backward_edge_wrap_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('b')
    # Expected: (0, 1) facing N
    assert rover.position == (0, 1)
    assert rover.heading == 'N'  # Heading should remain unchanged

def test_backward_edge_wrap_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.move('b')
    # Expected: (0, 98) facing S
    assert rover.position == (0, 98)
    assert rover.heading == 'S'  # Heading should remain unchanged

def test_backward_edge_wrap_east():
    rover = Rover(100, 100, 'E')
    rover.position = (0, 0)
    rover.move('b')
    # Expected: (99, 0) facing E
    assert rover.position == (99, 0)
    assert rover.heading == 'E'  # Heading should remain unchanged

def test_backward_edge_wrap_west():
    rover = Rover(100, 100, 'W')
    rover.position = (99, 0)
    rover.move('b')
    # Expected: (0, 0) facing W
    assert rover.position == (0, 0)
    assert rover.heading == 'W'  # Heading should remain unchanged

def test_one_by_one_grid_forward_move():
    rover = Rover(1, 1, 'N')
    rover.move('f')
    # Expected: (0, 0) facing N, status "ok"
    assert rover.position == (0, 0)
    assert rover.status == 'ok'