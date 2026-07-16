from solution import Board, Piece

def test_board_initial_state():
    board = Board(3, 3)
    expected_output = "...\n...\n...\n"  # 3 rows of 3 dots
    assert str(board) == expected_output

def test_board_size():
    board = Board(4, 2)
    assert len(str(board).splitlines()) == 2  # height
    assert len(str(board).splitlines()[0]) == 4  # width

def test_drop_single_block_initial_state():
    board = Board(3, 3)
    board.drop_block('A')
    assert str(board) == "...\n.A.\n...\n"  # A is in the top row

def test_drop_single_block_middle_column():
    board = Board(6, 4)
    board.drop_block('B')
    expected_output = "......\n......\n..B...\n......\n"  # B in the center (fourth column)
    assert str(board) == expected_output

def test_single_block_falls_one_row_per_tick():
    board = Board(3, 3)
    board.drop_block('C')
    board.tick()
    assert str(board) == "...\n.C.\n...\n"  # After 1 tick
    board.tick()
    assert str(board) == "...\n...\n.C.\n"  # After 2 ticks
    board.tick()
    assert str(board) == "...\n...\n.C.\n"  # Block remains in place at the bottom

def test_block_lands_and_stops():
    board = Board(3, 3)
    board.drop_block('D')
    for _ in range(3):
        board.tick()
    board.tick()  # This tick should make it land
    assert str(board) == "...\n...\n.D.\n"  # D lands at the bottom

def test_only_one_block_can_fall():
    board = Board(3, 3)
    board.drop_block('F')
    result = board.drop_block('G')  # Attempt to drop another block
    assert result == "already falling"

def test_piece_definition_and_rendering():
    piece = Piece([".T.", "TTT", "..."])
    expected_output = ".T.\nTTT\n..."  # T shape rendering
    assert str(piece) == expected_output

def test_piece_rotation_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    expected_output = ["...", ".XX", "..."]  # Correct clockwise rotation
    assert str(piece) == "\n".join(expected_output)

def test_piece_rotation_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    expected_output = ["...", "XX.", "..."]  # Correct counter-clockwise rotation
    assert str(piece) == "\n".join(expected_output)

def test_t_shape_rendering():
    piece = Piece([".T.", "TTT", "..."])
    expected_output = ".T.\nTTT\n..."  # T shape rendering
    assert str(piece) == expected_output

def test_drop_piece_and_center_on_board():
    board = Board(7, 5)
    piece = Piece([".T.", "TTT", "..."])
    board.drop_piece(piece)
    expected_output = "....T..\n...TTT.\n.......\n.......\n.......\n"  # T shape centered on width 7
    assert str(board) == expected_output

