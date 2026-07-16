import pytest
from solution import parse_maze, solve_maze

# Test maze parsing and validation

def test_parse_maze_valid():
    maze_text = """
    #####
    # S #
    #   #
    # E #
    #####"""
    maze = parse_maze(maze_text)
    assert maze['width'] == 5  # 5 columns
    assert maze['height'] == 5  # 5 rows
    assert maze['start'] == (2, 1)  # Start at (2, 1)
    assert maze['exit'] == (2, 3)  # Exit at (2, 3)
    assert maze['cells'][(2, 1)] == 'S'  # Cell (2, 1) is 'S'
    assert maze['cells'][(2, 3)] == 'E'  # Cell (2, 3) is 'E'

def test_parse_maze_multiple_starts():
    maze_text = """
    #####
    # S #
    # S #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_text)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_missing_start():
    maze_text = """
    #####
    #   #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_text)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_multiple_exits():
    maze_text = """
    #####
    # S #
    # E #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_text)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_missing_exit():
    maze_text = """
    #####
    # S #
    #   #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_text)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_invalid_character():
    maze_text = """
    #####
    # S #
    # @ #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_text)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_blank_lines_dropped():
    maze_text = """
    
    #####
    # S #
    #   #
    # E #
    #####
    
    """
    maze = parse_maze(maze_text)
    assert maze['width'] == 5  # 5 columns
    assert maze['height'] == 5  # 5 rows
    assert maze['start'] == (2, 1)  # Start at (2, 1)
    assert maze['exit'] == (2, 3)  # Exit at (2, 3)

def test_solve_maze_shortest_path():
    maze_text = """
    #####
    # S #
    #   #
    # E #
    #####"""
    path = solve_maze(maze_text)
    assert path == [(2, 1), (2, 2), (2, 3)]  # The path should be S -> (2, 2) -> E

def test_solve_maze_no_path():
    maze_text = """
    #####
    # S #
    # # #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        solve_maze(maze_text)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_exit_diagonally_adjacent():
    maze_text = """
    #####
    # S #
    #   #
    #   #
    # E #
    #####"""
    with pytest.raises(ValueError) as excinfo:
        solve_maze(maze_text)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_start_next_to_exit():
    maze_text = """
    #####
    # S E#
    #   #
    #####"""
    path = solve_maze(maze_text)
    assert path == [(2, 1), (3, 1)]  # Path should go directly from S to E

def test_solve_maze_consecutive_coordinates():
    maze_text = """
    #####
    # S #
    #   #
    # E #
    #####"""
    path = solve_maze(maze_text)
    assert path[1][0] == path[0][0]  # Same column
    assert abs(path[1][1] - path[0][1]) == 1  # Adjacent rows

def test_solve_maze_route_around_corners():
    maze_text = """
    #####
    # S #
    #   #
    # #E#
    #####"""
    path = solve_maze(maze_text)
    assert path == [(2, 1), (2, 2), (1, 2), (1, 3), (2, 3)]  # Path should navigate around corner

def test_solve_maze_dot_and_space_corridors():
    maze_text = """
    #####
    # S #
    # . #
    # E #
    #####"""
    path = solve_maze(maze_text)
    assert path == [(2, 1), (2, 2), (2, 3)]  # The path should be S -> (2, 2) -> E