from solution import Rover
import pytest

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_valid_arguments():
    rover = Rover(5, 5, 'E')
    assert rover.position == (0, 0)  # Default position
    assert rover.heading == 'E'  # Facing East
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_case_insensitive_heading():
    rover = Rover(5, 5, 's')
    assert rover.heading == 'S'  # Should be treated as South

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError, match="Unknown direction: x"):
        Rover(5, 5, 'x')  # x is an unknown direction

def test_deploy_with_zero_grid_dimensions():
    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(0, 5)  # Zero width

    with pytest.raises(ValueError, match="Grid dimensions must be positive"):
        Rover(5, 0)  # Zero height

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    assert rover.position == (0, 0)  # Position should be (0, 0)
    assert rover.heading == 'N'  # Facing North

def test_move_forward():
    rover = Rover(100, 100, 'N')
    rover.move('f')  # Move forward
    assert rover.position == (0, 1)  # New position should be (0, 1)

def test_move_backward():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('b')  # Move backward
    assert rover.position == (0, 99)  # New position should wrap to (0, 99)

def test_command_string_execution():
    rover = Rover(100, 100, 'S')
    rover.move('fflff')  # Move command string
    assert rover.position == (2, 2)  # Final position should be (2, 2)
    assert rover.heading == 'E'  # Final heading should be East

def test_unknown_command():
    rover = Rover(100, 100, 'N')
    with pytest.raises(ValueError, match="Unknown command: z"):
        rover.move('fz')  # z is an unknown command

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.move('l')  # Turn left
    assert rover.heading == 'W'  # Heading should be West

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.move('r')  # Turn right
    assert rover.heading == 'E'  # Heading should be East

def test_edge_wrapping_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('f')  # Move north off the edge
    assert rover.position == (0, 99)  # Should wrap to (0, 99)

def test_edge_wrapping_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.move('f')  # Move south off the edge
    assert rover.position == (0, 0)  # Should wrap to (0, 0)

def test_edge_wrapping_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.move('f')  # Move east off the edge
    assert rover.position == (0, 0)  # Should wrap to (0, 0)

def test_edge_wrapping_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.move('f')  # Move west off the edge
    assert rover.position == (99, 0)  # Should wrap to (99, 0)

def test_obstacle_blocking_move():
    rover = Rover(100, 100, 'N', obstacles={(0, 1)})
    rover.position = (0, 0)
    rover.move('f')  # Move into an obstacle
    assert rover.position == (0, 0)  # Should remain at (0, 0)
    assert rover.status == 'blocked'  # Status should be blocked
    assert rover.last_obstacle == (0, 1)  # Last obstacle should be recorded

def test_obstacle_nearby():
    rover = Rover(100, 100, 'N', obstacles={(0, 1)})
    rover.position = (0, 0)
    rover.move('b')  # Move backward (no obstacle)
    assert rover.position == (0, 99)  # Should wrap to (0, 99)
    assert rover.status == 'ok'  # Status should remain ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_turning_with_obstacles():
    rover = Rover(100, 100, 'N', obstacles={(0, 1)})
    rover.position = (0, 0)
    rover.move('l')  # Turn left
    assert rover.heading == 'W'  # Should turn left regardless of obstacles