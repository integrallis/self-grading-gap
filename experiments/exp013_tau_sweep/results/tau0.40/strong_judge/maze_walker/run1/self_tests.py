import pytest
from solution import validate_and_parse_maze, solve_maze

# US-1: Reading the drawing

def test_validate_and_parse_maze_valid():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "#####"
    ]
    # Expected width = 5, height = 5, start = (2, 1), exit = (2, 3)
    parsed_maze = validate_and_parse_maze(drawing)
    assert parsed_maze['width'] == 5
    assert parsed_maze['height'] == 5
    assert parsed_maze['start'] == (2, 1)
    assert parsed_maze['exit'] == (2, 3)

def test_validate_and_parse_maze_multiple_starts():
    drawing = [
        "#####",
        "# S #",
        "# S #",
        "# E #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Maze must contain exactly one start 'S'"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_no_start():
    drawing = [
        "#####",
        "#   #",
        "# E #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Maze must contain exactly one start 'S'"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_multiple_exits():
    drawing = [
        "#####",
        "# S #",
        "# E #",
        "# E #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Maze must contain exactly one exit 'E'"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_no_exit():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Maze must contain exactly one exit 'E'"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_unknown_character():
    drawing = [
        "#####",
        "# S #",
        "# ? #",
        "# E #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Unknown maze character"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_blank_lines():
    drawing = [
        "",
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "#####",
        ""
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    # Expected width = 5, height = 5, start = (2, 1), exit = (2, 3)
    assert parsed_maze['width'] == 5
    assert parsed_maze['height'] == 5
    assert parsed_maze['start'] == (2, 1)
    assert parsed_maze['exit'] == (2, 3)

def test_validate_and_parse_maze_leading_spaces():
    drawing = [
        "#####",
        "   # S #",
        "#   #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    assert parsed_maze['start'] == (5, 1)  # Leading spaces preserved
    assert parsed_maze['exit'] == (2, 3)

def test_validate_and_parse_maze_open_and_closed_cells():
    drawing = [
        "#####",
        "# S #",
        "# * #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    assert parsed_maze.is_open((3, 1))  # Open corridor
    assert not parsed_maze.is_open((2, 2))  # Wall

def test_validate_and_parse_maze_dot_corridor():
    drawing = [
        "#####",
        "# S #",
        "# . #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    assert parsed_maze.is_open((3, 1))  # Open corridor (dot)

# US-2: Walking the shortest route

def test_solve_maze_shortest_route():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    route = solve_maze(parsed_maze)
    # Expected route [(2, 1), (2, 2), (2, 3)]
    assert route == [(2, 1), (2, 2), (2, 3)]

def test_solve_maze_start_next_to_exit():
    drawing = [
        "#####",
        "# S #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    route = solve_maze(parsed_maze)
    # Expected route [(2, 1), (2, 2)]
    assert route == [(2, 1), (2, 2)]

def test_solve_maze_no_path_to_exit():
    drawing = [
        "#####",
        "# S #",
        "# # #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(parsed_maze)

def test_solve_maze_walled_off_exit():
    drawing = [
        "#####",
        "# S #",
        "# # #",
        "#   #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(parsed_maze)

def test_solve_maze_multiple_routes():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    route = solve_maze(parsed_maze)
    # Route can go through (2, 2) or (1, 2), but the minimum length is expected
    assert route == [(2, 1), (2, 2), (2, 3)]

def test_solve_maze_route_turns_around_corner():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# # #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    route = solve_maze(parsed_maze)
    # Updated expected route that turns around the corner
    assert route == [(2, 1), (2, 2), (1, 2), (0, 2), (0, 3)]

def test_solve_maze_route_movement_upward():
    drawing = [
        "#####",
        "#   #",
        "# S #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    route = solve_maze(parsed_maze)
    assert route == [(2, 2), (1, 2), (0, 2)]

def test_solve_maze_diagonal_only_contact():
    drawing = [
        "#####",
        "#   #",
        "# S #",
        "#   #",
        "# E #",
        "#####"
    ]
    parsed_maze = validate_and_parse_maze(drawing)
    with pytest.raises(ValueError, match="No path to exit"):
        solve_maze(parsed_maze)

def test_validate_and_parse_maze_unknown_character_edge():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "# ? #",
        "#####"
    ]
    with pytest.raises(ValueError, match="Unknown maze character"):
        validate_and_parse_maze(drawing)

def test_validate_and_parse_maze_unknown_character_corner():
    drawing = [
        "#####",
        "# S #",
        "#   #",
        "# E #",
        "?",
        "#####"
    ]
    with pytest.raises(ValueError, match="Unknown maze character"):
        validate_and_parse_maze(drawing)