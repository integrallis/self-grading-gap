import pytest
from solution import Rover

def test_deploy_rover_default():
    rover = Rover()
    assert rover.position == (0, 0)  # AC-1.2: Default position
    assert rover.heading == 'N'  # AC-1.2: Default heading
    assert rover.status == 'ok'  # AC-1.2: Default status
    assert rover.obstacle is None  # AC-1.2: No obstacle

def test_deploy_rover_with_arguments():
    rover = Rover(x=5, y=5, heading='E', grid_width=10, grid_height=10)
    assert rover.position == (5, 5)  # AC-1.1: Deployed position
    assert rover.heading == 'E'  # AC-1.1: Deployed heading
    assert rover.status == 'ok'  # AC-1.1: Default status
    assert rover.obstacle is None  # AC-1.1: No obstacle

def test_deploy_rover_case_insensitivity():
    rover = Rover(heading='s')
    assert rover.heading == 'S'  # AC-1.3: Heading is case-insensitive

def test_deploy_rover_unknown_heading():
    with pytest.raises(ValueError) as excinfo:  # Expecting a ValueError
        Rover(heading='X')
    assert str(excinfo.value) == "Unknown direction: X"  # AC-1.4: Unknown heading

def test_deploy_rover_zero_width_grid():
    with pytest.raises(ValueError) as excinfo:  # Expecting a ValueError
        Rover(grid_width=0, grid_height=10)
    assert str(excinfo.value) == "Grid dimensions must be positive"  # AC-1.5: Zero width

def test_deploy_rover_zero_height_grid():
    with pytest.raises(ValueError) as excinfo:  # Expecting a ValueError
        Rover(grid_width=10, grid_height=0)
    assert str(excinfo.value) == "Grid dimensions must be positive"  # AC-1.5: Zero height

def test_deploy_rover_one_by_one_grid():
    rover = Rover(grid_width=1, grid_height=1)
    assert rover.position == (0, 0)  # AC-1.6: Valid position on 1x1 grid
    assert rover.heading == 'N'  # AC-1.6: Default heading
    assert rover.status == 'ok'  # AC-1.6: Default status
    assert rover.obstacle is None  # AC-1.6: No obstacle