def test_falling_piece_moves_down_each_tick():
    board = Board(3, 3)
    piece = Piece([".X.", ".X.", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    assert str(board) == "...\n.X.\n.X.\n"  # After 1 tick
    board.tick()  # Move down again
    assert str(board) == "...\n...\n.X.\n"  # After 2 ticks

def test_steer_falling_piece_left():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move the piece down
    board.steer_left()  # Move left
    expected_output = ".....\n.....\n..X..\nXXX..\n.....\n"  # Piece moved left
    assert str(board) == expected_output

def test_steer_falling_piece_right():
    board = Board(5, 5)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move the piece down
    board.steer_right()  # Move right
    expected_output = ".....\n.....\n...X.\nXXX..\n.....\n"  # Piece moved right
    assert str(board) == expected_output

def test_steer_does_not_cross_boundaries():
    board = Board(5, 5)
    piece = Piece(["X", "X", "X"])
    board.drop_piece(piece)
    board.tick()  # Move the piece down
    board.steer_left()  # Move left
    board.steer_left()  # Attempt to move left again
    expected_output = ".....\n.....\n.....\nXX...\n.....\n"  # Piece stays at column 0
    assert str(board) == expected_output

def test_rotate_falling_piece():
    board = Board(3, 3)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move the piece down
    board.rotate_right()  # Rotate
    expected_output = "...\n.X.\nXXX\n"  # Rotation abandoned due to border
    assert str(board) == expected_output

def test_rotate_single_block_changes_nothing():
    board = Board(4, 4)
    board.drop_block('B')
    board.rotate_right()  # Rotate a single block
    expected_output = "....\n....\n..B.\n....\n"  # Block remains unchanged
    assert str(board) == expected_output

def test_board_has_no_falling_item():
    board = Board(3, 3)
    assert str(board) == "...\n...\n...\n"  # No falling item

def test_blocks_and_pieces_can_be_dropped_in_succession():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Move down
    board.tick()  # Land block
    board.drop_piece(Piece([".X.", "XXX", "..."]))
    board.tick()  # Move piece down
    expected_output = "...\n.A.\n.X.\nXXX\n"  # Verify both are on the board
    assert str(board) == expected_output

def test_empty_cells_in_falling_piece_are_transparent():
    board = Board(3, 3)
    board.drop_block('A')  # Drop a block first
    board.tick()  # Move down
    piece = Piece([".X.", "X.X", "..."])
    board.drop_piece(piece)
    board.tick()  # Move down
    expected_output = "...\n.A.\nX.X\n"  # A should be visible behind empty cells
    assert str(board) == expected_output

def test_piece_with_no_room_to_descend_lands_immediately():
    board = Board(3, 3)
    board.drop_block('X')  # Land a block
    piece = Piece(["X", "X", "X"])  # Piece cannot fall
    board.drop_piece(piece)
    expected_output = "...\nX..\nX..\n"  # Piece lands immediately
    assert str(board) == expected_output

def test_clip_pieces_beyond_right_edge():
    board = Board(5, 5)
    piece = Piece(["..X.", "XXX", "..."])  # Piece has part extending beyond right edge
    board.drop_piece(piece)
    board.tick()  # Move down
    expected_output = ".....\n.....\n..X..\nXXX..\n.....\n"  # Clipped on right
    assert str(board) == expected_output

def test_clip_pieces_beyond_bottom_edge():
    board = Board(5, 3)
    piece = Piece(["X", "X", "X", "X"])  # Vertical piece too tall for board
    board.drop_piece(piece)
    for _ in range(3):
        board.tick()  # Move down
    expected_output = ".....\n.....\nXXX..\n"  # Clipped at the bottom
    assert str(board) == expected_output

def test_bottom_row_block_is_falling():
    board = Board(3, 3)
    board.drop_block('A')
    for _ in range(3):
        board.tick()  # Move down to the bottom
    assert str(board) == "...\n...\n.A.\n"  # It is still falling
    board.tick()  # Should settle now
    assert str(board) == "...\n...\n.A.\n"  # After settling

def test_drop_piece_while_block_is_falling():
    board = Board(3, 3)
    board.drop_block('A')
    board.tick()  # Move down
    result = board.drop_piece(Piece([".X.", "XXX", "..."]))  # Attempt to drop a piece
    assert result == "already falling"

def test_steering_empty_board_does_nothing():
    board = Board(3, 3)
    board.steer_left()  # No falling block
    assert str(board) == "...\n...\n...\n"  # Board remains unchanged

def test_steering_single_block():
    board = Board(3, 3)
    board.drop_block('B')
    board.steer_left()  # Attempt to steer left
    assert str(board) == "....\n....\n..B.\n....\n"  # Block remains unchanged

def test_rotate_successful_on_falling_piece():
    board = Board(3, 3)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    board.tick()  # Move the piece down
    board.rotate_right()  # Rotate
    expected_output = "...\n.X.\nXXX\n"  # Rotation successful
    assert str(board) == expected_output

def test_rotate_rejected_by_landed_material():
    board = Board(3, 3)
    piece = Piece([".X.", "XXX", "..."])
    board.drop_piece(piece)
    for _ in range(2):
        board.tick()  # Move down
    board.rotate_right()  # Rotate should be rejected
    expected_output = "...\n.X.\nXXX\n"  # Should remain the same
    assert str(board) == expected_output