import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing N
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_valid_arguments():
    rover = Rover(10, 10, 'E')
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'E'  # Facing E
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_case_insensitive_heading():
    rover = Rover(10, 10, 's')
    assert rover.heading == 'S'  # Heading should be reported as uppercase

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError, match="Unknown direction: X"):
        Rover(10, 10, 'X')  # Should raise an error for unknown heading

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(0, 10, 'N')  # Should raise an error for zero width

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(10, 0, 'N')  # Should raise an error for zero height

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing N
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_drive_forward():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("f")
    assert rover.position == (0, 99)  # (0, 0) to (0, -1) wraps to (0, 99)
    assert rover.heading == 'N'  # Still facing N
    assert rover.status == 'ok'  # Status is ok

def test_drive_backward():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("b")
    assert rover.position == (0, 1)  # (0, 0) to (0, 1)
    assert rover.heading == 'N'  # Still facing N
    assert rover.status == 'ok'  # Status is ok

def test_drive_multiple_commands():
    rover = Rover(100, 100, 'S')
    rover.execute_commands("fflff")
    assert rover.position == (2, 2)  # (0, 0) -> (0, 1) -> (0, 2) -> (1, 2) -> (2, 2)
    assert rover.heading == 'E'  # Final heading E
    assert rover.status == 'ok'  # Status is ok

def test_drive_with_unknown_command():
    rover = Rover(100, 100, 'N')
    with pytest.raises(ValueError, match="Unknown command: x"):
        rover.execute_commands("fxy")  # Should raise an error for unknown command

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("l")
    assert rover.heading == 'W'  # Turns from N to W
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'ok'  # Status is ok

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("r")
    assert rover.heading == 'E'  # Turns from N to E
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'ok'  # Status is ok

def test_edge_wrapping_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.execute_commands("f")  # Moving north
    assert rover.position == (0, 99)  # Wraps to (0, 99)
    assert rover.status == 'ok'  # Status is ok

def test_edge_wrapping_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.execute_commands("f")  # Moving south
    assert rover.position == (0, 0)  # Wraps to (0, 0)
    assert rover.status == 'ok'  # Status is ok

def test_edge_wrapping_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.execute_commands("f")  # Moving east
    assert rover.position == (0, 0)  # Wraps to (0, 0)
    assert rover.status == 'ok'  # Status is ok

def test_edge_wrapping_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.execute_commands("f")  # Moving west
    assert rover.position == (99, 0)  # Wraps to (99, 0)
    assert rover.status == 'ok'  # Status is ok

def test_obstacle_blocking_movement():
    rover = Rover(100, 100, 'N')
    rover.set_obstacle(0, 99)  # Set an obstacle at (0, 99)
    rover.execute_commands("f")  # Attempt to move forward into the obstacle
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Last obstacle recorded

def test_same_command_string_blockage():
    rover = Rover(100, 100, 'N')
    rover.set_obstacle(0, 99)  # Set an obstacle at (0, 99)
    rover.execute_commands("flr")  # First command blocks
    assert rover.heading == 'N'  # Heading unchanged
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'blocked'  # Status is still blocked

def test_run_near_obstacle():
    rover = Rover(100, 100, 'N')
    rover.set_obstacle(1, 99)  # Set an obstacle at (1, 99)
    rover.execute_commands("f")  # Move to (0, 99)
    assert rover.position == (0, 99)  # Position at (0, 99)
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle recorded

def test_obstacle_at_wrapped_destination():
    rover = Rover(100, 100, 'N')
    rover.set_obstacle(0, 99)  # Set an obstacle at (0, 99)
    rover.position = (0, 0)
    rover.execute_commands("f")  # This should block
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Last obstacle recorded

def test_complete_compass_cycle_left():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("llll")  # Full cycle left
    assert rover.heading == 'N'  # Back to N
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'ok'  # Status is ok

def test_complete_compass_cycle_right():
    rover = Rover(100, 100, 'N')
    rover.execute_commands("rrrr")  # Full cycle right
    assert rover.heading == 'N'  # Back to N
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'ok'  # Status is ok

def test_drive_on_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    rover.execute_commands("f")  # Move forward
    assert rover.position == (0, 0)  # Position remains (0, 0)
    assert rover.status == 'ok'  # Status remains ok
    assert rover.last_obstacle is None  # No obstacle recorded

def test_backward_wrapping_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 1)
    rover.execute_commands("b")  # Moving backward north
    assert rover.position == (0, 0)  # Wraps to (0, 0)
    assert rover.status == 'ok'  # Status is ok

def test_backward_wrapping_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 0)
    rover.execute_commands("b")  # Moving backward south
    assert rover.position == (0, 99)  # Wraps to (0, 99)
    assert rover.status == 'ok'  # Status is ok

def test_backward_wrapping_east():
    rover = Rover(100, 100, 'E')
    rover.position = (0, 0)
    rover.execute_commands("b")  # Moving backward east
    assert rover.position == (99, 0)  # Wraps to (99, 0)
    assert rover.status == 'ok'  # Status is ok

def test_backward_wrapping_west():
    rover = Rover(100, 100, 'W')
    rover.position = (99, 0)
    rover.execute_commands("b")  # Moving backward west
    assert rover.position == (0, 0)  # Wraps to (0, 0)
    assert rover.status == 'ok'  # Status is ok

def test_turn_with_obstacles():
    rover = Rover(100, 100, 'N')
    rover.set_obstacle(0, 1)  # Set obstacles around
    rover.set_obstacle(1, 0)
    rover.set_obstacle(1, 1)
    rover.execute_commands("l")  # Should be able to turn left
    assert rover.heading == 'W'  # Turns from N to W
    assert rover.position == (0, 0)  # Position unchanged
    assert rover.status == 'ok'  # Status is ok