from solution import Rover

def test_deploy_without_arguments():
    rover = Rover()
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_valid_arguments():
    rover = Rover(5, 5, 'E')
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'E'  # Facing East
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_deploy_with_lowercase_heading():
    rover = Rover(5, 5, 's')
    assert rover.heading == 'S'  # Heading is reported as uppercase

def test_deploy_with_unknown_heading():
    with pytest.raises(ValueError) as excinfo:
        Rover(5, 5, 'X')
    assert str(excinfo.value) == "Unknown direction: X"

def test_deploy_with_zero_width_grid():
    with pytest.raises(ValueError) as excinfo:
        Rover(0, 5, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_zero_height_grid():
    with pytest.raises(ValueError) as excinfo:
        Rover(5, 0, 'N')
    assert str(excinfo.value) == "Grid dimensions must be positive"

def test_deploy_with_one_by_one_grid():
    rover = Rover(1, 1, 'N')
    assert rover.position == (0, 0)  # Deployed at (0, 0)
    assert rover.heading == 'N'  # Facing North
    assert rover.status == 'ok'  # Status is ok
    assert rover.last_obstacle is None  # No obstacle on record

def test_move_forward():
    rover = Rover(100, 100, 'N')
    rover.move('f')
    assert rover.position == (0, 1)  # Moved to (0, 1)
    assert rover.heading == 'N'  # Heading remains the same

def test_move_backward():
    rover = Rover(100, 100, 'N')
    rover.move('b')
    assert rover.position == (0, 99)  # Moved to (0, 99)
    assert rover.heading == 'N'  # Heading remains the same

def test_command_string_execution():
    rover = Rover(100, 100, 'S')
    rover.execute_commands('fflff')
    assert rover.position == (2, 2)  # Worked example ends at (2, 2)
    assert rover.heading == 'E'  # Ends facing East

def test_unknown_command():
    rover = Rover(100, 100, 'N')
    with pytest.raises(ValueError) as excinfo:
        rover.move('z')
    assert str(excinfo.value) == "Unknown command: z"

def test_turn_left():
    rover = Rover(100, 100, 'N')
    rover.turn('l')
    assert rover.heading == 'W'  # Turned to West

def test_turn_right():
    rover = Rover(100, 100, 'N')
    rover.turn('r')
    assert rover.heading == 'E'  # Turned to East

def test_edge_wrap_north():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.move('f')
    assert rover.position == (0, 99)  # Wrapped to the bottom

def test_edge_wrap_south():
    rover = Rover(100, 100, 'S')
    rover.position = (0, 99)
    rover.move('f')
    assert rover.position == (0, 0)  # Wrapped to the top

def test_edge_wrap_east():
    rover = Rover(100, 100, 'E')
    rover.position = (99, 0)
    rover.move('f')
    assert rover.position == (0, 0)  # Wrapped to the left

def test_edge_wrap_west():
    rover = Rover(100, 100, 'W')
    rover.position = (0, 0)
    rover.move('f')
    assert rover.position == (99, 0)  # Wrapped to the right

def test_obstacle_blocking_move():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.add_obstacle((0, 1))  # Add an obstacle at (0, 1)
    rover.move('f')
    assert rover.position == (0, 0)  # Remains at (0, 0)
    assert rover.status == 'blocked'  # Status is blocked
    assert rover.last_obstacle == (0, 1)  # Last obstacle recorded

def test_obstacle_ignored_on_turn():
    rover = Rover(100, 100, 'N')
    rover.position = (0, 0)
    rover.add_obstacle((0, 1))
    rover.turn('l')  # Turn left should not be blocked
    assert rover.heading == 'W'  # Heading should change
    assert rover.status == 'ok'  # Status should remain ok