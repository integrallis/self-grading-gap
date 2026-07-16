import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at starting position (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_valid_arguments():
    rover = Rover(5, 5, 'E')
    assert rover.position == (0, 0)  # Starting position is (0, 0)
    assert rover.heading == 'E'  # Facing East
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_case_insensitive_heading():
    rover = Rover(5, 5, 's')
    assert rover.heading == 'S'  # Heading should be reported as 'S'

def test_deploy_with_unknown_heading():
    with pytest.raises(Exception) as excinfo:
        Rover(5, 5, 'Z')
    assert str(excinfo.value) == "Unknown direction: Z"

def test_deploy_with_zero_grid_width():
    with pytest.raises(Exception) as excinfo:
        Rover(0, 5, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_zero_grid_height():
    with pytest.raises(Exception) as excinfo:
        Rover(5, 0, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    assert rover.position == (0, 0)  # Starting position is (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_default_grid_behavior():
    rover = Rover()
    rover.move('f')  # Move from (0, 0) to (0, 99)
    assert rover.position == (0, 99)  # Should wrap to (0, 99)
    assert rover.status == 'ok'  # Status is ok

def test_move_forward():
    rover = Rover(5, 5, 'N')
    rover.move('f')
    assert rover.position == (0, 4)  # Move forward to (0, 4)
    assert rover.heading == 'N'  # Heading remains 'N'
    assert rover.status == 'ok'  # Status is ok

def test_move_backward():
    rover = Rover(5, 5, 'N')
    rover.move('b')
    assert rover.position == (0, 1)  # Move backward to (0, 1)
    assert rover.heading == 'N'  # Heading remains 'N'
    assert rover.status == 'ok'  # Status is ok

def test_move_sequence():
    rover = Rover(5, 5, 'S')
    rover.move('fflff')  # Move sequence
    assert rover.position == (2, 2)  # Final position after moves
    assert rover.heading == 'E'  # Final heading after turns
    assert rover.status == 'ok'  # Status is ok

def test_unknown_command():
    rover = Rover(5, 5, 'N')
    with pytest.raises(Exception) as excinfo:
        rover.move('x')
    assert str(excinfo.value) == "Unknown command: x"

def test_turn_left():
    rover = Rover(5, 5, 'N')
    rover.move('l')
    assert rover.heading == 'W'  # Heading should now be West

def test_turn_right():
    rover = Rover(5, 5, 'N')
    rover.move('r')
    assert rover.heading == 'E'  # Heading should now be East

def test_turn_full_cycle_left():
    rover = Rover(5, 5, 'N')
    rover.move('llll')  # Full turn cycle left
    assert rover.heading == 'N'  # Should end facing North

def test_turn_full_cycle_right():
    rover = Rover(5, 5, 'N')
    rover.move('rrrr')  # Full turn cycle right
    assert rover.heading == 'N'  # Should end facing North

def test_edge_wrapping_north():
    rover = Rover(5, 5, 'N')
    rover.move('f')  # Move from (0,0) to (0,4)
    assert rover.position == (0, 4)  # Wrap around to (0, 4)

def test_edge_wrapping_south():
    rover = Rover(5, 5, 'S')
    rover.position = (0, 0)  # Starting at top row
    rover.move('f')  # Move south from (0,0) to (0,1)
    assert rover.position == (0, 1)  # Should reach (0, 1)

def test_edge_wrapping_east():
    rover = Rover(5, 5, 'E')
    rover.position = (4, 0)  # Starting at right column
    rover.move('f')  # Move east from (4,0) to (0,0)
    assert rover.position == (0, 0)  # Wrap around to (0, 0)

def test_edge_wrapping_west():
    rover = Rover(5, 5, 'W')
    rover.position = (0, 0)  # Starting at left column
    rover.move('f')  # Move west from (0,0) to (4,0)
    assert rover.position == (4, 0)  # Wrap around to (4, 0)

def test_edge_wrapping_backward_north():
    rover = Rover(5, 5, 'N')
    rover.position = (0, 0)  # Starting at top row
    rover.move('b')  # Move backward from (0,0) to (0,4)
    assert rover.position == (0, 4)  # Should wrap to (0, 4)

def test_edge_wrapping_backward_south():
    rover = Rover(5, 5, 'S')
    rover.position = (0, 0)  # Starting at top row
    rover.move('b')  # Move backward from (0,0) to (0,4)
    assert rover.position == (0, 4)  # Should wrap to (0, 4)

def test_edge_wrapping_backward_east():
    rover = Rover(5, 5, 'E')
    rover.position = (4, 0)  # Starting at right column
    rover.move('b')  # Move backward from (4,0) to (3,0)
    assert rover.position == (3, 0)  # Should reach (3, 0)

def test_edge_wrapping_backward_west():
    rover = Rover(5, 5, 'W')
    rover.position = (0, 0)  # Starting at left column
    rover.move('b')  # Move backward from (0,0) to (0,4)
    assert rover.position == (0, 4)  # Should wrap to (0, 4)

def test_obstacle_blocking_move():
    rover = Rover(5, 5, 'N')
    rover.obstacles = {(0, 4)}  # Place an obstacle at (0, 4)
    rover.move('f')
    assert rover.position == (0, 0)  # Should not move
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.last_obstacle == (0, 4)  # Last obstacle recorded

def test_remaining_commands_after_blocked_move():
    rover = Rover(5, 5, 'N')
    rover.obstacles = {(0, 4)}  # Place an obstacle at (0, 4)
    rover.move('fl')  # First move blocked
    assert rover.position == (0, 0)  # Should not move
    assert rover.heading == 'N'  # Heading should remain 'N'
    assert rover.status == 'blocked'  # Status should be blocked

def test_turning_with_obstacle():
    rover = Rover(5, 5, 'N')
    rover.obstacles = {(0, 1)}  # Place an obstacle at (0, 1)
    rover.move('l')  # Turn left
    assert rover.heading == 'W'  # Should turn left regardless of obstacle
    assert rover.status == 'ok'  # Status should still be ok

def test_near_obstacle():
    rover = Rover(5, 5, 'N')
    rover.obstacles = {(0, 4)}  # Place an obstacle at (0, 4)
    rover.move('f')  # Move to (0, 3)
    assert rover.position == (0, 3)  # Should move to (0, 3)
    assert rover.status == 'ok'  # Status should still be ok
    assert rover.last_obstacle is None  # No obstacle recorded

def test_edge_wrapping_backward():
    rover = Rover(5, 5, 'N')
    rover.move('b')  # Move backward from (0,0) to (0,1)
    assert rover.position == (0, 1)  # Wrap around to (0, 1)

def test_forward_move_on_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    rover.move('f')
    assert rover.position == (0, 0)  # Still at (0, 0)
    assert rover.status == 'ok'  # Status remains ok