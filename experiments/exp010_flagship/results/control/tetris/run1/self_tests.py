from solution import Board, Piece

def test_board_initialization():
    board = Board(3, 3)
    # Expected representation of a 3x3 empty board
    expected_output = "... \n... \n... \n"  # 3 rows of dots, each ending with a newline
    assert str(board) == expected_output

def test_board_initialization_6x3():
    board = Board(6, 3)
    # Expected representation of a 6x3 empty board
    expected_output = "......\n......\n......\n"  # 3 rows of 6 dots, each ending with a newline
    assert str(board) == expected_output

def test_drop_single_block():
    board = Board(3, 3)
    board.drop('A')
    # Expected representation after dropping 'A' in the middle column
    expected_output = "... \n A. \n... \n"  # 'A' in the middle of the second row
    assert str(board) == expected_output

def test_falling_block_moves_down():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # Move down
    # Expected representation after one tick
    expected_output = "... \n... \n A. \n"  # 'A' moved down to the last row
    assert str(board) == expected_output

def test_block_lands_at_bottom():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # Move down
    board.tick()  # Move down
    # Block should land after the second tick
    board.tick()  # Should not move down anymore
    expected_output = "... \n... \n A. \n"  # 'A' is now settled
    assert str(board) == expected_output

def test_prevent_multiple_drops():
    board = Board(3, 3)
    board.drop('A')
    result = board.drop('B')
    # Expecting the message "already falling"
    assert result == "already falling"

def test_falling_block_stops_on_landed_block():
    board = Board(3, 3)
    board.drop('A')
    board.tick()  # Move down
    board.drop('B')  # Drop another block
    # Block 'B' should not be able to fall
    assert str(board) == "... \n A. \n B. \n"  # 'B' is on top of 'A'

def test_define_piece_shape():
    piece = Piece([".T.", "TTT", "..."])
    # Expected representation of the piece
    expected_output = ".T.\nTTT\n...\n"  # The piece shape defined
    assert str(piece) == expected_output

def test_rotate_piece_right():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_right()
    # After rotating right, should be "...", ".XX", "..."
    expected_output = "... \n.XX\n...\n"  # The rotated shape
    assert str(piece) == expected_output

def test_rotate_piece_left():
    piece = Piece([".X.", ".X.", "..."])
    piece.rotate_left()
    # After rotating left, should be "...", "XX.", "..."
    expected_output = "... \nXX.\n...\n"  # The rotated shape
    assert str(piece) == expected_output

def test_drop_piece_on_board():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    # Expected representation after dropping piece in center
    expected_output = "......\n......\n...T..\n..TTT.\n......\n"  # Piece dropped centered
    assert str(board) == expected_output

def test_piece_lands_and_stops():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.tick()  # Move down
    # Piece should land after two ticks
    expected_output = "......\n......\n......\n...T..\n..TTT.\n"  # Piece is now settled
    assert str(board) == expected_output

def test_steer_piece_left():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.steer_left()  # Move piece left
    expected_output = "......\n......\n......\n..T...\n.TTT..\n"  # Piece moved left
    assert str(board) == expected_output

def test_steer_piece_right():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.steer_right()  # Move piece right
    expected_output = "......\n......\n......\n...T..\n..TTT.\n"  # Piece is unchanged
    assert str(board) == expected_output

def test_rotate_piece_when_falling():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.rotate_right()  # Rotate while falling
    expected_output = "......\n......\n......\n..T...\n.TTT..\n"  # Piece rotated
    assert str(board) == expected_output

def test_rotate_piece_if_blocked():
    board = Board(6, 3)
    piece = Piece(["...T..", "..TTT.", "......"])
    board.drop_piece(piece)
    board.tick()  # Move down
    board.steer_left()  # Move piece left
    board.rotate_right()  # Attempt to rotate right while blocked
    expected_output = "......\n......\n......\n..T...\n.TTT..\n"  # Piece remains blocked
    assert str(board) == expected_output