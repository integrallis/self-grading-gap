import pytest
from solution import parse_maze, solve_maze

# Test suite for maze solving from text art

# US-1: Reading the drawing

def test_parse_maze_valid():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    #####
    """
    maze = parse_maze(maze_text)
    # Width: 9, Height: 5, Start: (5, 1), Exit: (7, 3)
    assert maze['width'] == 9
    assert maze['height'] == 5
    assert maze['start'] == (5, 1)
    assert maze['exit'] == (7, 3)

def test_parse_maze_multiple_starts():
    maze_text = """
    #####
    #S  #
    #S  #
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"Maze must contain exactly one start 'S'"):
        parse_maze(maze_text)

def test_parse_maze_multiple_exits():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"Maze must contain exactly one exit 'E'"):
        parse_maze(maze_text)

def test_parse_maze_missing_start():
    maze_text = """
    #####
    #   #
    #   #
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"Maze must contain exactly one start 'S'"):
        parse_maze(maze_text)

def test_parse_maze_missing_exit():
    maze_text = """
    #####
    #S  #
    #   #
    #   #
    #####
    """
    with pytest.raises(Exception, match=r"Maze must contain exactly one exit 'E'"):
        parse_maze(maze_text)

def test_parse_maze_unknown_character_interior():
    maze_text = """
    #####
    #S#@#
    #   #
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"Unknown maze character"):
        parse_maze(maze_text)

def test_parse_maze_unknown_character_edge():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    # #@#
    #####
    """
    with pytest.raises(Exception, match=r"Unknown maze character"):
        parse_maze(maze_text)

def test_parse_maze_unknown_character_corner():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    #@###
    """
    with pytest.raises(Exception, match=r"Unknown maze character"):
        parse_maze(maze_text)

def test_parse_maze_blank_lines():
    maze_text = """
    
    #####
    #S  #
    #   #
    #  E#
    #####
    
    """
    maze = parse_maze(maze_text)
    assert maze['start'] == (5, 1)
    assert maze['exit'] == (7, 3)

def test_parse_maze_leading_spaces():
    maze_text = """
    #####
    # S #
    #   #
    #  E#
    #####
    """
    maze = parse_maze(maze_text)
    # Width: 9, Height: 5, Start: (5, 1), Exit: (7, 3)
    assert maze['width'] == 9
    assert maze['height'] == 5
    assert maze['start'] == (5, 1)
    assert maze['exit'] == (7, 3)

def test_parse_maze_cell_query_open():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    #####
    """
    maze = parse_maze(maze_text)
    assert maze['is_open'](5, 1) == False  # Wall
    assert maze['is_open'](5, 2) == True   # Open
    assert maze['is_open'](7, 3) == False  # Wall
    assert maze['is_open'](6, 3) == False  # Wall
    assert maze['is_open'](7, 2) == True   # Open

# US-2: Walking the shortest route

def test_solve_maze_valid_route():
    maze_text = """
    #####
    #S  #
    #   #
    #  E#
    #####
    """
    route = solve_maze(maze_text)
    # The actual shortest route can vary; assert it begins and ends correctly
    assert route[0] == (5, 1)  # Start
    assert route[-1] == (7, 3)  # Exit
    assert all(route[i][0] == route[i+1][0] or route[i][1] == route[i+1][1] for i in range(len(route)-1))  # Orthogonal movement

def test_solve_maze_start_next_to_exit():
    maze_text = """
    #####
    #S E#
    #####
    """
    route = solve_maze(maze_text)
    # Expected route: [(5, 1), (6, 1)]
    assert route[0] == (5, 1)  # Start
    assert route[-1] == (6, 1)  # Exit

def test_solve_maze_no_path_to_exit():
    maze_text = """
    #####
    #S* #
    # # #
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze_text)

def test_solve_maze_exit_walled_off():
    maze_text = """
    #####
    #S  #
    # # #
    #   #
    #####
    """
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze_text)

def test_solve_maze_diagonal_unreachable():
    maze_text = """
    #####
    #S  #
    #   #
    #E  #
    #####
    """
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze_text)

def test_solve_maze_walled_exit():
    maze_text = """
    #####
    #S  #
    #   #
    # #E#
    #####
    """
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze_text)

def test_solve_maze_corner_touching():
    maze_text = """
    #####
    #S# #
    #   #
    #  E#
    #####
    """
    with pytest.raises(Exception, match=r"No path to exit"):
        solve_maze(maze_text)

def test_solve_maze_dot_corridor():
    maze_text = """
    #####
    #S. #
    #   #
    #  E#
    #####
    """
    route = solve_maze(maze_text)
    assert route[0] == (5, 1)  # Start
    assert route[-1] == (7, 3)  # Exit
    assert len(route) > 2  # Must pass through the dot
    assert all(route[i][0] == route[i+1][0] or route[i][1] == route[i+1][1] for i in range(len(route)-1))  # Orthogonal movement

def test_solve_maze_longer_valid_alternative():
    maze_text = """
    #####
    #S  #
    #   #
    #   #
    #  E#
    #####
    """
    route = solve_maze(maze_text)
    assert len(route) == 6  # Assert the shortest route length
    assert route[0] == (5, 1)  # Start
    assert route[-1] == (7, 3)  # Exit