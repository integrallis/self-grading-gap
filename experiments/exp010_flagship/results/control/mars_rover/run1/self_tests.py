from solution import Rover
import pytest

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at starting position
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.obstacle is None  # No obstacles on record

def test_deploy_with_valid_arguments():
    rover = Rover((5, 5), 'E', (10, 10))
    assert rover.position == (5, 5)  # Deployed at (5, 5)
    assert rover.heading == 'E'  # Facing East
    assert rover.status == 'ok'  # Status is ok
    assert rover.obstacle is None  # No obstacles on record

def test_deploy_with_lowercase_heading():
    rover = Rover((0, 0), 's', (100, 100))
    assert rover.heading == 'S'  # Should be reported as uppercase

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError, match="Unknown direction: x"):
        Rover((0, 0), 'x', (100, 100))

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover((0, 0), 'N', (0, 100))

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover((0, 0), 'N', (100, 0))

def test_deploy_with_one_by_one_grid():
    rover = Rover((0, 0), 'N', (1, 1))
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.obstacle is None  # No obstacles on record

def test_command_forward():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.execute_commands('f')
    assert rover.position == (0, 1)  # Moves from (0, 0) to (0, 1)
    assert rover.heading == 'N'  # Heading remains the same
    assert rover.status == 'ok'  # Status is ok

def test_command_backward():
    rover = Rover((0, 1), 'N', (100, 100))
    rover.execute_commands('b')
    assert rover.position == (0, 0)  # Moves from (0, 1) to (0, 0)
    assert rover.heading == 'N'  # Heading remains the same
    assert rover.status == 'ok'  # Status is ok

def test_command_sequence():
    rover = Rover((0, 0), 'S', (100, 100))
    rover.execute_commands('fflff')
    assert rover.position == (2, 2)  # Final position after commands
    assert rover.heading == 'E'  # Final heading after commands
    assert rover.status == 'ok'  # Status is ok

def test_command_unknown_command():
    rover = Rover((0, 0), 'N', (100, 100))
    with pytest.raises(ValueError, match="Unknown command: z"):
        rover.execute_commands('fz')

def test_turn_left():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.execute_commands('l')
    assert rover.heading == 'W'  # Turns from N to W

def test_turn_right():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.execute_commands('r')
    assert rover.heading == 'E'  # Turns from N to E

def test_edge_wrap_north():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.execute_commands('f' * 100)  # Move 100 times north
    assert rover.position == (0, 99)  # Final position should wrap to (0, 99)

def test_obstacle_blockage():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.set_obstacle((0, 1))  # Set obstacle at (0, 1)
    rover.execute_commands('f')  # This should block the rover
    assert rover.position == (0, 0)  # Should not move
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.obstacle == (0, 1)  # Last encountered obstacle

def test_obstacle_no_error_on_turn():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.set_obstacle((0, 1))  # Set obstacle at (0, 1)
    rover.execute_commands('l')  # Turning should not be blocked
    assert rover.heading == 'W'  # Should turn to West
    assert rover.position == (0, 0)  # Should remain at (0, 0)
    assert rover.status == 'ok'  # Status should be ok

def test_edge_wrap_with_obstacle():
    rover = Rover((99, 0), 'E', (100, 100))
    rover.set_obstacle((0, 0))  # Set obstacle at (0, 0)
    rover.execute_commands('f')  # Should move to (0, 0) but blocked
    assert rover.position == (99, 0)  # Should not move
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.obstacle == (0, 0)  # Last encountered obstacle

def test_backward_wrap():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.execute_commands('b')  # Moving backward from (0,0) should wrap
    assert rover.position == (0, 99)  # Wraps to (0, 99)
    assert rover.status == 'ok'  # Status should be ok

def test_backward_wrap_with_obstacle():
    rover = Rover((0, 0), 'N', (100, 100))
    rover.set_obstacle((0, 99))  # Set obstacle at (0, 99)
    rover.execute_commands('b')  # Should try to move to (0, 99) but blocked
    assert rover.position == (0, 0)  # Should not move
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.obstacle == (0, 99)  # Last encountered obstacle