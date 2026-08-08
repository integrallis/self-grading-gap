import pytest
from solution import parse_maze, solve_maze

def test_parse_maze_valid():
    drawing = """
######
#S   #
#    #
#  E #
######
"""
    maze = parse_maze(drawing)
    # Width: 6, Height: 5, Start: (1, 1), Exit: (3, 3)
    assert maze['width'] == 6
    assert maze['height'] == 5
    assert maze['start'] == (1, 1)
    assert maze['exit'] == (3, 3)

def test_parse_maze_missing_start():
    drawing = """
######
#    #
#    #
#  E #
######
"""
    with pytest.raises(ValueError) as exc:
        parse_maze(drawing)
    assert str(exc.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_multiple_starts():
    drawing = """
######
#S   #
#S  E#
######
"""
    with pytest.raises(ValueError) as exc:
        parse_maze(drawing)
    assert str(exc.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_missing_exit():
    drawing = """
######
#S   #
#    #
######
"""
    with pytest.raises(ValueError) as exc:
        parse_maze(drawing)
    assert str(exc.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_multiple_exits():
    drawing = """
######
#S   #
# E #
# E #
######
"""
    with pytest.raises(ValueError) as exc:
        parse_maze(drawing)
    assert str(exc.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_unknown_character():
    drawing = """
######
#S   #
#    X
#  E #
######
"""
    with pytest.raises(ValueError) as exc:
        parse_maze(drawing)
    assert "Unknown maze character" in str(exc.value)

def test_parse_maze_with_leading_spaces():
    drawing = """
  ######
  #S   #
  #    #
  #  E #
  ######
"""
    maze = parse_maze(drawing)
    # Width: 8, Height: 5, Start: (3, 1), Exit: (5, 3)
    assert maze['width'] == 8
    assert maze['height'] == 5
    assert maze['start'] == (3, 1)
    assert maze['exit'] == (5, 3)

def test_solve_maze_success():
    drawing = """
######
#S   #
#    #
#  E #
######
"""
    route = solve_maze(drawing)
    # The expected length is 5 since the route can be: (1, 1) -> (1, 2) -> (1, 3) -> (2, 3) -> (3, 3)
    assert len(route) >= 5  # Validating minimum length, exact path not asserted due to multiple options

def test_solve_maze_directly_beside_exit():
    drawing = """
######
#S E #
######
"""
    route = solve_maze(drawing)
    # Expected route: [(1, 1), (2, 1)]
    assert route == [(1, 1), (2, 1)]

def test_solve_maze_no_path_to_exit():
    drawing = """
######
#S* E#
######
"""
    with pytest.raises(ValueError) as exc:
        solve_maze(drawing)
    assert str(exc.value) == "No path to exit"

def test_solve_maze_exit_unreachable_diagonally():
    drawing = """
######
#S   #
#  E #
######
"""
    with pytest.raises(ValueError) as exc:
        solve_maze(drawing)
    assert str(exc.value) == "No path to exit"

def test_solve_maze_walled_exit():
    drawing = """
######
#S   #
#***E#
######
"""
    with pytest.raises(ValueError) as exc:
        solve_maze(drawing)
    assert str(exc.value) == "No path to exit"

def test_solve_maze_dot_corridor():
    drawing = """
######
#S.  #
#    #
#  E #
######
"""
    route = solve_maze(drawing)
    # The expected length is 5 since the route can be: (1, 1) -> (1, 2) -> (1, 3) -> (2, 3) -> (3, 3)
    assert len(route) >= 5  # Validating minimum length, exact path not asserted due to multiple options

def test_solve_maze_route_around_corner():
    drawing = """
######
#S   #
# #  #
# E  #
######
"""
    route = solve_maze(drawing)
    # Expected route: [(1, 1), (1, 2), (1, 3), (2, 3)]
    assert len(route) >= 4  # Validating minimum length, exact path not asserted due to multiple options

def test_solve_maze_route_upward_and_downward():
    drawing = """
######
#S   #
#  #E#
######
"""
    route = solve_maze(drawing)
    # Expected route can be: (1, 1) -> (1, 2) -> (2, 2) -> (3, 2) -> (4, 2)
    assert len(route) >= 5  # Validating minimum length, exact path not asserted due to multiple options

def test_solve_maze_multiple_routes():
    drawing = """
######
#S   #
# #  #
# E  #
######
"""
    route = solve_maze(drawing)
    # The route should be valid, checking that it starts with S and ends with E
    assert route[0] == (1, 1)
    assert route[-1] == (3, 3)
    assert len(route) >= 4  # Minimum length assertion