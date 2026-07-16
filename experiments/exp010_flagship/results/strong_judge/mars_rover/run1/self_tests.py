import pytest
from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'       # Facing North
    assert rover.status == 'ok'       # Status is ok
    assert rover.last_obstacle is None # No obstacle recorded

def test_deploy_with_valid_arguments():
    rover = Rover(x=5, y=10, heading='E')
    assert rover.position == (5, 10)  # Deployed at (5, 10)
    assert rover.heading == 'E'        # Facing East
    assert rover.status == 'ok'        # Status is ok
    assert rover.last_obstacle is None # No obstacle recorded

def test_deploy_with_case_insensitive_heading():
    rover = Rover(heading='s')
    assert rover.heading == 'S'        # Heading is reported as uppercase S

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError, match="Unknown direction: Z"):
        Rover(heading='Z')

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(width=0, height=100)

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(width=100, height=0)

def test_deploy_with_one_by_one_grid():
    rover = Rover(width=1, height=1)
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'       # Facing North
    assert rover.status == 'ok'       # Status is ok
    assert rover.last_obstacle is None # No obstacle recorded

def test_default_grid_size():
    rover = Rover()
    rover.drive('f')  # Move north from (0, 0)
    assert rover.position[1] == 99  # Should wrap to (0, 99)

def test_drive_forward():
    rover = Rover(width=100, height=100, heading='N')
    rover.drive('f')
    assert rover.position == (0, 99)  # Moves forward to (0, 99)
    assert rover.heading == 'N'       # Heading remains N
    assert rover.status == 'ok'       # Status is ok

def test_drive_backward():
    rover = Rover(width=100, height=100, heading='N')
    rover.drive('b')
    assert rover.position == (0, 1)   # Moves backward to (0, 1)
    assert rover.heading == 'N'        # Heading remains N
    assert rover.status == 'ok'        # Status is ok

def test_drive_command_string():
    rover = Rover(width=100, height=100, heading='S')
    rover.drive('fflff')
    assert rover.position == (2, 2)   # Ends at (2, 2)
    assert rover.heading == 'E'        # Facing East
    assert rover.status == 'ok'        # Status is ok

def test_drive_unknown_command():
    rover = Rover()
    with pytest.raises(ValueError, match="Unknown command: x"):
        rover.drive('fxyz')

def test_turn_left():
    rover = Rover()
    rover.turn('l')
    assert rover.heading == 'W'       # Turns left to West

def test_turn_right():
    rover = Rover()
    rover.turn('r')
    assert rover.heading == 'E'        # Turns right to East

def test_edge_wrap_north():
    rover = Rover(width=100, height=100, heading='N', position=(0, 0))
    rover.drive('f')
    assert rover.position == (0, 99)  # Wraps to the bottom row

def test_edge_wrap_south():
    rover = Rover(width=100, height=100, heading='S', position=(0, 99))
    rover.drive('f')
    assert rover.position == (0, 0)   # Wraps to the top row

def test_edge_wrap_east():
    rover = Rover(width=100, height=100, heading='E', position=(99, 0))
    rover.drive('f')
    assert rover.position == (0, 0)   # Wraps to the left column

def test_edge_wrap_west():
    rover = Rover(width=100, height=100, heading='W', position=(0, 0))
    rover.drive('f')
    assert rover.position == (99, 0)  # Wraps to the right column

def test_obstacle_blocked_move():
    rover = Rover(width=100, height=100, position=(0, 0), heading='N')
    rover.set_obstacle((0, 99))  # Place an obstacle at (0, 99)
    rover.drive('f')
    assert rover.position == (0, 0)  # Remains at (0, 0)
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Records obstacle

def test_blocked_command_halts_remaining_commands():
    rover = Rover(width=100, height=100, position=(0, 0), heading='N')
    rover.set_obstacle((0, 99))  # Place an obstacle at (0, 99)
    rover.drive('flf')  # Attempt to drive forward, then left
    assert rover.position == (0, 0)  # Still at (0, 0)
    assert rover.heading == 'N'       # Heading remains North
    assert rover.status == 'blocked'  # Status is blocked

def test_backwards_edge_wrap_north():
    rover = Rover(width=100, height=100, heading='N', position=(0, 1))
    rover.drive('b')
    assert rover.position == (0, 0)  # Moves to the top row

def test_backwards_edge_wrap_south():
    rover = Rover(width=100, height=100, heading='S', position=(0, 0))
    rover.drive('b')
    assert rover.position == (0, 99)  # Moves to the bottom row

def test_one_by_one_grid_forward_move():
    rover = Rover(width=1, height=1)
    rover.drive('f')
    assert rover.position == (0, 0)  # Remains at (0, 0)
    assert rover.status == 'ok'       # Status is ok

def test_blocked_wrap_destination():
    rover = Rover(width=100, height=100, position=(0, 0), heading='N')
    rover.set_obstacle((0, 99))  # Place an obstacle at (0, 99)
    rover.drive('f')
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Records obstacle

def test_no_error_on_obstacle_collision():
    rover = Rover(width=100, height=100, position=(0, 0), heading='N')
    rover.set_obstacle((0, 99))  # Place an obstacle at (0, 99)
    rover.drive('f')  # Should not raise an error
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 99)  # Records obstacle

def test_near_obstacle_state():
    rover = Rover(width=100, height=100, position=(0, 0), heading='N')
    rover.set_obstacle((0, 99))  # Place an obstacle at (0, 99)
    rover.drive('b')  # Move south to (0, 1)
    assert rover.status == 'ok'  # Status remains ok
    assert rover.last_obstacle is None  # No obstacle recorded

def test_surrounded_rover_turning():
    rover = Rover(width=100, height=100, position=(1, 1), heading='N')
    rover.set_obstacle((0, 1))
    rover.set_obstacle((1, 0))
    rover.set_obstacle((1, 2))
    rover.set_obstacle((2, 1))
    rover.turn('l')  # Should still be able to turn
    assert rover.heading == 'W'  # Heading should change to West
    rover.turn('r')  # Should still be able to turn
    assert rover.heading == 'N'  # Heading should change back to North