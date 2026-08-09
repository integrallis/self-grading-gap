import pytest
from solution import parse_maze, solve_maze
import textwrap

# Test maze parsing and validation

def test_parse_maze_valid():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    # E #
    #####
    """)
    parsed = parse_maze(maze)
    assert parsed['width'] == 5  # Width is 5 characters
    assert parsed['height'] == 5  # Height is 5 lines
    assert parsed['start'] == (2, 1)  # Start is at (2, 1)
    assert parsed['exit'] == (2, 3)  # Exit is at (2, 3)
    assert parsed['is_open']((2, 1))  # Start is open
    assert parsed['is_open']((2, 3))  # Exit is open
    assert not parsed['is_open']((0, 0))  # (0, 0) is a wall

def test_parse_maze_missing_start():
    maze = textwrap.dedent("""
    #####
    #   #
    #   #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"Maze must contain exactly one start 'S'"):
        parse_maze(maze)

def test_parse_maze_multiple_starts():
    maze = textwrap.dedent("""
    #####
    # S #
    # S #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"Maze must contain exactly one start 'S'"):
        parse_maze(maze)

def test_parse_maze_missing_exit():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    #   #
    #####
    """)
    with pytest.raises(Exception, match=r"Maze must contain exactly one exit 'E'"):
        parse_maze(maze)

def test_parse_maze_multiple_exits():
    maze = textwrap.dedent("""
    #####
    # S #
    # E #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"Maze must contain exactly one exit 'E'"):
        parse_maze(maze)

def test_parse_maze_unknown_character():
    maze = textwrap.dedent("""
    #####
    # S #
    # @ #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"Unknown maze character"):
        parse_maze(maze)

def test_parse_maze_with_blank_lines():
    maze = textwrap.dedent("""
    
    #####
    # S #
    #   #
    # E #
    #####
    
    """)
    parsed = parse_maze(maze)
    assert parsed['width'] == 5
    assert parsed['height'] == 5
    assert parsed['start'] == (2, 1)  # Start is at (2, 1)
    assert parsed['exit'] == (2, 3)  # Exit is at (2, 3)

def test_parse_maze_wall_character():
    maze = textwrap.dedent("""
    #####
    # S #
    # * #
    # E #
    #####
    """)
    parsed = parse_maze(maze)
    assert not parsed['is_open']((2, 2))  # (2, 2) is a wall

def test_parse_maze_unknown_character_edge():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    # E #
    # @ #
    #####
    """)
    with pytest.raises(Exception, match=r"Unknown maze character"):
        parse_maze(maze)

# Test maze solving

def test_solve_maze_valid():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (2, 2), (2, 3)]  # Start to exit coordinates

def test_solve_maze_no_path_to_exit():
    maze = textwrap.dedent("""
    #####
    # S #
    # # #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze)

def test_solve_maze_exit_diagonally_adjacent():
    maze = textwrap.dedent("""
    #####
    # S #
    # # #
    #   #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze)

def test_solve_maze_start_next_to_exit():
    maze = textwrap.dedent("""
    #####
    # S E#
    #   #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (3, 1)]  # Start to exit coordinates

def test_solve_maze_multiple_paths():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    #   #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (2, 2), (2, 3), (2, 4)]  # The shortest path

def test_solve_maze_dot_is_open():
    maze = textwrap.dedent("""
    #####
    # S #
    # . #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (2, 2), (2, 3)]  # Dot is treated as open

def test_solve_maze_no_path_with_star_wall():
    maze = textwrap.dedent("""
    #####
    # S #
    # * #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze)

def test_solve_maze_route_adjacency():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    #   #
    # E #
    #####
    """)
    route = solve_maze(maze)
    for i in range(len(route) - 1):
        assert abs(route[i][0] - route[i + 1][0]) + abs(route[i][1] - route[i + 1][1]) == 1  # Manhattan distance of 1

def test_solve_maze_route_around_corner():
    maze = textwrap.dedent("""
    #####
    # S #
    #   #
    # # #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (2, 2), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3)]  # Route around corner

def test_solve_maze_route_detour_around_wall():
    maze = textwrap.dedent("""
    #####
    # S #
    # * #
    #   #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3)]  # Route around wall

def test_solve_maze_route_upward_movement():
    maze = textwrap.dedent("""
    #####
    #   #
    # S #
    #   #
    # E #
    #####
    """)
    route = solve_maze(maze)
    assert route == [(2, 1), (2, 0), (2, 3)]  # Upward movement from start to exit

def test_solve_maze_no_path_diagonal_only():
    maze = textwrap.dedent("""
    #####
    # S #
    # # #
    #   #
    # E #
    #####
    """)
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze)