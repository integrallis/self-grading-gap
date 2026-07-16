import pytest
from solution import parse_maze, solve_maze

# Test suite for maze solving from text art

# US-1: Reading the drawing

# AC-1.1: Validate drawing legend
def test_parses_valid_maze():
    maze = """
#####
# S E
#####
"""
    parsed = parse_maze(maze)
    assert parsed['width'] == 5  # 5 columns (5 walls)
    assert parsed['height'] == 3  # 3 rows
    assert parsed['start'] == (2, 1)  # Start at (2, 1)
    assert parsed['exit'] == (4, 1)  # Exit at (4, 1)

# AC-1.4: Reject maze without exactly one start
def test_rejects_maze_without_start():
    maze = """
#####
#   E
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

# AC-1.4: Reject maze with duplicate start
def test_rejects_maze_with_duplicate_start():
    maze = """
#####
# S S E
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

# AC-1.5: Reject maze without exactly one exit
def test_rejects_maze_without_exit():
    maze = """
#####
# S #
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

# AC-1.5: Reject maze with duplicate exit
def test_rejects_maze_with_duplicate_exit():
    maze = """
#####
# S E E
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

# AC-1.6: Reject maze with unknown characters
def test_rejects_maze_with_unknown_character():
    maze = """
#####
# S @
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

# AC-1.6: Reject maze with unknown character in a valid maze
def test_rejects_maze_with_unknown_character_at_edge():
    maze = """
#####
# S E
# @ #
#####
"""
    with pytest.raises(Exception) as excinfo:
        parse_maze(maze)
    assert "Unknown maze character" in str(excinfo.value)

# AC-1.7: Test that surrounding blank lines are discarded
def test_removes_surrounding_blank_lines():
    maze = """
    
#####
# S E
#####
    
"""
    parsed = parse_maze(maze)
    assert parsed['width'] == 5
    assert parsed['height'] == 3

# AC-1.7: Test that leading spaces are preserved
def test_preserves_leading_spaces():
    maze = """
#####
# S E
#  . #
#####
"""
    parsed = parse_maze(maze)
    assert parsed['start'] == (2, 1)
    assert parsed['exit'] == (4, 1)

# AC-1.2: Validate open/walled status of cells
def test_cell_open_walled_status():
    maze = """
#####
# S E
#  . #
#####
"""
    parsed = parse_maze(maze)
    assert not parsed['is_open'](0, 0)  # Wall
    assert parsed['is_open'](1, 1)      # Start
    assert parsed['is_open'](2, 1)      # Corridor
    assert not parsed['is_open'](0, 1)  # Wall
    assert parsed['is_open'](4, 1)      # Exit

# US-2: Walking the shortest route

# AC-2.1: Route returned as a sequence of coordinates
def test_solves_maze_with_route():
    maze = """
#####
# S E
#####
"""
    path = solve_maze(maze)
    assert path == [(2, 1), (3, 1), (4, 1)]  # Start at (2, 1) -> corridor at (3, 1) -> Exit at (4, 1)

# AC-2.2: Start directly beside exit
def test_solves_maze_with_adjacent_start_exit():
    maze = """
#####
# S #
# E #
#####
"""
    path = solve_maze(maze)
    assert path == [(2, 1), (2, 2)]  # Start at (2, 1) -> Exit at (2, 2)

# AC-2.3: Ensure consecutive coordinates differ by exactly one square
def test_consecutive_coordinates_differ_by_one_square():
    maze = """
#####
# S E
#####
"""
    path = solve_maze(maze)
    for i in range(len(path) - 1):
        assert abs(path[i][0] - path[i + 1][0]) + abs(path[i][1] - path[i + 1][1]) == 1

# AC-2.4: Test route follows corners and walls
def test_solves_maze_with_corners():
    maze = """
#####
# S . #
#   E #
#####
"""
    path = solve_maze(maze)
    assert path == [(2, 1), (2, 2), (3, 2), (4, 2)]  # Follow around the corner

# AC-2.5: Test multiple routes and shortest one is returned
def test_solves_maze_with_multiple_routes():
    maze = """
#####
# S . #
# . . #
# E # #
#####
"""
    path = solve_maze(maze)
    assert path[0] == (2, 1)  # Starts at S
    assert path[-1] == (4, 2)  # Ends at E
    assert len(path) == 5  # Route length should be 5

# AC-2.6: Ensure dot corridor cells are walked like spaces
def test_solves_maze_with_dot_corridor():
    maze = """
#####
# S . #
# E # #
#####
"""
    path = solve_maze(maze)
    assert path == [(2, 1), (2, 2), (3, 2)]  # Valid path through dot

# AC-3.1: Walled-off exit raises no-path error
def test_rejects_walled_off_exit():
    maze = """
#####
# S #
# # #
# E #
#####
"""
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

# AC-3.2: Exit unreachable if adjacent diagonally
def test_unreachable_exit_diagonal():
    maze = """
#####
# S #
#   E
#####
"""
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"

# AC-3.3: Test that both wall characters block movement
def test_both_wall_characters_block_movement():
    maze = """
#####
# S #
# * #
# E #
#####
"""
    with pytest.raises(Exception) as excinfo:
        solve_maze(maze)
    assert str(excinfo.value) == "No path to exit"