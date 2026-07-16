import pytest
from solution import parse_maze, solve_maze

def test_maze_parsing_valid_maze():
    maze = "#####\n# S E#\n#####"
    parsed = parse_maze(maze)
    # Width: 5, Height: 3, Start: (2, 1), Exit: (4, 1)
    assert parsed['width'] == 5
    assert parsed['height'] == 3
    assert parsed['start'] == (2, 1)
    assert parsed['exit'] == (4, 1)

def test_maze_parsing_blank_lines():
    maze = "\n  #####\n  # S E#\n  #####\n"
    parsed = parse_maze(maze)
    # Width: 5, Height: 3, Start: (4, 1), Exit: (6, 1)
    assert parsed['width'] == 7
    assert parsed['height'] == 3
    assert parsed['start'] == (4, 1)
    assert parsed['exit'] == (6, 1)

def test_maze_parsing_multiple_starts():
    maze = "#####\n# S S#\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert str(exc.value) == "Maze must contain exactly one start 'S'"

def test_maze_parsing_missing_start():
    maze = "#####\n#  E#\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert str(exc.value) == "Maze must contain exactly one start 'S'"

def test_maze_parsing_multiple_exits():
    maze = "#####\n# S E#\n#   E#\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert str(exc.value) == "Maze must contain exactly one exit 'E'"

def test_maze_parsing_missing_exit():
    maze = "#####\n# S  #\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert str(exc.value) == "Maze must contain exactly one exit 'E'"

def test_maze_parsing_invalid_character():
    maze = "#####\n# S @#\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert "Unknown maze character" in str(exc.value)

def test_maze_parsing_unknown_character_edge():
    maze = "#####\n# S E@\n#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert "Unknown maze character" in str(exc.value)

def test_maze_parsing_unknown_character_corner():
    maze = "#####\n# S E#\n#   #\n@#####"
    with pytest.raises(Exception) as exc:
        parse_maze(maze)
    assert "Unknown maze character" in str(exc.value)

def test_maze_parsing_star_walls():
    maze = "#####\n# S*E#\n#####"
    parsed = parse_maze(maze)
    # Width: 5, Height: 3, Start: (2, 1), Exit: (4, 1)
    assert parsed['width'] == 5
    assert parsed['height'] == 3
    assert parsed['start'] == (2, 1)
    assert parsed['exit'] == (4, 1)

def test_maze_solving_simple_path():
    maze = "#####\n# S E#\n#####"
    route = solve_maze(maze)
    # Path: [(2, 1), (3, 1), (4, 1)]
    assert route == [(2, 1), (3, 1), (4, 1)]

def test_maze_solving_directly_adjacent_start_exit():
    maze = "#####\n# S E#\n#####"
    route = solve_maze(maze)
    # Path: [(2, 1), (3, 1)]
    assert route == [(2, 1), (3, 1)]

def test_maze_solving_no_path():
    maze = "#####\n# S #E\n#####"
    with pytest.raises(Exception) as exc:
        solve_maze(maze)
    assert str(exc.value) == "No path to exit"

def test_maze_solving_diagonal_unreachable():
    maze = "#####\n# S #\n#   E\n#####"
    with pytest.raises(Exception) as exc:
        solve_maze(maze)
    assert str(exc.value) == "No path to exit"

def test_maze_solving_walled_exit():
    maze = "#####\n# S #\n# #E#\n#####"
    with pytest.raises(Exception) as exc:
        solve_maze(maze)
    assert str(exc.value) == "No path to exit"

def test_maze_solving_multiple_paths():
    maze = "#####\n# S #\n#   #\n# E #\n#####"
    route = solve_maze(maze)
    # Path: [(2, 1), (2, 2), (2, 3), (3, 3)]
    assert route == [(2, 1), (2, 2), (2, 3), (3, 3)]

def test_maze_solving_route_validity():
    maze = "#####\n# S  #\n#   E#\n#####"
    route = solve_maze(maze)
    # Path: [(2, 1), (2, 2), (2, 3), (3, 3)]
    assert route[0] == (2, 1)
    assert route[-1] == (4, 1)
    for i in range(len(route) - 1):
        assert (abs(route[i][0] - route[i + 1][0]) + abs(route[i][1] - route[i + 1][1])) == 1

def test_maze_solving_route_around_corner():
    maze = "#####\n# S #\n#   E#\n#####"
    route = solve_maze(maze)
    # Path should go around the wall
    assert route == [(2, 1), (2, 2), (3, 2), (4, 2)]

def test_maze_solving_route_upward_downward():
    maze = "#####\n# S #\n#   #\n# E #\n#####"
    route = solve_maze(maze)
    # Path should go down to exit
    assert route == [(2, 1), (2, 2), (3, 2), (3, 3)]

def test_maze_solving_dot_as_corridor():
    maze = "#####\n# S .#\n# E #\n#####"
    route = solve_maze(maze)
    # Path: [(2, 1), (2, 2), (3, 2)]
    assert route == [(2, 1), (2, 2), (3, 2)]