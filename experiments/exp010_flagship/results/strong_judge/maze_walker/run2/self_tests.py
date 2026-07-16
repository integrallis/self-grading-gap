import pytest
from solution import parse_maze, solve_maze

def test_parse_maze_valid():
    maze = "\n#####\n#S E#\n#####"
    parsed = parse_maze(maze)
    assert parsed['width'] == 5  # 5 columns
    assert parsed['height'] == 3  # 3 rows
    assert parsed['start'] == (1, 1)  # Start at (1, 1)
    assert parsed['exit'] == (3, 1)  # Exit at (3, 1)
    assert parsed['is_open']((1, 1)) == True  # Start is open
    assert parsed['is_open']((0, 0)) == False  # Wall is closed
    assert parsed['is_open']((2, 1)) == True  # Open corridor
    assert parsed['is_open']((3, 1)) == True  # Exit is open
    assert parsed['is_open']((4, 1)) == False  # Wall is closed

def test_parse_maze_invalid_missing_start():
    maze = "\n#####\n# E #\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_invalid_missing_exit():
    maze = "\n#####\n#S  #\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_invalid_multiple_starts():
    maze = "\n#####\n#S S#\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_invalid_multiple_exits():
    maze = "\n#####\n#S E E#\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_invalid_unknown_character():
    maze = "\n#####\n#S @#\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_invalid_edge_unknown_character():
    maze = "\n#####\n#S #\n#@E#\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_invalid_corner_unknown_character():
    maze = "\n#####\n#S #\n#E@#\n#####"
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_leading_spaces_retained():
    maze = "\n    #####\n    # S E#\n    #####"
    parsed = parse_maze(maze)
    assert parsed['width'] == 9  # 9 columns due to leading spaces
    assert parsed['height'] == 3  # 3 rows
    assert parsed['start'] == (6, 1)  # Start at (6, 1)
    assert parsed['exit'] == (8, 1)  # Exit at (8, 1)
    assert parsed['is_open']((5, 1)) == True  # Open corridor
    assert parsed['is_open']((6, 1)) == True  # Start is open

def test_parse_maze_trailing_blank_lines_dropped():
    maze = "\n\n#####\n#S E#\n#####\n\n"
    parsed = parse_maze(maze)
    assert parsed['width'] == 5  # 5 columns
    assert parsed['height'] == 3  # 3 rows

def test_parse_maze_multiple_blank_lines_dropped():
    maze = "\n\n\n#####\n#S E#\n#####\n\n\n"
    parsed = parse_maze(maze)
    assert parsed['width'] == 5  # 5 columns
    assert parsed['height'] == 3  # 3 rows

def test_solve_maze_valid():
    maze = "\n#####\n#S E#\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (2, 1), (3, 1)]  # From start to exit

def test_solve_maze_start_beside_exit():
    maze = "\n#####\n#SE #\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (2, 1)]  # Start to exit

def test_solve_maze_no_path_to_exit():
    maze = "\n#####\n#S*E#\n#####"
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_diagonal_unreachable_exit():
    maze = "\n#####\n#S ##\n##E#\n#####"
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_walled_off_exit():
    maze = "\n#####\n#S*E#\n#####"
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_multiple_routes():
    maze = "\n#####\n#S  #\n# E#\n#####"
    route = solve_maze(maze)
    assert route[0] == (1, 1)  # Start at (1, 1)
    assert route[-1] == (2, 2)  # Exit at (2, 2)
    assert len(route) == 3  # Length of route is 3
    assert (2, 1) in route  # Intermediate step must be included

def test_solve_maze_route_with_turn():
    maze = "\n#####\n#S  #\n# E#\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (1, 2), (2, 2)]  # Route with a turn

def test_solve_maze_route_around_dividing_wall():
    maze = "\n#####\n#S*E#\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (1, 2), (2, 2)]  # Route around wall

def test_solve_maze_route_upward_movement():
    maze = "\n#####\n# S #\n# E #\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (1, 0), (1, 2)]  # Route going upward

def test_solve_maze_dot_corridor():
    maze = "\n#####\n#S.E#\n#####"
    route = solve_maze(maze)
    assert route == [(1, 1), (2, 1), (3, 1)]  # Dot is treated like space