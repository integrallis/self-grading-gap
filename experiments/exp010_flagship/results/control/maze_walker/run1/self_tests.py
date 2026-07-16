from solution import parse_maze, solve_maze

def test_parse_maze_valid():
    maze_str = """
    #####
    #S E#
    #####
    """
    parsed_maze = parse_maze(maze_str)
    # width = 5, height = 3, start = (1, 1), exit = (3, 1)
    assert parsed_maze['width'] == 5
    assert parsed_maze['height'] == 3
    assert parsed_maze['start'] == (1, 1)
    assert parsed_maze['exit'] == (3, 1)

def test_parse_maze_multiple_starts():
    maze_str = """
    #####
    #S S#
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_str)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_missing_start():
    maze_str = """
    #####
    # E#
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_str)
    assert str(excinfo.value) == "Maze must contain exactly one start 'S'"

def test_parse_maze_multiple_exits():
    maze_str = """
    #####
    #S E E#
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_str)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_missing_exit():
    maze_str = """
    #####
    #S  #
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_str)
    assert str(excinfo.value) == "Maze must contain exactly one exit 'E'"

def test_parse_maze_unknown_character():
    maze_str = """
    #####
    #S Z#
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        parse_maze(maze_str)
    assert "Unknown maze character" in str(excinfo.value)

def test_parse_maze_valid_with_leading_spaces():
    maze_str = """
      #####
      #S E#
      #####
    """
    parsed_maze = parse_maze(maze_str)
    # width = 5, height = 3, start = (1, 1), exit = (3, 1)
    assert parsed_maze['width'] == 5
    assert parsed_maze['height'] == 3
    assert parsed_maze['start'] == (1, 1)
    assert parsed_maze['exit'] == (3, 1)

def test_solve_maze_no_path():
    maze_str = """
    #####
    #S*E#
    #####
    """
    with pytest.raises(ValueError) as excinfo:
        solve_maze(maze_str)
    assert str(excinfo.value) == "No path to exit"

def test_solve_maze_direct_neighbor():
    maze_str = """
    #####
    #S E#
    #####
    """
    path = solve_maze(maze_str)
    # path should be [(1, 1), (3, 1)]
    assert path == [(1, 1), (2, 1), (3, 1)]

def test_solve_maze_longer_path():
    maze_str = """
    #####
    #S  #
    # # #
    # E #
    #####
    """
    path = solve_maze(maze_str)
    # path should be [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
    assert path == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]

def test_solve_maze_with_dots():
    maze_str = """
    #####
    #S. #
    # # #
    # E #
    #####
    """
    path = solve_maze(maze_str)
    # path should be [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]
    assert path == [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]