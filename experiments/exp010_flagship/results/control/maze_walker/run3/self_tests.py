# test_maze_solver.py

import pytest
from solution import parse_maze, solve_maze

def test_parse_maze_valid():
    maze_text = """
    #####
    # S #
    #   #
    # E #
    #####
    """
    maze = parse_maze(maze_text)
    assert maze.width == 5  # Width is 5 characters
    assert maze.height == 5  # Height is 5 lines
    assert maze.start == (2, 1)  # Start 'S' is at (2, 1)
    assert maze.exit == (2, 3)  # Exit 'E' is at (2, 3)
    assert maze.is_open(1, 1)  # (1, 1) is a wall
    assert maze.is_open(2, 2)  # (2, 2) is a corridor

def test_parse_maze_missing_start():
    maze_text = """
    #####
    #   #
    #   #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Maze must contain exactly one start 'S'"):
        parse_maze(maze_text)

def test_parse_maze_multiple_starts():
    maze_text = """
    #####
    # S #
    # S #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Maze must contain exactly one start 'S'"):
        parse_maze(maze_text)

def test_parse_maze_missing_exit():
    maze_text = """
    #####
    # S #
    #   #
    #   #
    #####
    """
    with pytest.raises(ValueError, match="Maze must contain exactly one exit 'E'"):
        parse_maze(maze_text)

def test_parse_maze_multiple_exits():
    maze_text = """
    #####
    # S #
    # E #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Maze must contain exactly one exit 'E'"):
        parse_maze(maze_text)

def test_parse_maze_invalid_character():
    maze_text = """
    #####
    # S #
    # @ #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Unknown maze character"):
        parse_maze(maze_text)

def test_solve_maze_shortest_path():
    maze_text = """
    #####
    # S #
    #   #
    # E #
    #####
    """
    maze = parse_maze(maze_text)
    path = solve_maze(maze)
    expected_path = [(2, 1), (2, 2), (2, 3)]  # Path from (2, 1) to (2, 3)
    assert path == expected_path

def test_solve_maze_exit_adjacent():
    maze_text = """
    #####
    # S E#
    #####
    """
    maze = parse_maze(maze_text)
    path = solve_maze(maze)
    expected_path = [(2, 1), (3, 1)]  # Path from (2, 1) to (3, 1)
    assert path == expected_path

def test_solve_maze_no_path():
    maze_text = """
    #####
    # S #
    # # #
    # E #
    #####
    """
    maze = parse_maze(maze_text)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(maze)

def test_solve_maze_diagonal_unreachable():
    maze_text = """
    #####
    # S #
    #   #
    #   #
    # E #
    #####
    """
    maze = parse_maze(maze_text)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(maze)

def test_solve_maze_walled_exit():
    maze_text = """
    #####
    # S #
    # # #
    #   #
    # E #
    #####
    """
    maze = parse_maze(maze_text)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(maze)