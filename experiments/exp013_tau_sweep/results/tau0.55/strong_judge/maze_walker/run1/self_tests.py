import pytest
from solution import parse_maze, solve_maze

def test_parse_maze_valid():
    maze_input = """
    #####
    # S #
    #   #
    # E #
    #####
    """
    parsed_maze = parse_maze(maze_input)
    # width = 9, height = 5, start = (6, 1), exit = (6, 3)
    assert parsed_maze['width'] == 9
    assert parsed_maze['height'] == 5
    assert parsed_maze['start'] == (6, 1)
    assert parsed_maze['exit'] == (6, 3)

def test_parse_maze_multiple_starts():
    maze_input = """
    #####
    # S #
    # S #
    # E #
    #####
    """
    with pytest.raises(ValueError, match=r"^Maze must contain exactly one start 'S'$"):
        parse_maze(maze_input)

def test_parse_maze_missing_start():
    maze_input = """
    #####
    #   #
    # E #
    #####
    """
    with pytest.raises(ValueError, match=r"^Maze must contain exactly one start 'S'$"):
        parse_maze(maze_input)

def test_parse_maze_multiple_exits():
    maze_input = """
    #####
    # S #
    # E #
    # E #
    #####
    """
    with pytest.raises(ValueError, match=r"^Maze must contain exactly one exit 'E'$"):
        parse_maze(maze_input)

def test_parse_maze_missing_exit():
    maze_input = """
    #####
    # S #
    #   #
    #####
    """
    with pytest.raises(ValueError, match=r"^Maze must contain exactly one exit 'E'$"):
        parse_maze(maze_input)

def test_parse_maze_invalid_character():
    maze_input = """
    #####
    # S #
    # X #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Unknown maze character"):
        parse_maze(maze_input)

def test_parse_maze_invalid_character_at_edges():
    maze_input = """
    ####X
    # S #
    #   #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Unknown maze character"):
        parse_maze(maze_input)

def test_parse_maze_invalid_character_at_corners():
    maze_input = """
    ###X#
    # S #
    #   #
    # E #
    #####
    """
    with pytest.raises(ValueError, match="Unknown maze character"):
        parse_maze(maze_input)

def test_parse_maze_blank_lines_removed():
    maze_input = """
    
    #####
    # S #
    #   #
    # E #
    #####
    
    """
    parsed_maze = parse_maze(maze_input)
    # width = 9, height = 5, start = (6, 1), exit = (6, 3)
    assert parsed_maze['width'] == 9
    assert parsed_maze['height'] == 5
    assert parsed_maze['start'] == (6, 1)
    assert parsed_maze['exit'] == (6, 3)

def test_solve_maze_valid_route():
    maze_input = """
    #####
    # S #
    #   #
    # E #
    #####
    """
    route = solve_maze(maze_input)
    # expected route is [(6, 1), (6, 2), (6, 3)]
    assert route == [(6, 1), (6, 2), (6, 3)]

def test_solve_maze_exit_walled():
    maze_input = """
    #####
    # S #
    # # #
    # E #
    #####
    """
    with pytest.raises(ValueError, match=r"^No path to exit$"):
        solve_maze(maze_input)

def test_solve_maze_diagonal_exit_unreachable():
    maze_input = """
    #####
    # S #
    #   #
    #   #
    # E #
    #####
    """
    with pytest.raises(ValueError, match=r"^No path to exit$"):
        solve_maze(maze_input)

def test_solve_maze_multiple_routes():
    maze_input = """
    #######
    # S   #
    # ### #
    #     #
    # E   #
    #######
    """
    route = solve_maze(maze_input)
    # expected route is [(6,1), (5,1), (5,2), (5,3), (6,3), (6,4)]
    assert route == [(6,1), (5,1), (5,2), (5,3), (6,3), (6,4)]

def test_solve_maze_adjacency_exit():
    maze_input = """
    #####
    # S E#
    #####
    """
    route = solve_maze(maze_input)
    # expected route is [(6, 1), (6, 2)]
    assert route == [(6, 1), (6, 2)]

def test_solve_maze_route_property():
    maze_input = """
    #######
    # S   #
    # ### #
    #     #
    # E   #
    #######
    """
    route = solve_maze(maze_input)
    for i in range(len(route) - 1):
        assert (abs(route[i][0] - route[i + 1][0]) + abs(route[i][1] - route[i + 1][1])) == 1

def test_solve_maze_upward_movement():
    maze_input = """
    #####
    #   #
    # S #
    # E #
    #####
    """
    route = solve_maze(maze_input)
    assert route == [(6, 1), (6, 2), (6, 3)]

def test_solve_maze_using_dot():
    maze_input = """
    #######
    # S . #
    # ### #
    #     #
    # E   #
    #######
    """
    route = solve_maze(maze_input)
    assert route == [(6,1), (6,2), (6,3), (6,4)]

def test_solve_maze_unreachable_exit_walled():
    maze_input = """
    #######
    # S   #
    # ### #
    #     #
    # ###E#
    #######
    """
    with pytest.raises(ValueError, match=r"^No path to exit$"):
        solve_maze(maze_input)

def test_solve_maze_unreachable_exit_star():
    maze_input = """
    #######
    # S   #
    # ### #
    #     #
    # * *E#
    #######
    """
    with pytest.raises(ValueError, match=r"^No path to exit$"):
        solve_maze(maze_input)