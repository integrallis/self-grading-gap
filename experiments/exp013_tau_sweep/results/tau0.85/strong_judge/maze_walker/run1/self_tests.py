import pytest
from solution import parse_maze, solve_maze
import textwrap

def test_parse_maze_valid():
    maze = textwrap.dedent("""
    #####
    #S E#
    #####
    """)
    result = parse_maze(maze)
    expected = {
        'width': 9,  # 9 characters wide (5 + 4)
        'height': 3,  # 3 lines tall
        'start': (5, 1),  # Start at (5,1)
        'exit': (7, 1),  # Exit at (7,1)
        'is_open': lambda x, y: (x, y) in {(5, 1), (7, 1), (6, 1), (0, 0), (0, 1)}  # Open if it's S, E, or space
    }
    assert result['width'] == expected['width']
    assert result['height'] == expected['height']
    assert result['start'] == expected['start']
    assert result['exit'] == expected['exit']
    assert result['is_open'](5, 1)  # S is open
    assert result['is_open'](7, 1)  # E is open
    assert result['is_open'](6, 1)  # space is open
    assert not result['is_open'](0, 0)  # wall is not open
    assert not result['is_open'](0, 1)  # wall is not open

def test_parse_maze_multiple_starts():
    maze = textwrap.dedent("""
    #####
    #SS E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_no_start():
    maze = textwrap.dedent("""
    #####
    # E #
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_multiple_exits():
    maze = textwrap.dedent("""
    #####
    #S E E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_no_exit():
    maze = textwrap.dedent("""
    #####
    #S  #
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_invalid_character():
    maze = textwrap.dedent("""
    #####
    #S@E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_with_leading_spaces():
    maze = textwrap.dedent("""
    #####
    # S E#
    #     #
    #####
    """)
    result = parse_maze(maze)
    expected = {
        'width': 9,  # 9 characters wide, including leading spaces
        'height': 4,  # 4 lines tall
        'start': (2, 1),  # Start at (2,1)
        'exit': (4, 1),  # Exit at (4,1)
    }
    assert result['width'] == expected['width']
    assert result['height'] == expected['height']
    assert result['start'] == expected['start']
    assert result['exit'] == expected['exit']

def test_solve_maze_direct_route():
    maze = textwrap.dedent("""
    #####
    #S E#
    #####
    """)
    result = solve_maze(maze)
    expected = [(5, 1), (6, 1), (7, 1)]  # Start to exit (3 coordinates)
    assert result == expected

def test_solve_maze_directly_adjacent():
    maze = textwrap.dedent("""
    #####
    #SE #
    #####
    """)
    result = solve_maze(maze)
    expected = [(5, 1), (6, 1)]  # Start to exit (2 coordinates)
    assert result == expected

def test_solve_maze_no_path():
    maze = textwrap.dedent("""
    #####
    #S#E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_around_walls():
    maze = textwrap.dedent("""
    #####
    #S  #
    # ##E
    #####
    """)
    result = solve_maze(maze)
    expected = [(5, 1), (5, 2), (6, 2), (7, 2)]  # Start to exit navigating around walls
    assert result == expected

def test_solve_maze_diagonal_touching():
    maze = textwrap.dedent("""
    #####
    #S#E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_with_dots():
    maze = textwrap.dedent("""
    #####
    #S E#
    #.#.#
    #####
    """)
    result = solve_maze(maze)
    expected = [(5, 1), (6, 1), (7, 1)]  # Start to exit via space (3 coordinates)
    assert result == expected

def test_solve_maze_with_multiple_routes():
    maze = textwrap.dedent("""
    #####
    #S  #
    # #E#
    #####
    """)
    result = solve_maze(maze)
    assert result[0] == (5, 1)  # Should start at S
    assert result[-1] == (7, 2)  # Should end at E
    assert all((x, y) in [(5, 1), (5, 2), (6, 2), (7, 2)] for (x, y) in result)  # Ensure all in route are valid

def test_solve_maze_unreachable_exit_with_star():
    maze = textwrap.dedent("""
    #####
    #S*E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_diagonal_no_connection():
    maze = textwrap.dedent("""
    #####
    #S#E#
    #####
    """)
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"