from solution import Rover
import pytest

def test_deployment_default():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'       # Facing North
    assert rover.status == 'ok'       # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record
    assert rover.grid_size == (100, 100)  # Default grid size is 100x100

def test_deployment_with_arguments():
    rover = Rover(5, 5, 'E')
    assert rover.position == (0, 0)  # Default position
    assert rover.heading == 'E'       # Facing East
    assert rover.status == 'ok'       # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record
    assert rover.grid_size == (5, 5)  # Grid size is 5x5

def test_deployment_case_insensitivity():
    rover = Rover(10, 10, 's')
    assert rover.heading == 'S'       # Heading is reported as uppercase

def test_deployment_unknown_heading():
    rover = Rover(10, 10, 'Z')
    assert rover.status == 'blocked'    # Status is blocked
    assert rover.last_obstacle is None  # No obstacle on record

def test_deployment_zero_grid_width():
    rover = Rover(0, 10, 'N')
    assert rover.status == 'blocked'    # Status is blocked
    assert rover.last_obstacle is None  # No obstacle on record

def test_deployment_zero_grid_height():
    rover = Rover(10, 0, 'N')
    assert rover.status == 'blocked'    # Status is blocked
    assert rover.last_obstacle is None  # No obstacle on record

def test_deployment_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'       # Facing North
    assert rover.status == 'ok'       # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_command_forward_north_wrap():
    rover = Rover(100, 100, 'N')
    rover.execute_commands('f')
    assert rover.position == (0, 99)  # Moves from (0, 0) to (0, 99)
    assert rover.heading == 'N'        # Heading remains North

def test_command_forward_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 1)   # Moves from (0, 0) to (0, 1)
    assert rover.heading == 'S'        # Heading remains South

def test_command_forward_east():
    rover = Rover(100, 100, 'E')
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (1, 0)   # Moves from (0, 0) to (1, 0)
    assert rover.heading == 'E'        # Heading remains East

def test_command_forward_west():
    rover = Rover(100, 100, 'W')
    rover.position = (1, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 0)   # Moves from (1, 0) to (0, 0)
    assert rover.heading == 'W'        # Heading remains West

def test_command_backward_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 1)
    rover.execute_commands('b')
    assert rover.position == (0, 0)   # Moves from (0, 1) to (0, 0)
    assert rover.heading == 'N'        # Heading remains North

def test_command_backward_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 1)
    rover.execute_commands('b')
    assert rover.position == (0, 2)   # Moves from (0, 1) to (0, 2)
    assert rover.heading == 'S'        # Heading remains South

def test_command_backward_east():
    rover = Rover(100, 100, 'E')
    rover.position = (1, 0)
    rover.execute_commands('b')
    assert rover.position == (0, 0)   # Moves from (1, 0) to (0, 0)
    assert rover.heading == 'E'        # Heading remains East

def test_command_backward_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.execute_commands('b')
    assert rover.position == (1, 0)   # Moves from (0, 0) to (1, 0)
    assert rover.heading == 'W'        # Heading remains West

def test_command_sequence():
    rover = Rover(100, 100, 'S')
    rover.execute_commands('fflff')
    assert rover.position == (2, 2)   # End position after commands
    assert rover.heading == 'E'        # Final heading after rotation

def test_command_unknown_command():
    rover = Rover(100, 100, 'N')
    rover.execute_commands('fxyz')
    assert rover.position == (0, 99)   # Last valid position after 'f'
    assert rover.heading == 'N'         # Heading remains North
    assert rover.status == 'blocked'     # Status is blocked
    assert rover.last_obstacle is None   # No obstacle encountered

def test_turn_left_cycle():
    rover = Rover(100, 100, 'N')
    rover.execute_commands('l')
    assert rover.heading == 'W'        # Turned from North to West
    rover.execute_commands('l')
    assert rover.heading == 'S'        # Turned from West to South
    rover.execute_commands('l')
    assert rover.heading == 'E'        # Turned from South to East
    rover.execute_commands('l')
    assert rover.heading == 'N'        # Turned from East to North

def test_turn_right_cycle():
    rover = Rover(100, 100, 'N')
    rover.execute_commands('r')
    assert rover.heading == 'E'        # Turned from North to East
    rover.execute_commands('r')
    assert rover.heading == 'S'        # Turned from East to South
    rover.execute_commands('r')
    assert rover.heading == 'W'        # Turned from South to West
    rover.execute_commands('r')
    assert rover.heading == 'N'        # Turned from West to North

def test_edge_wrapping_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 99)   # Wraps from (0, 0) to (0, 99)

def test_edge_wrapping_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.execute_commands('f')
    assert rover.position == (0, 0)    # Wraps from (0, 99) to (0, 0)

def test_edge_wrapping_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 0)    # Wraps from (99, 0) to (0, 0)

def test_edge_wrapping_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (99, 0)   # Wraps from (0, 0) to (99, 0)

def test_obstacle_blocked_move():
    rover = Rover(100, 100, 'N', obstacles={(0, 99)})
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 0)    # Remains at (0, 0)
    assert rover.status == 'blocked'    # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Last obstacle recorded

def test_obstacle_no_blocking():
    rover = Rover(100, 100, 'N', obstacles={(1, 1)})
    rover.position = (0, 0)
    rover.execute_commands('ff')
    assert rover.position == (0, 98)   # Moves to (0, 98)
    assert rover.status == 'ok'         # Status remains ok
    assert rover.last_obstacle is None  # No obstacle since it didn't encounter one

def test_command_after_blocked_move():
    rover = Rover(100, 100, 'N', obstacles={(0, 99)})
    rover.position = (0, 0)
    rover.execute_commands('f')
    assert rover.position == (0, 0)    # Remains at (0, 0) due to block
    assert rover.status == 'blocked'    # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Last obstacle recorded
    rover.execute_commands('r')
    assert rover.heading == 'N'         # Heading remains unchanged

def test_turning_obstacle():
    rover = Rover(100, 100, 'N', obstacles={(0, 99), (0, 1), (1, 0), (99, 0)})
    rover.position = (0, 0)
    rover.execute_commands('l')
    assert rover.position == (0, 0)    # Position unchanged
    assert rover.heading == 'W'         # Heading changed to West
    rover.execute_commands('r')
    assert rover.heading == 'N'         # Heading changed back to North