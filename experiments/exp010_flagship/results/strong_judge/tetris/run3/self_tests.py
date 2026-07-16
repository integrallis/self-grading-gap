from solution import Board, Piece

# US-1: See the board
def test_empty_board_renders_correctly():
    board = Board(3, 3)
    assert board.render() == '...\n...\n...\n'  # 3 rows of 3 dots

def test_non_square_empty_board_renders_correctly():
    board = Board(4, 5)
    assert board.render() == '....\n....\n....\n....\n....\n'  # 5 rows of 4 dots

# US-2: Drop single blocks that fall and land
def test_initial_board_has_no_falling_block():
    board = Board(3, 3)
    assert board.render() == '...\n...\n...\n'  # No block is falling initially

def test_drop_block_places_it_in_play():
    board = Board(6, 4)
    board.drop_block('A')
    assert board.render() == '......\n......\n......\n..A...\n'  # Block 'A' visible at (3, 2)

def test_drop_block_in_middle_column():
    board = Board(3, 3)
    board.drop_block('A')
    assert board.render() == '...\n.A.\n...\n'  # At the top middle

def test_tick_moves_block_down():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()
    assert board.render() == '...\n.A.\n...\n'  # Block is still falling
    board.tick()
    assert board.render() == '...\n...\n.A..\n'  # Moved down one row

def test_block_lands_at_bottom():
    board = Board(3, 3)
    board.drop_block('A')
    for _ in range(3):
        board.tick()  # Move down until it settles
    assert board.render() == '...\n...\n.A..\n'  # Block 'A' at the bottom
    board.tick()  # Should still be falling
    assert board.render() == '...\n...\n.A..\n'  # Still at bottom, then becomes settled next tick

def test_cannot_drop_block_while_one_is_falling():
    board = Board(3, 3)
    board.drop_block('A')
    assert board.drop_block('B') == "already falling"  # Should refuse to drop

def test_falling_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Move down
    board.tick()  # Place landed block at (2, 1)
    board.drop_block('X')  # Simulate a block below
    board.tick()  # Next tick should settle 'A'
    assert board.render() == '...\n.A.\n.X..\n'  # Block 'A' should settle above 'X'

# US-3: Define pieces by their shape
def test_define_piece_by_shape():
    piece = Piece([".T.", "TTT", "..."])
    assert piece.render() == [".T.", "TTT", "..."]  # Renders as defined

def test_t_shape_renders_correctly():
    piece = Piece([".T.", "TTT", "..."])
    assert piece.render() == [".T.", "TTT", "..."]  # T-shape

# US-4: Play whole pieces on the board
def test_drop_piece_appears_at_top_middle():
    board = Board(6, 4)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    assert board.render() == '......\n......\n......\n...T..\n..TTT.\n'  # Centered in a 6-wide board

def test_falling_piece_descends_one_row_per_tick():
    board = Board(3, 3)
    piece = Piece([".X.", ".X.", "..."])
    board.drop_piece(piece)
    board.tick()
    assert board.render() == '...\n.X.\n...\n'  # Moved down one row
    board.tick()
    assert board.render() == '...\n.X.\n.X..\n'  # Moved down again

def test_piece_lands_when_no_further_fall():
    board = Board(3, 3)
    piece = Piece([".X.", ".X.", "..."])
    board.drop_piece(piece)
    for _ in range(3):
        board.tick()  # Move down until it settles
    assert board.render() == '...\n.X.\n.X..\n'  # Piece lands at the bottom

def test_piece_stops_on_landed_material():
    board = Board(3, 3)
    piece = Piece([".X.", ".X.", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.tick()  # Place landed block at (2, 1)
    board.drop_block('X')  # Simulate a block below
    board.tick()  # Next tick should settle piece
    assert board.render() == '...\n.X.\n.X..\n'  # Stops above 'X'

def test_dropped_piece_with_no_room_lands_immediately():
    board = Board(3, 3)
    board.drop_block('X')  # Block in the way
    piece = Piece([".X.", "X..", "..."])
    board.drop_piece(piece)
    assert board.render() == '...\n.X.\n...\n'  # Lands immediately without overlap

def test_piece_with_clip_beyond_board_edges():
    board = Board(4, 3)  # 4 wide, 3 high
    piece = Piece(["XXXX", "X..X", "...."])
    board.drop_piece(piece)
    assert board.render() == 'XXXX\nX..X\n....\n'  # Clipped to fit

# US-5: Steer the falling piece
def test_steer_falling_piece_left():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.steer_left()
    assert board.render() == '.....\n..X..\n.XXX.\n.....\n'  # Moved left

def test_steer_falling_piece_right():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.steer_right()
    assert board.render() == '.....\n...X.\n.XXX.\n.....\n'  # Moved right

def test_steer_falling_piece_cannot_cross_boundaries():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.steer_left()  # First move left
    board.steer_left()  # Attempt to move left again
    assert board.render() == '.....\n..X..\n.XXX.\n.....\n'  # Stay within bounds

def test_steer_no_effect_when_nothing_is_falling():
    board = Board(5, 5)
    board.steer_left()  # Nothing should happen
    assert board.render() == '.....\n.....\n.....\n.....\n.....\n'  # Board unchanged

# US-6: Rotate the falling piece
def test_rotate_falling_piece_clockwise():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.rotate_right()
    assert board.render() == '.....\n..X..\n..XX.\n..X..\n.....\n'  # Rotated correctly

def test_rotate_falling_piece_counter_clockwise():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.rotate_left()
    assert board.render() == '.....\n..X..\n.XX..\n..X..\n.....\n'  # Rotated correctly

def test_rotate_piece_if_it_fits():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.rotate_right()
    board.tick()  # Move down
    board.rotate_right()  # Rotate again
    assert board.render() == '.....\n.....\n.XXX.\n..X..\n.....\n'  # Rotated correctly after moving

def test_rotate_piece_abandon_if_blocked():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.drop_block('X')  # Block in the way
    board.rotate_right()  # Attempt to rotate
    assert board.render() == '.....\n..X..\nXXX..\n.....\n.....\n'  # Should not change

def test_single_block_rotation():
    board = Board(3, 3)
    board.drop_block('A')
    board.rotate_right()  # Should not change anything
    assert board.render() == '...\n.A.\n...\n'  # Block remains unchanged

def test_stock_t_shape_renders_correctly():
    piece = Piece([".T.", "TTT", "..."])
    assert piece.render() == [".T.", "TTT", "..."]  # T-shape