def test_command_forward_north():
    rover = Rover(x=0, y=0, heading='N', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (0, 99)  # AC-2.1: Move forward

def test_command_forward_east():
    rover = Rover(x=0, y=0, heading='E', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (1, 0)  # AC-2.1: Move forward

def test_command_forward_west():
    rover = Rover(x=1, y=0, heading='W', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (0, 0)  # AC-2.1: Move forward and wrap

def test_command_backward():
    rover = Rover(x=1, y=1, heading='E', grid_width=100, grid_height=100)
    rover.execute_commands("b")
    assert rover.position == (0, 1)  # AC-2.2: Move backward, should move west
    assert rover.heading == 'E'  # Heading should remain unchanged

def test_command_sequence():
    rover = Rover(x=0, y=0, heading='S', grid_width=100, grid_height=100)
    rover.execute_commands("fflff")
    assert rover.position == (2, 2)  # AC-2.4: Worked example
    assert rover.heading == 'E'  # AC-2.4: Final heading

def test_command_unknown():
    with pytest.raises(ValueError) as excinfo:  # Expecting a ValueError
        rover = Rover()
        rover.execute_commands("x")
    assert str(excinfo.value) == "Unknown command: x"  # AC-2.5: Unknown command

def test_turn_left_full_cycle():
    rover = Rover(heading='N')
    rover.execute_commands("l")
    assert rover.heading == 'W'  # AC-3.1: Turn left
    rover.execute_commands("l")
    assert rover.heading == 'S'  # Turn left
    rover.execute_commands("l")
    assert rover.heading == 'E'  # Turn left
    rover.execute_commands("l")
    assert rover.heading == 'N'  # Turn left back to N

def test_turn_right_full_cycle():
    rover = Rover(heading='N')
    rover.execute_commands("r")
    assert rover.heading == 'E'  # AC-3.2: Turn right
    rover.execute_commands("r")
    assert rover.heading == 'S'  # Turn right
    rover.execute_commands("r")
    assert rover.heading == 'W'  # Turn right
    rover.execute_commands("r")
    assert rover.heading == 'N'  # Turn right back to N

def test_edge_wrap_north():
    rover = Rover(x=0, y=0, heading='N', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (0, 99)  # AC-4.1: Wrap from top to bottom

def test_edge_wrap_south():
    rover = Rover(x=0, y=99, heading='S', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (0, 0)  # AC-4.2: Wrap from bottom to top

def test_edge_wrap_east():
    rover = Rover(x=99, y=0, heading='E', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (0, 0)  # AC-4.3: Wrap from right to left

def test_edge_wrap_west():
    rover = Rover(x=0, y=0, heading='W', grid_width=100, grid_height=100)
    rover.execute_commands("f")
    assert rover.position == (99, 0)  # AC-4.4: Wrap from left to right

def test_backward_wrap_north():
    rover = Rover(x=0, y=0, heading='N', grid_width=100, grid_height=100)
    rover.execute_commands("b")
    assert rover.position == (0, 99)  # AC-4.5: Backward wrap from North

def test_backward_wrap_south():
    rover = Rover(x=0, y=99, heading='S', grid_width=100, grid_height=100)
    rover.execute_commands("b")
    assert rover.position == (0, 0)  # AC-4.5: Backward wrap from South

def test_backward_wrap_east():
    rover = Rover(x=99, y=0, heading='E', grid_width=100, grid_height=100)
    rover.execute_commands("b")
    assert rover.position == (98, 0)  # AC-4.5: Backward move without wrapping

def test_backward_wrap_west():
    rover = Rover(x=0, y=0, heading='W', grid_width=100, grid_height=100)
    rover.execute_commands("b")
    assert rover.position == (1, 0)  # AC-4.5: Backward wrap from West

def test_one_by_one_grid_forward():
    rover = Rover(grid_width=1, grid_height=1)
    rover.execute_commands("f")
    assert rover.position == (0, 0)  # AC-4.6: Stays in place
    assert rover.status == 'ok'  # AC-4.6: Status stays ok

def test_obstacle_blocked_move():
    rover = Rover(x=1, y=1, heading='E', grid_width=3, grid_height=3)
    rover.set_obstacle((2, 1))  # Set an obstacle
    rover.execute_commands("ff")
    assert rover.position == (1, 1)  # AC-5.1: Should remain blocked
    assert rover.status == 'blocked'  # AC-5.1: Status should be blocked
    assert rover.obstacle == (2, 1)  # AC-5.1: Last obstacle recorded

def test_obstacle_no_command_execution():
    rover = Rover(x=1, y=1, heading='E', grid_width=3, grid_height=3)
    rover.set_obstacle((2, 1))  # Set an obstacle
    rover.execute_commands("ff")
    assert rover.position == (1, 1)  # AC-5.2: Remains at last valid position
    assert rover.status == 'blocked'  # AC-5.2: Status should be blocked
    rover.execute_commands("f")  # Trying to execute more commands
    assert rover.position == (1, 1)  # Should still be in the same position

def test_obstacle_near_but_not_blocked():
    rover = Rover(x=1, y=1, heading='E', grid_width=3, grid_height=3)
    rover.set_obstacle((2, 1))  # Set an obstacle
    rover.execute_commands("f")  # Move to (2, 1)
    assert rover.position == (1, 1)  # Should stop before the obstacle
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.obstacle == (2, 1)  # Last obstacle recorded

def test_obstacle_turning():
    rover = Rover(x=1, y=1, heading='E', grid_width=3, grid_height=3)
    rover.set_obstacle((2, 1))  # Set an obstacle
    rover.execute_commands("l")  # Turn left
    assert rover.heading == 'N'  # Should turn without issues
    rover.execute_commands("f")  # Move north
    assert rover.position == (1, 0)  # Move normally
    assert rover.status == 'ok'  # Status should be ok

def test_obstacle_blocked_command_string():
    rover = Rover(x=1, y=1, heading='E', grid_width=3, grid_height=3)
    rover.set_obstacle((2, 1))  # Set an obstacle
    rover.execute_commands("flr")  # First move is blocked
    assert rover.position == (1, 1)  # Should remain at (1, 1)
    assert rover.heading == 'E'  # Heading should be unchanged
    assert rover.status == 'blocked'  # Status should be blocked